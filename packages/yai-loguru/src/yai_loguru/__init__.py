"""
YAI Loguru Support

A collection of Loguru sinks for integrating with third-party cloud logging services.

This package provides a plugin-based architecture for extending Loguru with
various cloud logging services and custom sinks.

Core Components:
- PluginManager: Manages loading and configuration of plugins
- LoguruPlugin: Base class for creating custom plugins

Available Plugins (install separately):
- yai-loguru-file-sink: File-based logging with rotation
- yai-loguru-sls-sink: Aliyun SLS integration
- More plugins coming soon...

Example:
    from yai_loguru import PluginManager
    from loguru import logger
    
    # Initialize plugin manager
    manager = PluginManager()
    
    # Load and configure a plugin
    config = {"file_path": "/tmp/app.log", "level": "INFO"}
    if manager.load_plugin("file_sink", config):
        logger.info("Plugin loaded successfully")
        
        # Your application logging
        logger.info("This will be handled by the plugin")
        
        # Cleanup when done
        manager.cleanup_all()

For more information and examples, visit:
https://github.com/yai-nexus/yai-nexus-agentkit
"""

from typing import Dict, Type
from .manager import PluginManager
from .plugin import LoguruPlugin

__version__ = "0.3.7"
__all__ = [
    "PluginManager",
    "LoguruPlugin",
]

# Plugin discovery and validation
def list_available_plugins() -> Dict[str, Type[LoguruPlugin]]:
    """List all available plugins in the current environment."""
    manager = PluginManager()
    return manager.list_available_plugins()

def validate_plugin(plugin_name: str) -> bool:
    """Validate if a plugin can be loaded."""
    manager = PluginManager()
    available_plugins = manager.discover_plugins()
    return plugin_name in available_plugins