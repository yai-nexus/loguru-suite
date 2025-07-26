"""直接使用 sink 工厂的示例"""

import os
from loguru import logger


def direct_sink_example():
    """直接使用 sink 工厂的方式"""
    from yai_loguru_sinks import create_sls_sink
    
    # 检查环境变量
    access_key_id = os.getenv('SLS_ACCESS_KEY_ID')
    access_key_secret = os.getenv('SLS_ACCESS_KEY_SECRET')
    project = os.getenv('SLS_PROJECT', 'yai-log-test')
    logstore = os.getenv('SLS_LOGSTORE', 'app-log')
    region = os.getenv('SLS_DEFAULT_REGION', 'cn-beijing')
    
    if not access_key_id or not access_key_secret:
        print("⚠️  SLS 环境变量未设置，跳过 SLS sink 创建")
    else:
        # 创建 SLS sink
        sls_sink = create_sls_sink(
            project=project,
            logstore=logstore, 
            region=region,
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            topic="python-app",
            batch_size=50,
            flush_interval=5.0
        )
        
        # 添加到 logger
        logger.add(sls_sink, level="WARNING")
        print(f"✅ 已添加 SLS sink: {project}/{logstore}")
    
    # 添加本地文件 sink（Loguru 原生）
    logger.add(
        "logs/app.log",
        level="INFO",
        rotation="1 day",
        retention="30 days",
        compression="gz"
    )
    print("✅ 已添加本地文件 sink: logs/app.log")
    
    # 使用 logger
    logger.info("这条日志只会写入本地文件")
    logger.warning("这条日志会同时写入 SLS 和本地文件")
    logger.error("这条日志会同时写入 SLS 和本地文件")
    
    print("✅ 直接使用 sink 工厂示例完成")