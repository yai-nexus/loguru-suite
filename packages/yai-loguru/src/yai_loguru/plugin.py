from abc import ABC, abstractmethod

class LoguruPlugin(ABC):
    """所有插件的抽象基类。"""

    @abstractmethod
    def setup(self, config: dict) -> None:
        """根据提供的配置设置插件。"""
        pass