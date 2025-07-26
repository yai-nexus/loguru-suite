"""混合使用配置文件和代码的示例"""

import os
from loguru import logger


def hybrid_example():
    """混合使用配置文件和代码的方式"""
    from yai_loguru_sinks import register_protocol_parsers, create_config_from_file, create_sls_sink
    
    # 检查环境变量
    access_key_id = os.getenv('SLS_ACCESS_KEY_ID')
    access_key_secret = os.getenv('SLS_ACCESS_KEY_SECRET')
    
    if not access_key_id or not access_key_secret:
        print("⚠️  SLS 环境变量未设置，跳过混合示例")
        return
    
    # 先从配置文件加载基础配置
    register_protocol_parsers()
    config = create_config_from_file('configs/logging.yaml')
    print("✅ 已加载基础配置文件")
    
    # 然后根据运行时条件添加额外的 sink
    if os.getenv('ENABLE_EXTRA_SLS') == 'true':
        extra_sls_sink = create_sls_sink(
            project="extra-project",
            logstore="extra-logstore",
            region="cn-beijing",
            topic="extra-logs"
        )
        logger.add(extra_sls_sink, level="ERROR")
        print("✅ 已添加额外的 SLS sink")
    
    # 使用 logger
    logger.info("混合配置示例")
    print("✅ 混合使用示例完成")