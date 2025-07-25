#!/usr/bin/env python3
"""
yai-loguru 插件系统示例

这个示例展示了如何使用 yai-loguru 的插件系统来管理日志输出。
"""

import os
import tempfile
from pathlib import Path
from loguru import logger
from yai_loguru import PluginManager

def main():
    """主函数"""
    print("🚀 yai-loguru 插件系统示例")
    print("=" * 50)
    
    # 创建临时目录用于日志文件
    with tempfile.TemporaryDirectory() as temp_dir:
        log_dir = Path(temp_dir)
        
        # 初始化插件管理器
        manager = PluginManager()
        
        # 显示可用插件
        available_plugins = manager.list_available_plugins()
        print(f"📦 可用插件: {list(available_plugins.keys())}")
        print()
        
        # 配置多个文件日志插件
        configs = {
            "app_log": {
                "file_path": str(log_dir / "app.log"),
                "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
                "rotation": "1 MB",
                "retention": "7 days",
                "compression": "zip"
            },
            "error_log": {
                "file_path": str(log_dir / "error.log"),
                "format": "{time} | {level} | {message}",
                "level": "ERROR"
            },
            "debug_log": {
                "file_path": str(log_dir / "debug.log"),
                "format": "{time} | {level} | {file}:{line} | {message}",
                "level": "DEBUG"
            }
        }
        
        # 批量加载插件
        print("🔧 配置日志插件...")
        for name, config in configs.items():
            success = manager.load_plugin("file_sink", config)
            if success:
                print(f"✅ {name} 配置成功")
            else:
                print(f"❌ {name} 配置失败")
        
        print()
        
        # 显示已加载的插件
        loaded_plugins = manager.list_loaded_plugins()
        print(f"🔌 已加载插件数量: {len(loaded_plugins)}")
        print()
        
        # 测试不同级别的日志
        print("📝 测试日志输出...")
        logger.debug("这是一条调试信息")
        logger.info("应用启动成功")
        logger.warning("这是一个警告")
        logger.error("发生了一个错误")
        logger.critical("这是一个严重错误")
        
        print()
        
        # 模拟一些应用日志
        for i in range(5):
            logger.info(f"处理任务 #{i+1}")
            if i == 2:
                logger.warning(f"任务 #{i+1} 处理缓慢")
            if i == 4:
                logger.error(f"任务 #{i+1} 处理失败")
        
        # 清理所有插件
        print("🧹 清理插件...")
        manager.cleanup_all()
        
        # 检查生成的日志文件
        print("\n📁 生成的日志文件:")
        for log_file in log_dir.glob("*.log"):
            size = log_file.stat().st_size
            print(f"  📄 {log_file.name} ({size} bytes)")
            
            # 显示文件内容的前几行
            try:
                content = log_file.read_text()
                lines = content.strip().split('\n')
                print(f"     内容预览 (共 {len(lines)} 行):")
                for line in lines[:3]:  # 只显示前3行
                    print(f"     {line}")
                if len(lines) > 3:
                    print(f"     ... 还有 {len(lines) - 3} 行")
                print()
            except Exception as e:
                print(f"     读取失败: {e}")
    
    print("🎉 示例完成！")

if __name__ == "__main__":
    main()