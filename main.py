import os
import json
import requests
import time
from datetime import datetime
from node_tasks import NodeTaskManager

CONFIG_FILE = "config.json"

# 初始化任务管理器
task_manager = NodeTaskManager()

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print("❌ 配置文件不存在，请先运行 python setup.py")
        return None
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def send_telegram_message(token, chat_id, message: str):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    return requests.post(url, json=payload)

def fetch_peer_data(peer_name):
    url_name = peer_name.replace(" ", "%20")
    url = f"https://dashboard.gensyn.ai/api/v1/peer?name={url_name}"
    try:
        response = requests.get(url)
        if response.ok:
            data = response.json()
            task_manager.update_node_stats(
                data["peerId"], 
                data.get("reward", 0), 
                data.get("score", 0), 
                data.get("online", False)
            )
            return data
    except Exception as e:
        print(f"获取节点数据失败: {str(e)}")
    return None

def format_node_status(name, info, peerno, previous_data=None):
    peer_id = info["peerId"]
    reward = info.get("reward", 0)
    score = info.get("score", 0)
    online = info.get("online", False)
    
    # 获取统计数据变化
    stats_changes = task_manager.get_stats_change(peer_id)
    
    changes = []
    if previous_data:
        prev_reward = previous_data.get("reward", 0)
        prev_score = previous_data.get("score", 0)
        prev_online = previous_data.get("online", False)
        
        if reward != prev_reward:
            change = reward - prev_reward
            changes.append(f"R:{prev_reward}→{reward}({change:+.0f})")
        
        if score != prev_score:
            change = score - prev_score
            changes.append(f"S:{prev_score}→{score}({change:+.0f})")
        
        if online != prev_online:
            status_change = "🟢上线" if online else "🔴离线"
            changes.append(status_change)

    status_icon = "🟢" if online else "🔴"
    change_text = " | " + " | ".join(changes) if changes else ""
    
    msg = f"<b>{peerno}</b> {status_icon} <code>{name}</code>\n"
    msg += f"R:{reward} | S:{score} | ID:{peer_id[:12]}...{change_text}"
    
    # 添加统计数据趋势
    if stats_changes:
        msg += "\n📊 趋势: "
        trend_parts = []
        if 'reward' in stats_changes:
            r_change = stats_changes['reward']
            trend_parts.append(f"R:{r_change['change']:+.0f}")
        if 'score' in stats_changes:
            s_change = stats_changes['score']
            trend_parts.append(f"S:{s_change['change']:+.0f}")
        if 'online' in stats_changes:
            o_change = stats_changes['online']
            trend_parts.append("🟢上线" if o_change['current'] else "🔴离线")
        msg += " | ".join(trend_parts)
    return msg

def query_nodes_status(config, chat_id):
    """查询所有节点状态"""
    try:
        messages = []
        current_data = {}

        for name in config["PEER_NAMES"]:
            data = fetch_peer_data(name)
            if data:
                current_data[data["peerId"]] = data

        for i, (name, info) in enumerate(current_data.items(), 1):
            msg = format_node_status(name, info, i)
            messages.append(msg)

        timestamp = datetime.now().strftime("%H:%M:%S")
        full_message = f"<b>📊 Gensyn Nodes Status ({timestamp})</b>\n\n"
        full_message += "\n".join(messages)

        response = send_telegram_message(config["TELEGRAM_API_TOKEN"], chat_id, full_message)
        
        if not response.ok:
            send_telegram_message(config["TELEGRAM_API_TOKEN"], chat_id, "❌ 查询失败，请稍后重试")
            
    except Exception as e:
        send_telegram_message(config["TELEGRAM_API_TOKEN"], chat_id, f"❌ 查询失败: {str(e)}")

def get_updates(config, offset=None):
    """获取Telegram更新"""
    url = f"https://api.telegram.org/bot{config['TELEGRAM_API_TOKEN']}/getUpdates"
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    
    try:
        response = requests.get(url, params=params, timeout=35)
        if response.ok:
            return response.json()
    except Exception as e:
        print(f"获取更新失败: {str(e)}")
    return None

def process_message(config, message):
    """处理消息"""
    chat_id = message['chat']['id']
    text = message.get('text', '').strip()
    
    # 检查是否是授权用户
    if str(chat_id) != config["CHAT_ID"]:
        return
    
    if text == '/start':
        welcome_msg = """🤖 <b>Gensyn 节点监控机器人</b>

可用命令：
/status - 查询所有节点状态
/help - 显示帮助信息

机器人会显示节点的 Reward、Score 和在线状态变化。"""
        send_telegram_message(config["TELEGRAM_API_TOKEN"], chat_id, welcome_msg)
    
    elif text == '/status':
        send_telegram_message(config["TELEGRAM_API_TOKEN"], chat_id, "🔄 正在查询节点状态...")
        query_nodes_status(config, chat_id)
    
    elif text == '/help':
        help_msg = """📖 <b>帮助信息</b>

<b>命令列表：</b>
/start - 启动机器人
/status - 查询所有节点状态
/help - 显示此帮助信息

<b>状态说明：</b>
🟢 - 节点在线
🔴 - 节点离线
R: - Reward 值
S: - Score 值
ID: - Peer ID（前12位）

<b>变化检测：</b>
机器人会自动检测并显示 Reward、Score 和在线状态的变化。"""
        send_telegram_message(config["TELEGRAM_API_TOKEN"], chat_id, help_msg)

def main():
    config = load_config()
    if not config:
        return

    print("🤖 Gensyn 节点监控机器人 - Telegram Bot 模式")
    print("机器人已启动，请在 Telegram 中发送命令：")
    print("- /start - 启动机器人")
    print("- /status - 查询节点状态")
    print("- /help - 显示帮助")
    
    offset = None
    
    while True:
        try:
            updates = get_updates(config, offset)
            if updates and updates.get('ok') and updates.get('result'):
                for update in updates['result']:
                    if 'message' in update:
                        process_message(config, update['message'])
                    offset = update['update_id'] + 1
            
            time.sleep(1)  # 避免过于频繁的请求
            
        except KeyboardInterrupt:
            print("\n👋 机器人已停止")
            break
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
            time.sleep(5)  # 出错时等待更长时间

if __name__ == "__main__":
    main()
