#!/usr/bin/env python3
"""
Basic Demo - 极简的 yai-loguru-sinks 使用示例

这个示例展示了如何使用 yai-loguru-sinks 进行最基本的日志记录。
"""

import os
from pathlib import Path
from loguru import logger
from yai_loguru_sinks import register_protocol_parsers, create_config_from_file


def main():
    """主函数 - 演示基本的日志记录功能"""
    print("🚀 Basic Demo - yai-loguru-sinks 基础使用示例")
    print("=" * 50)
    
    # 注册协议解析器
    register_protocol_parsers()
    
    # 加载日志配置
    config_path = Path(__file__).parent / "logging.yaml"
    create_config_from_file(str(config_path))
    
    # 基本日志记录示例
    logger.info("✅ 日志系统初始化完成")
    logger.debug("🔍 这是一条调试信息")
    logger.info("📝 这是一条普通信息")
    logger.warning("⚠️ 这是一条警告信息")
    logger.error("❌ 这是一条错误信息")
    
    # 结构化日志示例
    user_data = {
        "user_id": 12345,
        "username": "demo_user",
        "action": "login"
    }
    logger.info("👤 用户操作记录", extra=user_data)
    
    # 异常日志示例
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        logger.exception("💥 捕获到异常")
    
    print("\n✨ 示例运行完成！请查看 logs/ 目录下的日志文件。")


if __name__ == "__main__":
    main()