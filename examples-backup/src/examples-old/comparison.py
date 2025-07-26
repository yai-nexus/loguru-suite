"""对比新旧系统的差异示例"""


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
    from yai_loguru_sinks import register_protocol_parsers
    from loguru_config import LoguruConfig
    
    register_protocol_parsers()
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