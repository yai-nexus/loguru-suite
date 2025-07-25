#!/usr/bin/env python3
"""
yai-loguru 插件系统使用示例

演示如何使用 yai-loguru 的插件系统来扩展日志功能。
这个示例展示了插件的发现、加载、配置和使用。
"""

import time
import asyncio
from pathlib import Path
from loguru import logger
from yai_loguru import PluginManager


def main():
    """主函数 - 演示插件系统的完整使用流程"""
    
    print("🔌 yai-loguru 插件系统使用示例")
    print("=" * 50)
    
    # 确保日志目录存在
    logs_dir = Path("../../logs")
    logs_dir.mkdir(exist_ok=True)
    
    # 1. 初始化插件管理器
    print("\n📦 初始化插件管理器...")
    manager = PluginManager()
    
    # 2. 发现可用插件
    print("\n🔍 发现可用插件...")
    available_plugins = manager.discover_plugins()
    
    if available_plugins:
        print("发现的插件:")
        for plugin_name in available_plugins:
            print(f"  • {plugin_name}")
    else:
        print("❌ 未发现任何插件")
        print("请确保已安装插件包，例如:")
        print("  pip install yai-loguru-file-sink")
        print("  pip install yai-loguru-sls-sink")
        return
    
    # 3. 演示文件插件
    demo_file_plugin(manager, logs_dir)
    
    # 4. 演示 SLS 插件（如果可用）
    if "sls_sink" in available_plugins:
        demo_sls_plugin(manager)
    else:
        print("\n⚠️ SLS 插件未安装，跳过 SLS 演示")
    
    # 5. 演示插件配置和批量管理
    demo_plugin_management(manager, logs_dir)
    
    # 6. 清理所有插件
    print("\n🧹 清理所有插件...")
    manager.cleanup_all()
    print("✅ 所有插件已清理完成")


def demo_file_plugin(manager: PluginManager, logs_dir: Path):
    """演示文件插件的使用"""
    
    print("\n📁 演示文件插件...")
    
    # 配置文件插件
    file_config = {
        "file_path": str(logs_dir / "plugin-demo_{time:YYYY-MM-DD}.log"),
        "level": "INFO",
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        "rotation": "10 MB",
        "retention": "7 days",
        "compression": "zip"
    }
    
    # 加载文件插件
    if manager.load_plugin("file_sink", file_config):
        print("✅ 文件插件加载成功")
        
        # 测试日志输出
        logger.info("这是通过文件插件记录的日志")
        logger.warning("文件插件支持日志轮转", extra={"plugin": "file_sink"})
        logger.error("这是一个错误日志", extra={"error_code": 500})
        
        print(f"📄 日志已写入: {file_config['file_path']}")
    else:
        print("❌ 文件插件加载失败")


def demo_sls_plugin(manager: PluginManager):
    """演示 SLS 插件的使用"""
    
    print("\n☁️ 演示 SLS 插件...")
    
    # SLS 配置（使用测试配置）
    sls_config = {
        "endpoint": "test-endpoint.log.aliyuncs.com",
        "access_key_id": "test_access_key",
        "access_key": "test_secret",
        "project": "test_project",
        "logstore": "test_logstore",
        "topic": "plugin-demo",
        "source": "yai-loguru-example"
    }
    
    # 加载 SLS 插件
    if manager.load_plugin("sls_sink", sls_config):
        print("✅ SLS 插件加载成功")
        
        # 测试日志输出
        logger.info("这是通过 SLS 插件记录的日志")
        logger.bind(user_id="demo_user", action="test").info("带上下文的 SLS 日志")
        
        # 模拟一些业务操作
        start_time = time.time()
        time.sleep(0.1)
        duration = time.time() - start_time
        
        logger.bind(
            operation="demo_operation",
            duration_ms=round(duration * 1000, 2),
            success=True
        ).info("操作完成")
        
        print("📤 日志已发送到 SLS（注意：使用测试配置，实际不会发送）")
    else:
        print("❌ SLS 插件加载失败")


def demo_plugin_management(manager: PluginManager, logs_dir: Path):
    """演示插件的批量管理功能"""
    
    print("\n⚙️ 演示插件批量管理...")
    
    # 准备多个插件配置
    plugins_config = {
        "file_sink": {
            "file_path": str(logs_dir / "batch-demo_{time:YYYY-MM-DD}.log"),
            "level": "DEBUG",
            "format": "{time} | {level} | {message}",
        }
    }
    
    # 如果 SLS 插件可用，也加入配置
    available_plugins = manager.discover_plugins()
    if "sls_sink" in available_plugins:
        plugins_config["sls_sink"] = {
            "endpoint": "batch-test.log.aliyuncs.com",
            "access_key_id": "batch_test_key",
            "access_key": "batch_test_secret",
            "project": "batch_test_project",
            "logstore": "batch_test_logstore"
        }
    
    # 批量设置插件
    print(f"📋 批量配置 {len(plugins_config)} 个插件...")
    manager.setup_plugins(plugins_config)
    
    # 测试批量配置的插件
    logger.info("批量配置测试", extra={"test_type": "batch_setup"})
    logger.warning("多插件同时工作", extra={"plugin_count": len(plugins_config)})
    
    # 显示当前加载的插件
    loaded_plugins = list(manager.plugins.keys())
    print(f"✅ 当前已加载插件: {loaded_plugins}")
    
    # 演示插件验证
    print("\n🔍 验证插件状态...")
    for plugin_name in loaded_plugins:
        from yai_loguru import validate_plugin
        is_valid = validate_plugin(plugin_name)
        status = "✅ 有效" if is_valid else "❌ 无效"
        print(f"  • {plugin_name}: {status}")


def demo_advanced_features():
    """演示高级功能"""
    
    print("\n🚀 演示高级功能...")
    
    # 列出所有可用插件
    from yai_loguru import list_available_plugins
    available = list_available_plugins()
    
    print("📋 系统中所有可用插件:")
    for name, plugin_class in available.items():
        print(f"  • {name}: {plugin_class.__name__}")
    
    # 演示插件的动态加载和卸载
    manager = PluginManager()
    
    print("\n🔄 演示动态插件管理...")
    
    # 动态加载
    if "file_sink" in available:
        config = {"file_path": "/tmp/dynamic-test.log", "level": "INFO"}
        if manager.load_plugin("file_sink", config):
            print("✅ 动态加载文件插件成功")
            logger.info("动态加载测试")
            
            # 动态卸载
            manager.unload_plugin("file_sink")
            print("✅ 动态卸载文件插件成功")


if __name__ == "__main__":
    main()
    
    # 演示高级功能
    demo_advanced_features()