"""配置驱动的使用方式示例"""

import os
from loguru import logger


def config_driven_example():
    """配置驱动的使用方式"""
    from yai_loguru_sinks import register_protocol_parsers, create_config_from_file
    
    # 加载 .env 文件（如果存在）
    try:
        from dotenv import load_dotenv
        load_dotenv('../.env')  # 加载根目录的 .env 文件
        print("✅ 已加载 .env 文件")
    except ImportError:
        print("⚠️  python-dotenv 未安装，跳过 .env 文件加载")
    
    # 检查环境变量
    access_key_id = os.getenv('SLS_ACCESS_KEY_ID')
    access_key_secret = os.getenv('SLS_ACCESS_KEY_SECRET')
    
    if not access_key_id or not access_key_secret:
        print("⚠️  SLS 环境变量未设置，使用模拟模式")
        return
    
    print(f"✅ 使用 SLS 配置: {access_key_id[:8]}...")
    
    # 注册企业级协议解析器
    register_protocol_parsers()
    
    # 从配置文件加载
    config = create_config_from_file('configs/logging.yaml')
    
    # 现在可以直接使用 logger
    logger.info("这是一条信息日志")
    logger.warning("这是一条警告日志")
    logger.error("这是一条错误日志")
    
    print("✅ 配置驱动示例完成")