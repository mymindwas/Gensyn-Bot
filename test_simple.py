import requests
import json
from node_tasks import NodeTaskManager

def test_simple_api():
    """测试简化的 API 调用"""
    task_manager = NodeTaskManager()
    
    # 测试节点名称
    test_names = ["loud sleek bat", "knobby leaping kangaroo"]
    
    for name in test_names:
        print(f"\n测试节点: {name}")
        url_name = name.replace(" ", "%20")
        url = f"https://dashboard.gensyn.ai/api/v1/peer?name={url_name}"
        
        try:
            response = requests.get(url)
            print(f"状态码: {response.status_code}")
            
            if response.ok:
                data = response.json()
                print("API 响应:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                
                # 更新统计数据
                task_manager.update_node_stats(
                    data["peerId"], 
                    data.get("reward", 0), 
                    data.get("score", 0), 
                    data.get("online", False)
                )
                
                # 获取变化
                changes = task_manager.get_stats_change(data["peerId"])
                if changes:
                    print(f"\n变化检测:")
                    for key, change in changes.items():
                        print(f"  {key}: {change}")
                
            else:
                print(f"API 请求失败: {response.text}")
                
        except Exception as e:
            print(f"错误: {str(e)}")

if __name__ == "__main__":
    test_simple_api() 