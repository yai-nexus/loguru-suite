#!/usr/bin/env python3
"""
配置模块 - 环境变量和日志配置处理
"""

import os
import re
from pathlib import Path
from loguru import logger
from yai_loguru_sinks import register_protocol_parsers, create_config_from_file


def load_environment():
    """加载环境变量"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ 已加载 .env 文件")
    except ImportError:
        print("⚠️ 未安装 python-dotenv，跳过 .env 文件加载")


def setup_logging():
    """设置日志配置"""
    # 移除默认处理器
    logger.remove()
    
    # 注册协议解析器
    register_protocol_parsers()
    
    # 加载配置文件
    config_path = Path(__file__).parent.parent / "logging.yaml"
    create_config_from_file(str(config_path))
    
    logger.info("日志系统初始化完成")


def check_sls_config() -> bool:
    """检查 SLS 配置"""
    access_key_id = os.getenv('SLS_ACCESS_KEY_ID')
    access_key_secret = os.getenv('SLS_ACCESS_KEY_SECRET')
    
    if access_key_id and access_key_secret:
        print("✅ SLS 配置已就绪")
        logger.info("SLS 配置检查通过")
        return True
    else:
        print("⚠️ SLS 配置未完整，将仅使用本地日志")
        return False