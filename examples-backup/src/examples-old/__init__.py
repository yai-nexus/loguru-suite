"""
yai-loguru-sinks 使用示例模块

展示如何使用新的 sink 工厂模式替代传统插件系统。
专注于阿里云 SLS 支持。
"""

from .config_driven import config_driven_example
from .direct_sink import direct_sink_example
from .hybrid_usage import hybrid_example
from .comparison import compare_with_old_plugin_system
from .multi_environment import multi_environment_example

__all__ = [
    "config_driven_example",
    "direct_sink_example", 
    "hybrid_example",
    "compare_with_old_plugin_system",
    "multi_environment_example",
]