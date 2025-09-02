#!/usr/bin/env python3
"""
测试新的节点配置格式和API调用方式
"""

import requests
import json
from node_tasks import NodeTaskManager

def test_id_based_query():
    """测试基于ID的查询方式"""
    print("🔍 测试基于ID的查询方式")
    print("=" * 50)
    
    # 测试节点ID
    test_ids = [
        "Qmb14s2Es99SDQ6Fh6kkZkM6359raDgBLdjcYoSk3nxxv7",
        "QmPboLHehSK3TJYkDskwDW4tFqhJDne8xLiKTiEARMuavj"
    ]
    
    for peer_id in test_ids:
        print(f"\n📡 查询节点ID: {peer_id}")
        url = f"https://dashboard.gensyn.ai/api/v1/peer?id={peer_id}"
        
        try:
            response = requests.get(url)
            print(f"状态码: {response.status_code}")
            
            if response.ok:
                data = response.json()
                print("✅ API 响应成功:")
                print(f"  Peer ID: {data.get('peerId', 'N/A')}")
                print(f"  Reward: {data.get('reward', 'N/A')}")
                print(f"  Score: {data.get('score', 'N/A')}")
                print(f"  在线状态: {'🟢在线' if data.get('online', False) else '🔴离线'}")
            else:
                print(f"❌ API 请求失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 错误: {str(e)}")

def test_new_config_format():
    """测试新的配置格式"""
    print("\n🔧 测试新的配置格式")
    print("=" * 50)
    
    # 模拟新的配置格式
    config = {
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
    
    print("📋 新配置格式示例:")
    print(json.dumps(config, indent=2, ensure_ascii=False))
    
    print("\n📊 节点信息:")
    for i, node in enumerate(config["PEER_NAMES"], 1):
        print(f"  {i}. ID: {node['id'][:20]}...")
        print(f"     备注: {node['remark']}")

if __name__ == "__main__":
    print("🚀 Gensyn 节点监控 - 新格式测试")
    print("=" * 60)
    
    test_id_based_query()
    test_new_config_format()
    
    print("\n✅ 测试完成！")
    print("\n💡 建议:")
    print("1. 使用ID查询获得更准确的在线状态")
    print("2. 添加备注信息便于识别服务器")
    print("3. 新格式完全兼容旧格式")
