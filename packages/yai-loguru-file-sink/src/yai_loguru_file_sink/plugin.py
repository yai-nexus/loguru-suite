"""
文件日志插件实现

一个用于文件日志输出的插件，支持多种文件策略和配置选项。
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger
from yai_loguru.plugin import LoguruPlugin


class FileSinkPlugin(LoguruPlugin):
    """文件日志插件
    
    支持的配置选项：
    - file_path: 日志文件路径
    - level: 日志级别 (默认: INFO)
    - format: 日志格式 (可选)
    - rotation: 文件轮转配置 (可选)
    - retention: 文件保留配置 (可选)
    - compression: 压缩配置 (可选)
    - encoding: 文件编码 (默认: utf-8)
    - ensure_dir: 是否自动创建目录 (默认: True)
    """
    
    def __init__(self):
        self.sink_id: Optional[int] = None
    
    def setup(self, config: Dict[str, Any]) -> None:
        """设置文件日志插件"""
        # 验证必需的配置
        if "file_path" not in config:
            raise ValueError("FileSinkPlugin 需要 'file_path' 配置")
        
        file_path = config["file_path"]
        
        # 确保目录存在
        if config.get("ensure_dir", True):
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        # 构建loguru配置
        sink_config = {
            "sink": file_path,
            "level": config.get("level", "INFO"),
            "encoding": config.get("encoding", "utf-8"),
        }
        
        # 可选配置
        if "format" in config:
            sink_config["format"] = config["format"]
        if "rotation" in config:
            sink_config["rotation"] = config["rotation"]
        if "retention" in config:
            sink_config["retention"] = config["retention"]
        if "compression" in config:
            sink_config["compression"] = config["compression"]
        
        # 添加到loguru
        self.sink_id = logger.add(**sink_config)
        
        logger.info(f"FileSinkPlugin 已启用，日志文件: {file_path}")
    
    def cleanup(self) -> None:
        """清理插件资源"""
        if self.sink_id is not None:
            logger.remove(self.sink_id)
            self.sink_id = None