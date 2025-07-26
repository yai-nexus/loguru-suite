"""多环境配置示例"""

import os
from loguru import logger


def multi_environment_example():
    """多环境配置示例"""
    from yai_loguru_sinks import register_protocol_parsers, create_config_from_file
    
    # 检查环境变量
    access_key_id = os.getenv('SLS_ACCESS_KEY_ID')
    access_key_secret = os.getenv('SLS_ACCESS_KEY_SECRET')
    
    if not access_key_id or not access_key_secret:
        print("⚠️  SLS 环境变量未设置，跳过多环境示例")
        return
    
    # 根据环境变量选择配置文件
    env = os.getenv('ENVIRONMENT', 'development')
    config_file = f'configs/logging-{env}.yaml'
    
    # 如果环境特定配置不存在，使用默认配置
    if not os.path.exists(config_file):
        config_file = 'configs/logging.yaml'
        print(f"✅ 使用默认配置文件: {config_file}")
    else:
        print(f"✅ 使用环境特定配置文件: {config_file}")
    
    register_protocol_parsers()
    config = create_config_from_file(config_file)
    
    logger.info(f"使用 {env} 环境配置")
    print("✅ 多环境配置示例完成")