#!/usr/bin/env python3
"""
yai-loguru 简单使用示例

演示如何使用 yai-loguru 核心库进行基本的日志配置和输出。
这个示例不涉及插件系统，展示最简单的使用方式。
"""

import time
from pathlib import Path
from loguru import logger
from yai_loguru import PluginManager


def main():
    """主函数 - 演示 yai-loguru 核心库的基本使用"""
    
    print("🚀 yai-loguru 简单使用示例")
    print("=" * 40)
    
    # 确保日志目录存在
    logs_dir = Path("../../logs")
    logs_dir.mkdir(exist_ok=True)
    
    # 1. 初始化插件管理器（但不加载任何插件）
    print("\n📦 初始化 yai-loguru 核心库...")
    manager = PluginManager()
    print(f"✅ 插件管理器已初始化，发现 {len(manager.discover_plugins())} 个可用插件")
    
    # 2. 配置基本的 loguru 日志输出
    print("\n📝 配置基本日志输出...")
    
    # 移除默认的控制台输出
    logger.remove()
    
    # 添加彩色控制台输出
    logger.add(
        sink=lambda msg: print(msg, end=""),
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="DEBUG",
        colorize=True
    )
    
    # 添加文件输出（按日期轮转）
    logger.add(
        sink=logs_dir / "simple-app_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="00:00",  # 每天午夜轮转
        retention="7 days",  # 保留7天
        compression="zip"  # 压缩旧文件
    )
    
    logger.info("应用启动", extra={"service": "simple-app", "manager": "yai-loguru"})
    
    # 3. 基本日志输出
    print("\n📝 测试基本日志输出...")
    logger.debug("这是调试信息")
    logger.info("这是普通信息")
    logger.warning("这是警告信息")
    logger.error("这是错误信息")
    logger.critical("这是严重错误")
    
    # 4. 带上下文的日志
    print("\n🏷️ 测试带上下文的日志...")
    logger.bind(user_id="user123", request_id="req456").info("用户登录成功")
    logger.bind(operation="data_process").warning("数据处理耗时较长")
    
    # 5. 结构化日志
    print("\n📊 测试结构化日志...")
    start_time = time.time()
    time.sleep(0.1)  # 模拟一些工作
    duration = time.time() - start_time
    
    logger.bind(
        task_name="demo_task",
        duration_ms=round(duration * 1000, 2),
        success=True,
        items_processed=100
    ).info("任务完成")
    
    # 6. 异常日志
    print("\n⚠️ 测试异常日志...")
    try:
        result = 1 / 0
    except ZeroDivisionError:
        logger.exception("捕获到除零异常")
    
    # 7. 不同模块的日志
    print("\n🔧 测试模块化日志...")
    auth_logger = logger.bind(module="auth")
    auth_logger.info("认证模块初始化")
    auth_logger.warning("认证令牌即将过期")
    
    db_logger = logger.bind(module="database")
    db_logger.info("数据库连接建立")
    db_logger.error("数据库查询超时")
    
    # 8. 自定义格式的日志
    print("\n🎨 测试自定义格式...")
    
    # 添加一个 JSON 格式的文件输出
    logger.add(
        sink=logs_dir / "simple-app-json_{time:YYYY-MM-DD}.log",
        format="{time} | {level} | {message}",
        level="INFO",
        serialize=True,  # JSON 格式
        rotation="100 MB"
    )
    
    logger.info("JSON 格式日志测试", extra={
        "event_type": "test",
        "metadata": {
            "version": "1.0.0",
            "environment": "development",
            "framework": "yai-loguru"
        }
    })
    
    # 9. 展示插件管理器的基本信息（不加载插件）
    print("\n🔌 yai-loguru 插件系统信息...")
    available_plugins = manager.discover_plugins()
    print(f"📋 发现可用插件: {list(available_plugins.keys())}")
    print("💡 提示: 要使用插件功能，请参考 plugin-usage 示例")
    
    print("\n✅ 示例完成！")
    print(f"📁 日志文件保存在: {logs_dir}")
    
    # 显示生成的日志文件
    log_files = list(logs_dir.glob("simple-app*.log*"))
    if log_files:
        print("\n📄 生成的日志文件:")
        for log_file in log_files:
            size = log_file.stat().st_size
            print(f"  • {log_file.name} ({size} bytes)")


if __name__ == "__main__":
    main()