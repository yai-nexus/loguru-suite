#!/usr/bin/env python3
"""
插件系统测试示例

演示如何使用 yai-loguru 的插件系统。
"""

import os
import asyncio
from pathlib import Path
from loguru import logger
from yai_loguru import PluginManager


def test_file_sink_plugin():
    """测试文件日志插件"""
    print("=== 测试文件日志插件 ===")
    
    # 创建插件管理器
    manager = PluginManager()
    
    # 列出可用插件
    available_plugins = manager.list_available_plugins()
    print(f"可用插件: {list(available_plugins.keys())}")
    
    # 配置文件日志插件
    logs_dir = Path("../../logs")
    logs_dir.mkdir(exist_ok=True)
    
    config = {
        "file_path": str(logs_dir / "plugin_test.log"),
        "level": "INFO",
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {message}",
        "rotation": "1 MB",
        "retention": "3 days"
    }
    
    # 加载插件
    success = manager.load_plugin("file_sink", config)
    if success:
        print("✅ 文件日志插件加载成功")
        
        # 测试日志输出
        logger.info("这是一条测试日志")
        logger.warning("这是一条警告日志", extra_data="test_value")
        logger.error("这是一条错误日志")
        
        # 列出已加载的插件
        loaded_plugins = manager.list_loaded_plugins()
        print(f"已加载插件: {list(loaded_plugins.keys())}")
        
        print(f"✅ 日志已写入: {config['file_path']}")
        
        # 清理插件
        manager.cleanup_all()
        print("✅ 插件清理完成")
    else:
        print("❌ 文件日志插件加载失败")


def test_multiple_plugins():
    """测试多个插件同时使用"""
    print("\n=== 测试多个插件配置 ===")
    
    manager = PluginManager()
    
    # 批量配置多个插件
    logs_dir = Path("../../logs")
    
    plugins_config = {
        "file_sink": {
            "file_path": str(logs_dir / "multi_test.log"),
            "level": "DEBUG",
            "format": "{time} | {level} | {message}"
        }
        # 这里可以添加更多插件配置
        # "sentry": {...},
        # "datadog": {...}
    }
    
    # 批量设置插件
    manager.setup_plugins(plugins_config)
    
    # 测试日志
    logger.debug("调试日志")
    logger.info("信息日志")
    logger.warning("警告日志")
    
    print("✅ 多插件配置测试完成")
    
    # 清理
    manager.cleanup_all()


if __name__ == "__main__":
    print("启动插件系统测试...")
    
    # 基本的控制台日志配置
    logger.remove()  # 移除默认处理器
    logger.add(
        lambda msg: print(msg, end=""),
        format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan> | {message}",
        level="DEBUG"
    )
    
    try:
        test_file_sink_plugin()
        test_multiple_plugins()
        print("\n🎉 所有测试完成！")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()