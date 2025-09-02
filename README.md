# 🤖 Gensyn 节点监控机器人

这是一个用于监控 Gensyn 节点状态的 Telegram 机器人，支持在 Telegram 中发送命令查询节点的 Reward、Score 和在线状态变化。

## ✨ 功能特点

- 🔍 Telegram 命令查询节点状态
- 📊 追踪 Reward 和 Score 变化
- 🟢🔴 在线状态监控
- 📱 紧凑的 Telegram 消息格式
- 📈 自动变化检测和播报
- 💾 历史数据记录

## 📋 系统要求

- Python 3.7+
- 网络连接
- Telegram 账号

## 🚀 快速开始

### 1. 创建 Telegram Bot

#### 步骤 1: 创建 Bot
1. 在 Telegram 中搜索 `@BotFather`
2. 发送 `/newbot` 命令
3. 按照提示设置机器人名称（例如：Gensyn Monitor）
4. 设置机器人用户名（必须以 'bot' 结尾，例如：gensyn_monitor_bot）
5. 保存获得的 Bot Token（格式：`123456789:ABCdefGHIjklMNOpqrsTUVwxyz`）

#### 步骤 2: 获取 Chat ID
1. 与你的机器人对话，发送 `/start`
2. 访问以下链接（替换 `<YOUR_BOT_TOKEN>` 为你的 Bot Token）：
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
3. 在返回的 JSON 中找到 `"chat" -> "id"` 字段的值
4. 保存这个 Chat ID

### 2. 运行设置脚本
```bash
python setup.py
```

按提示输入：
- **Bot Token**: 从 BotFather 获得的 Token
- **Chat ID**: 你的聊天 ID
- **节点信息**: 支持两种格式

#### 节点配置格式

**格式1 - 简单名称（兼容旧版本）:**
```
loud sleek bat, knobby leaping kangaroo
```

**格式2 - 详细信息（推荐，更准确）:**
```
Qmb14s2Es99SDQ6Fh6kkZkM6359raDgBLdjcYoSk3nxxv7,服务器A
QmPboLHehSK3TJYkDskwDW4tFqhJDne8xLiKTiEARMuavj,服务器B
```

**格式说明：**
- 第一列：节点ID（Peer ID）- 用于准确查询在线状态
- 第二列：备注信息 - 用于标识对应的服务器

**为什么使用ID查询更准确？**
- 使用 `name` 参数查询可能返回不准确的结果
- 使用 `id` 参数查询能获得最准确的节点状态
- 建议优先使用ID进行配置

### 3. 启动机器人
```bash
python main.py
```

### 4. 在 Telegram 中使用

启动机器人后，在 Telegram 中与你的机器人对话：

- `/start` - 启动机器人，显示欢迎信息
- `/status` - 查询所有节点状态
- `/help` - 显示帮助信息

## 📱 消息格式

机器人会发送紧凑格式的状态消息：

```
📊 Gensyn Nodes Status (14:30:25)

1 🟢 loud sleek bat
R:78 | S:216 | ID:QmQR1emZtMW... | R:75→78(+3) | S:210→216(+6)

2 🔴 knobby leaping kangaroo  
R:45 | S:120 | ID:QmX5RDyKC4s... | 🔴离线
```

### 消息说明：
- `1` - 节点编号
- `🟢/🔴` - 在线状态（绿色=在线，红色=离线）
- `loud sleek bat` - 节点名称
- `R:78` - Reward 值
- `S:216` - Score 值
- `ID:QmQR1emZtMW...` - Peer ID 前12位
- `R:75→78(+3)` - Reward 变化（从75增加到78，+3）
- `S:210→216(+6)` - Score 变化
- `🔴离线` - 状态变化提醒

## ⚙️ 配置说明

### 配置文件
配置信息保存在 `config.json` 文件中：

#### 旧格式（兼容）:
```json
{
    "TELEGRAM_API_TOKEN": "your_bot_token_here",
    "CHAT_ID": "your_chat_id_here",
    "PEER_NAMES": ["loud sleek bat", "knobby leaping kangaroo"]
}
```

#### 新格式（推荐）:
```json
{
    "TELEGRAM_API_TOKEN": "your_bot_token_here",
    "CHAT_ID": "your_chat_id_here",
    "PEER_NAMES": [
        {
            "id": "Qmb14s2Es99SDQ6Fh6kkZkM6359raDgBLdjcYoSk3nxxv7",
            "remark": "服务器A"
        },
        {
            "id": "QmPboLHehSK3TJYkDskwDW4tFqhJDne8xLiKTiEARMuavj",
            "remark": "服务器B"
        }
    ]
}
```

### 添加更多节点
编辑 `config.json` 文件，在 `PEER_NAMES` 数组中添加节点名称：

```json
"PEER_NAMES": [
    "loud sleek bat",
    "knobby leaping kangaroo",
    "sly fast tiger",
    "blue quiet elephant"
]
```

## 🛠️ 故障排除

### 常见问题

#### 1. Telegram 连接失败
- 检查 Bot Token 是否正确
- 确认 Chat ID 是否正确
- 确保机器人没有被阻止

#### 2. 机器人无响应
- 确保机器人正在运行（`python main.py`）
- 检查网络连接
- 确认 Bot Token 有效

#### 3. 节点数据获取失败
- 检查网络连接
- 确认节点名称是否正确
- 检查 Gensyn 仪表板是否可访问

### 调试模式
运行测试脚本来验证 API 连接：

```bash
python test_simple.py
```

## 📊 数据存储

### 数据文件
- `node_tasks.json` - 节点统计数据
- `config.json` - 配置文件

## 🔄 使用方法

1. 运行 `python main.py` 启动机器人
2. 在 Telegram 中与机器人对话
3. 发送 `/status` 命令查询节点状态
4. 机器人会返回当前状态和变化信息

## 🚀 部署建议

### 本地运行
```bash
python main.py
```

### 服务器运行
```bash
# 使用 screen 或 tmux 保持运行
screen -S gensyn_bot
python main.py
# Ctrl+A+D 分离会话
```

### 后台运行
```bash
nohup python main.py > bot.log 2>&1 &
```

---

**注意**: 请确保你的 Bot Token 和 Chat ID 安全，不要分享给他人。 