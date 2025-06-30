#!/usr/bin/env python3
"""
Gensyn 节点监控机器人快速设置脚本
"""

import os
import sys
import json
import subprocess

def print_banner():
    """打印欢迎横幅"""
    print("🤖" + "="*50 + "🤖")
    print("    Gensyn 节点监控机器人 - 快速设置")
    print("🤖" + "="*50 + "🤖")

def print_telegram_guide():
    """打印 Telegram 设置指南"""
    print("\n📱 请先按照 README.md 中的说明创建 Telegram Bot")
    print("   获取 Bot Token 和 Chat ID 后再继续")

def get_telegram_config():
    """获取 Telegram 配置"""
    print("\n🔧 配置 Telegram Bot")
    print("-" * 30)
    
    config = {}
    config["TELEGRAM_API_TOKEN"] = input("请输入 Bot Token: ").strip()
    config["CHAT_ID"] = input("请输入 Chat ID: ").strip()
    return config

def get_monitoring_config():
    """获取监控配置"""
    print("\n📊 配置监控参数")
    print("-" * 30)
    
    print("请输入节点名称（用逗号分隔）:")
    print("示例: loud sleek bat, knobby leaping kangaroo")
    names = input("节点名称: ").strip().split(",")
    config = {}
    config["PEER_NAMES"] = [name.strip() for name in names if name.strip()]
    
    return config

def save_config(config):
    """保存配置"""
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    print(f"✅ 配置已保存到 config.json")

def main():
    print_banner()
    
    # 检查 Python 版本
    if sys.version_info < (3, 7):
        print("❌ 需要 Python 3.7 或更高版本")
        sys.exit(1)
    
    # 检查依赖
    try:
        import requests
    except ImportError:
        print("📦 安装依赖...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # 显示设置指南
    print_telegram_guide()
    
    # 获取配置
    telegram_config = get_telegram_config()
    monitoring_config = get_monitoring_config()
    
    # 合并配置
    config = {**telegram_config, **monitoring_config}
    
    # 保存配置
    save_config(config)
    
    print("\n🎉 设置完成！")
    print("\n下一步：")
    print("运行: python main.py")
    print("然后按回车键查询节点状态")

if __name__ == "__main__":
    main() 