"""loguru-config 扩展配置

注册企业级 sink 协议解析器，目前专注于阿里云 SLS 支持。
"""

import re
from typing import Any, Dict
from loguru_config import LoguruConfig

from .sls import parse_sls_url, create_sls_sink


def sls_protocol_parser(url: str) -> Any:
    """SLS 协议解析器
    
    解析 sls:// URL 并创建对应的 sink 函数
    
    Args:
        url: SLS URL，格式如 sls://project/logstore?region=cn-hangzhou&topic=app
        
    Returns:
        可调用的 sink 函数
    """
    config = parse_sls_url(url)
    return create_sls_sink(**config)


def setup_extended_config() -> None:
    """注册企业级 sink 协议解析器
    
    将 SLS 协议解析器注册到 loguru-config，
    使其能够解析配置文件中的 sls:// URL。
    """
    # 创建 SLS 协议正则表达式
    sls_protocol = re.compile(r'^sls://(.+)$')
    
    # 注册 SLS 协议解析器
    LoguruConfig.supported_protocol_parsers = list(LoguruConfig.supported_protocol_parsers) + [
        (sls_protocol, lambda match: sls_protocol_parser(match.group(0)))
    ]


def create_config_from_dict(config_dict: Dict[str, Any]) -> LoguruConfig:
    """从字典创建 LoguruConfig
    
    Args:
        config_dict: 配置字典
        
    Returns:
        配置好的 LoguruConfig 实例
    """
    config = LoguruConfig()
    config.load(config_dict)
    return config


def create_config_from_file(config_file: str) -> LoguruConfig:
    """从文件创建 LoguruConfig
    
    Args:
        config_file: 配置文件路径
        
    Returns:
        配置好的 LoguruConfig 实例
    """
    config = LoguruConfig()
    config.load(config_file)
    return config