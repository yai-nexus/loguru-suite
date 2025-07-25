"""
yai-loguru-sinks 使用示例

展示如何使用新的 sink 工厂模式替代传统插件系统。
专注于阿里云 SLS 支持。
"""

import os
from loguru import logger

# 方式一：配置驱动（推荐）
def config_driven_example():
    """配置驱动的使用方式"""
    from yai_loguru_sinks import setup_extended_config, create_config_from_file
    
    # 设置环境变量（实际使用中应该在环境中设置）
    os.environ.update({
        'SLS_ACCESS_KEY_ID': 'your-access-key-id',
        'SLS_ACCESS_KEY_SECRET': 'your-access-key-secret',
    })
    
    # 注册企业级协议解析器
    setup_extended_config()
    
    # 从配置文件加载
    config = create_config_from_file('configs/logging.yaml')
    
    # 现在可以直接使用 logger
    logger.info("这是一条信息日志")
    logger.warning("这是一条警告日志")
    logger.error("这是一条错误日志")


# 方式二：直接使用 sink 工厂
def direct_sink_example():
    """直接使用 sink 工厂的方式"""
    from yai_loguru_sinks import create_sls_sink
    
    # 创建 SLS sink
    sls_sink = create_sls_sink(
        project="my-project",
        logstore="my-logstore", 
        region="cn-hangzhou",
        access_key_id="your-access-key-id",
        access_key_secret="your-access-key-secret",
        topic="python-app",
        batch_size=50,
        flush_interval=5.0
    )
    
    # 添加到 logger
    logger.add(sls_sink, level="WARNING")
    
    # 添加本地文件 sink（Loguru 原生）
    logger.add(
        "logs/app.log",
        level="INFO",
        rotation="1 day",
        retention="30 days",
        compression="gz"
    )
    
    # 使用 logger
    logger.info("这条日志只会写入本地文件")
    logger.warning("这条日志会同时写入 SLS 和本地文件")
    logger.error("这条日志会同时写入 SLS 和本地文件")


# 方式三：混合使用
def hybrid_example():
    """混合使用配置文件和代码的方式"""
    from yai_loguru_sinks import setup_extended_config, create_config_from_file, create_sls_sink
    
    # 先从配置文件加载基础配置
    setup_extended_config()
    config = create_config_from_file('configs/logging.yaml')
    
    # 然后根据运行时条件添加额外的 sink
    if os.getenv('ENABLE_EXTRA_SLS') == 'true':
        extra_sls_sink = create_sls_sink(
            project="extra-project",
            logstore="extra-logstore",
            region="cn-beijing",
            topic="extra-logs"
        )
        logger.add(extra_sls_sink, level="ERROR")
    
    # 使用 logger
    logger.info("混合配置示例")


# 方式四：对比传统插件系统
def compare_with_old_plugin_system():
    """对比新旧系统的差异"""
    
    print("=== 传统插件系统（已废弃）===")
    print("""
    # 复杂的插件配置
    from yai_loguru import PluginManager
    from yai_loguru_sls_sink import SlsSinkPlugin
    
    manager = PluginManager()
    manager.register_plugin('sls', SlsSinkPlugin())
    manager.setup_plugin('sls', {
        'endpoint': 'https://cn-hangzhou.log.aliyuncs.com',
        'access_key_id': 'xxx',
        'access_key': 'xxx',
        'project': 'my-project',
        'logstore': 'my-logstore',
        'level': 'WARNING'
    })
    """)
    
    print("\n=== 新的 Sink 工厂系统 ===")
    print("""
    # 简洁的配置驱动
    from yai_loguru_sinks import setup_extended_config
    from loguru_config import LoguruConfig
    
    setup_extended_config()
    config = LoguruConfig()
    config.load('logging.yaml')
    
    # 配置文件中：
    # handlers:
    #   - sink: sls://my-project/my-logstore?region=cn-hangzhou
    #     level: WARNING
    """)
    
    print("\n优势对比：")
    print("✅ 移除了复杂的插件抽象层")
    print("✅ 统一的配置文件格式")
    print("✅ 利用 loguru-config 的成熟生态")
    print("✅ 更好的类型安全和错误处理")
    print("✅ 支持环境变量和动态配置")
    print("✅ 专注于核心功能，避免过度设计")


# 方式五：多环境配置示例
def multi_environment_example():
    """多环境配置示例"""
    from yai_loguru_sinks import setup_extended_config, create_config_from_file
    
    # 根据环境变量选择配置文件
    env = os.getenv('ENVIRONMENT', 'development')
    config_file = f'configs/logging-{env}.yaml'
    
    # 如果环境特定配置不存在，使用默认配置
    if not os.path.exists(config_file):
        config_file = 'configs/logging.yaml'
    
    setup_extended_config()
    config = create_config_from_file(config_file)
    
    logger.info(f"使用 {env} 环境配置")


if __name__ == "__main__":
    print("yai-loguru-sinks 使用示例")
    print("=" * 50)
    
    # 创建日志目录
    os.makedirs("logs", exist_ok=True)
    
    try:
        print("\n1. 配置驱动示例")
        config_driven_example()
        
        print("\n2. 直接使用 sink 工厂示例")
        direct_sink_example()
        
        print("\n3. 混合使用示例")
        hybrid_example()
        
        print("\n4. 对比传统插件系统")
        compare_with_old_plugin_system()
        
        print("\n5. 多环境配置示例")
        multi_environment_example()
        
    except ImportError as e:
        print(f"依赖缺失: {e}")
        print("请安装必要的依赖：")
        print("uv add loguru-config aliyun-log-python-sdk")
    except Exception as e:
        print(f"示例运行错误: {e}")
    
    print("\n示例运行完成！")