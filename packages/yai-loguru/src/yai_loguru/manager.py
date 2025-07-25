"""
插件管理器

负责发现、加载和管理 yai-loguru 插件。
"""

import importlib.metadata
from typing import Dict, Type, Any, Optional
from loguru import logger

from .plugin import LoguruPlugin


class PluginManager:
    """负责发现、加载和管理插件。"""

    def __init__(self):
        self.plugins: Dict[str, LoguruPlugin] = {}
        self.loaded_plugins: Dict[str, LoguruPlugin] = {}

    def discover_plugins(self) -> Dict[str, Type[LoguruPlugin]]:
        """发现所有通过 entry points 声明的插件。
        
        Returns:
            Dict[str, Type[LoguruPlugin]]: 发现的插件类字典
        """
        discovered = {}
        try:
            entry_points = importlib.metadata.entry_points(group='yai_loguru.plugins')
            for entry_point in entry_points:
                try:
                    plugin_class: Type[LoguruPlugin] = entry_point.load()
                    discovered[entry_point.name] = plugin_class
                    logger.debug(f"发现插件: {entry_point.name}")
                except Exception as e:
                    logger.error(f"加载插件 {entry_point.name} 失败: {e}")
        except Exception as e:
            logger.error(f"发现插件失败: {e}")
        
        return discovered

    def load_plugin(self, plugin_name: str, config: Dict[str, Any]) -> bool:
        """加载并配置单个插件。
        
        Args:
            plugin_name: 插件名称
            config: 插件配置
            
        Returns:
            bool: 是否成功加载
        """
        try:
            # 如果插件已经加载，先清理
            if plugin_name in self.loaded_plugins:
                self.unload_plugin(plugin_name)
            
            # 发现可用插件
            available_plugins = self.discover_plugins()
            
            if plugin_name not in available_plugins:
                logger.error(f"插件 '{plugin_name}' 未找到")
                return False
            
            # 实例化插件
            plugin_class = available_plugins[plugin_name]
            plugin_instance = plugin_class()
            
            # 配置插件
            plugin_instance.setup(config)
            
            # 记录已加载的插件
            self.loaded_plugins[plugin_name] = plugin_instance
            
            logger.info(f"插件 '{plugin_name}' 加载成功")
            return True
            
        except Exception as e:
            logger.error(f"加载插件 '{plugin_name}' 失败: {e}")
            return False

    def unload_plugin(self, plugin_name: str) -> bool:
        """卸载插件。
        
        Args:
            plugin_name: 插件名称
            
        Returns:
            bool: 是否成功卸载
        """
        if plugin_name not in self.loaded_plugins:
            logger.warning(f"插件 '{plugin_name}' 未加载")
            return False
        
        try:
            plugin = self.loaded_plugins[plugin_name]
            
            # 如果插件有清理方法，调用它
            if hasattr(plugin, 'cleanup'):
                plugin.cleanup()
            
            # 从已加载列表中移除
            del self.loaded_plugins[plugin_name]
            
            logger.info(f"插件 '{plugin_name}' 卸载成功")
            return True
            
        except Exception as e:
            logger.error(f"卸载插件 '{plugin_name}' 失败: {e}")
            return False

    def setup_plugins(self, config: Dict[str, Dict[str, Any]]) -> None:
        """根据配置批量设置插件。
        
        Args:
            config: 插件配置字典，格式为 {plugin_name: plugin_config}
        """
        for plugin_name, plugin_config in config.items():
            self.load_plugin(plugin_name, plugin_config)

    def list_available_plugins(self) -> Dict[str, Type[LoguruPlugin]]:
        """列出所有可用的插件。
        
        Returns:
            Dict[str, Type[LoguruPlugin]]: 可用插件字典
        """
        return self.discover_plugins()

    def list_loaded_plugins(self) -> Dict[str, LoguruPlugin]:
        """列出所有已加载的插件。
        
        Returns:
            Dict[str, LoguruPlugin]: 已加载插件字典
        """
        return self.loaded_plugins.copy()

    def cleanup_all(self) -> None:
        """清理所有已加载的插件。"""
        plugin_names = list(self.loaded_plugins.keys())
        for plugin_name in plugin_names:
            self.unload_plugin(plugin_name)