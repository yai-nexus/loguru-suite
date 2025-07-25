#!/usr/bin/env python3
"""
测试 SLS 插件是否能正常加载和工作
"""

import os
import tempfile
from yai_loguru import PluginManager
from loguru import logger

def test_sls_plugin():
    """测试 SLS 插件的基本功能"""
    print("=== 测试 SLS 插件 ===")
    
    # 初始化插件管理器
    manager = PluginManager()
    
    # 列出可用插件
    available_plugins = manager.list_available_plugins()
    print(f"可用插件: {list(available_plugins.keys())}")
    
    # 检查 SLS 插件是否可用
    if "sls_sink" not in available_plugins:
        print("❌ SLS 插件未找到")
        return False
    
    print("✅ SLS 插件已发现")
    
    # 配置 SLS 插件（使用测试配置）
    sls_config = {
        "endpoint": "cn-hangzhou.log.aliyuncs.com",
        "access_key_id": "test_key_id",
        "access_key": "test_key",
        "project": "test_project",
        "logstore": "test_logstore",
        "level": "INFO",
        "batch_size": 10,
        "flush_interval": 5.0
    }
    
    try:
        # 加载插件
        success = manager.load_plugin("sls_sink", sls_config)
        if success:
            print("✅ SLS 插件加载成功")
            
            # 列出已加载的插件
            loaded_plugins = manager.list_loaded_plugins()
            print(f"已加载插件: {list(loaded_plugins.keys())}")
            
            # 测试日志记录（注意：这会尝试连接到 SLS，可能会失败）
            print("📝 测试日志记录...")
            logger.info("这是一条测试日志消息")
            logger.warning("这是一条警告消息")
            logger.error("这是一条错误消息")
            
            print("✅ 日志记录完成")
            
            # 清理插件
            manager.cleanup_all()
            print("✅ 插件清理完成")
            
            return True
        else:
            print("❌ SLS 插件加载失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    success = test_sls_plugin()
    if success:
        print("\n🎉 SLS 插件测试成功！")
    else:
        print("\n💥 SLS 插件测试失败！")