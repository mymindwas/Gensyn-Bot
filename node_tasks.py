import json
import os
from datetime import datetime
from typing import Dict, Optional

class NodeTaskManager:
    def __init__(self, data_file: str = "node_tasks.json"):
        self.data_file = data_file
        self.node_stats: Dict[str, Dict] = {}  # 存储节点统计数据
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.node_stats = data.get("node_stats", {})

    def save_tasks(self):
        data = {
            "node_stats": self.node_stats
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)

    def update_node_stats(self, node_address: str, reward: int, score: int, online: bool):
        """更新节点统计数据"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if node_address not in self.node_stats:
            self.node_stats[node_address] = {
                'reward': [],
                'score': [],
                'online': [],
                'last_update': current_time
            }
        
        # 添加新的数据点
        self.node_stats[node_address]['reward'].append({
            'value': reward,
            'timestamp': current_time
        })
        self.node_stats[node_address]['score'].append({
            'value': score,
            'timestamp': current_time
        })
        self.node_stats[node_address]['online'].append({
            'value': online,
            'timestamp': current_time
        })
        
        # 只保留最近50个数据点
        if len(self.node_stats[node_address]['reward']) > 50:
            self.node_stats[node_address]['reward'] = self.node_stats[node_address]['reward'][-50:]
        if len(self.node_stats[node_address]['score']) > 50:
            self.node_stats[node_address]['score'] = self.node_stats[node_address]['score'][-50:]
        if len(self.node_stats[node_address]['online']) > 50:
            self.node_stats[node_address]['online'] = self.node_stats[node_address]['online'][-50:]
        
        self.node_stats[node_address]['last_update'] = current_time
        self.save_tasks()

    def get_stats_change(self, node_address: str) -> Dict:
        """获取统计数据的变化"""
        if node_address in self.node_stats:
            stats = self.node_stats[node_address]
            changes = {}
            
            # 计算 Reward 变化
            if len(stats['reward']) >= 2:
                current_reward = stats['reward'][-1]['value']
                previous_reward = stats['reward'][-2]['value']
                changes['reward'] = {
                    'current': current_reward,
                    'previous': previous_reward,
                    'change': current_reward - previous_reward
                }
            
            # 计算 Score 变化
            if len(stats['score']) >= 2:
                current_score = stats['score'][-1]['value']
                previous_score = stats['score'][-2]['value']
                changes['score'] = {
                    'current': current_score,
                    'previous': previous_score,
                    'change': current_score - previous_score
                }
            
            # 检查在线状态变化
            if len(stats['online']) >= 2:
                current_online = stats['online'][-1]['value']
                previous_online = stats['online'][-2]['value']
                if current_online != previous_online:
                    changes['online'] = {
                        'current': current_online,
                        'previous': previous_online
                    }
            
            return changes
        return {}

    def get_last_update_time(self, node_address: str) -> Optional[str]:
        """获取最后更新时间"""
        if node_address in self.node_stats:
            return self.node_stats[node_address].get('last_update')
        return None 