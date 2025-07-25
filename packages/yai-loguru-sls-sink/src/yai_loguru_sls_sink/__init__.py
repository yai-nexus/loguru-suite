"""
YAI Loguru SLS Sink Plugin

A plugin that provides Aliyun SLS (Simple Log Service) integration for yai-loguru.
"""

from .plugin import SlsSinkPlugin  # type: ignore

__version__ = "0.1.0"
__all__ = ["SlsSinkPlugin"]