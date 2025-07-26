"""
yai-loguru-sinks 使用示例主程序

展示如何使用新的 sink 工厂模式替代传统插件系统。
专注于阿里云 SLS 支持。
"""

import os
from examples import (
    config_driven_example,
    direct_sink_example,
    hybrid_example,
    compare_with_old_plugin_system,
    multi_environment_example,
)


def main():
    """主程序入口"""
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


if __name__ == "__main__":
    main()