"""
阿里云 SLS (Simple Log Service) 插件

提供将日志发送到阿里云 SLS 的功能。
"""

import os
import json
import time
import threading
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from queue import Queue, Empty

from yai_loguru.plugin import LoguruPlugin
from loguru import logger

try:
    from aliyun.log import LogClient  # type: ignore
    from aliyun.log.logitem import LogItem  # type: ignore
    from aliyun.log.putlogsrequest import PutLogsRequest  # type: ignore
    HAS_ALIYUN_SDK = True
except ImportError:
    HAS_ALIYUN_SDK = False
    LogClient = None
    LogItem = None
    PutLogsRequest = None


@dataclass
class SlsConfig:
    """Configuration for Aliyun SLS sink."""
    
    # SLS 连接配置
    endpoint: str = ""
    access_key_id: str = ""
    access_key: str = ""
    project: str = ""
    logstore: str = ""
    
    # SLS 特定配置
    topic: str = "python-app"
    source: str = "yai-loguru"
    
    # 批量发送配置
    batch_size: int = 100
    flush_interval: float = 5.0
    max_retries: int = 3
    timeout: float = 30.0
    
    # 其他配置
    compress: bool = True
    level: str = "INFO"
    format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
    
    def __post_init__(self):
        """从环境变量加载配置"""
        if not self.endpoint:
            self.endpoint = os.getenv("SLS_ENDPOINT", "")
        if not self.access_key_id:
            self.access_key_id = os.getenv("SLS_AK_ID", "")
        if not self.access_key:
            self.access_key = os.getenv("SLS_AK_KEY", "")
        if not self.project:
            self.project = os.getenv("SLS_PROJECT", "")
        if not self.logstore:
            self.logstore = os.getenv("SLS_LOGSTORE", "")
        if not self.topic or self.topic == "python-app":
            self.topic = os.getenv("SLS_TOPIC", "python-app")
        if not self.source or self.source == "yai-loguru":
            self.source = os.getenv("SLS_SOURCE", "yai-loguru")


class SlsSinkPlugin(LoguruPlugin):
    """Aliyun SLS sink plugin for yai-loguru."""
    
    def __init__(self):
        super().__init__()
        self.config: Optional[SlsConfig] = None
        self.client: Optional[LogClient] = None
        self.sink_id: Optional[int] = None
        self.log_queue: Optional[Queue] = None
        self.stop_event: Optional[threading.Event] = None
        self.flush_thread: Optional[threading.Thread] = None
        
    def setup(self, config: Dict[str, Any]) -> None:
        """设置 SLS 插件。
        
        Args:
            config: 插件配置字典
        """
        if not HAS_ALIYUN_SDK:
            logger.error("阿里云 SDK 未安装，请运行: pip install aliyun-log-python-sdk")
            raise ImportError("Missing aliyun-log-python-sdk dependency")
        
        # 解析配置
        self.config = SlsConfig(**config)
        
        # 验证必需的配置
        required_fields = ['endpoint', 'access_key_id', 'access_key', 'project', 'logstore']
        missing_fields = [field for field in required_fields if not getattr(self.config, field)]
        
        if missing_fields:
            logger.error(f"SLS配置缺少必需字段: {missing_fields}")
            raise ValueError(f"Missing required SLS configuration fields: {missing_fields}")
        
        # 初始化SLS客户端
        self.client = LogClient(
            self.config.endpoint,
            self.config.access_key_id,
            self.config.access_key
        )
        
        # 初始化日志队列和处理线程
        self.log_queue = Queue()
        self.stop_event = threading.Event()
        self.flush_thread = threading.Thread(target=self._flush_worker, daemon=True)
        self.flush_thread.start()
        
        # 添加loguru sink
        self.sink_id = logger.add(
            self._log_handler,
            level=self.config.level,
            format=self.config.format,
            serialize=True
        )
        
        logger.info(f"SLS 插件已启用，目标: {self.config.project}/{self.config.logstore}")
    
    def cleanup(self) -> bool:
        """清理SLS插件"""
        try:
            # 停止刷新线程
            if self.stop_event:
                self.stop_event.set()
            
            if self.flush_thread and self.flush_thread.is_alive():
                self.flush_thread.join(timeout=5.0)
            
            # 发送剩余的日志
            if self.log_queue and not self.log_queue.empty():
                self._flush_messages()
            
            # 移除loguru sink
            if self.sink_id is not None:
                logger.remove(self.sink_id)
                self.sink_id = None
            
            logger.info("SLS 插件已清理")
            return True
            
        except Exception as e:
            logger.error(f"SLS 插件清理失败: {e}")
            return False
    
    def _log_handler(self, message):
        """处理日志消息"""
        try:
            if not self.log_queue:
                return
                
            # 格式化消息
            record = message.record
            
            # 添加到队列
            log_data = {
                'timestamp': record['time'].timestamp(),
                'level': record['level'].name,
                'message': str(record['message']),
                'module': record.get('name', ''),
                'function': record.get('function', ''),
                'line': record.get('line', 0),
            }
            
            self.log_queue.put(log_data)
                
        except Exception as e:
            # 避免日志处理错误影响主程序
            print(f"SLS日志处理错误: {e}")
    
    def _flush_worker(self):
        """后台线程工作函数，定期刷新日志"""
        messages = []
        
        while not self.stop_event.is_set():
            try:
                # 收集消息
                try:
                    # 等待消息或超时
                    message = self.log_queue.get(timeout=self.config.flush_interval)
                    messages.append(message)
                    
                    # 继续收集直到批量大小或队列为空
                    while len(messages) < self.config.batch_size:
                        try:
                            message = self.log_queue.get_nowait()
                            messages.append(message)
                        except Empty:
                            break
                            
                except Empty:
                    # 超时，如果有消息就发送
                    pass
                
                # 发送消息
                if messages:
                    self._send_messages(messages)
                    messages.clear()
                    
            except Exception as e:
                logger.error(f"SLS刷新工作线程错误: {e}")
                time.sleep(1)  # 避免错误循环
    
    def _flush_messages(self):
        """立即发送队列中的所有消息"""
        if not self.log_queue:
            return
            
        messages = []
        try:
            while not self.log_queue.empty():
                messages.append(self.log_queue.get_nowait())
        except Empty:
            pass
        
        if messages:
            self._send_messages(messages)
    
    def _send_messages(self, messages: List[Dict[str, Any]]):
        """发送消息到SLS"""
        if not messages or not self.client or not self.config:
            return
        
        try:
            # 转换为SLS LogItem格式
            log_items = []
            for msg in messages:
                log_item = LogItem()
                log_item.set_time(int(msg['timestamp']))
                log_item.set_contents([
                    ('level', msg['level']),
                    ('message', msg['message']),
                    ('module', msg['module']),
                    ('function', msg['function']),
                    ('line', str(msg['line'])),
                ])
                log_items.append(log_item)
            
            # 创建请求
            request = PutLogsRequest(
                project=self.config.project,
                logstore=self.config.logstore,
                topic=self.config.topic,
                source=self.config.source,
                logitems=log_items,
                compress=self.config.compress
            )
            
            # 发送到SLS
            response = self.client.put_logs(request)
            
            if response.is_success():
                logger.debug(f"成功发送 {len(log_items)} 条日志到SLS")
            else:
                logger.error(f"SLS发送失败: {response.get_error_message()}")
                
        except Exception as e:
            logger.error(f"SLS消息发送错误: {e}")