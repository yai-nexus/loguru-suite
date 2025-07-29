# SLS 日志字段上报方案建议

## 当前 SLS 字段分析

根据提供的 SLS 结构化字段示例，当前系统包含以下 18 个显示字段：

### 基础字段（必需上报）

| 字段名 | 类型 | 说明 | 当前状态 | 建议 |
|--------|------|------|----------|------|
| `app_name` | text | 应用名称 | ❌ 未上报 | ✅ **需要添加** |
| `level` | text | 日志级别 | ✅ 已上报 | ✅ 保持 |
| `version` | text | 应用版本 | ❌ 未上报 | ✅ **需要添加** |
| `environment` | text | 运行环境 | ❌ 未上报 | ✅ **需要添加** |
| `hostname` | text | 主机名 | ❌ 未上报 | ✅ **需要添加** |
| `datetime` | text | 时间戳 | ✅ 已上报 (timestamp) | ✅ 保持 |
| `category` | text | 日志分类 | ❌ 未上报 | ✅ **需要添加** |
| `host_ip` | text | 主机IP | ❌ 未上报 | ✅ **需要添加** |
| `logger` | text | 日志记录器名称 | ✅ 已上报 (module) | ✅ 保持 |

### 业务字段（可选上报）

| 字段名 | 类型 | 说明 | 当前状态 | 建议 |
|--------|------|------|----------|------|
| `thread` | text | 线程信息 | ❌ 未上报 | 🔶 **可选添加** |
| `message` | text | 日志消息 | ✅ 已上报 | ✅ 保持 |

### 扩展字段（根据业务需要）

当前通过 `extra` 字段上报的业务数据，建议保持现有方式。

## 当前实现分析

### 已实现的字段映射

```python
# 当前 core.py 中的字段映射
log_data = {
    'timestamp': record['time'].timestamp(),     # ✅ 对应 datetime
    'level': record['level'].name,               # ✅ 对应 level  
    'message': str(record['message']),           # ✅ 对应 message
    'module': record.get('name', ''),            # ✅ 对应 logger
    'function': record.get('function', ''),      # ✅ 已有但未在SLS显示
    'line': record.get('line', 0),              # ✅ 已有但未在SLS显示
}
```

### 缺失的关键字段

1. **app_name** - 应用标识
2. **version** - 版本信息
3. **environment** - 环境标识
4. **hostname** - 主机名
5. **category** - 日志分类
6. **host_ip** - 主机IP
7. **thread** - 线程信息（可选）

## 实施方案

### 方案一：扩展 SlsConfig 配置（推荐）

**优点：** 配置灵活，支持环境变量，易于维护

#### 1. 修改 `data.py` 配置类

```python
@dataclass
class SlsConfig:
    # ... 现有配置 ...
    
    # 新增应用信息配置
    app_name: str = "unknown-app"
    app_version: str = "1.0.0"
    environment: str = "development"
    
    # 系统信息（可自动获取）
    auto_detect_hostname: bool = True
    auto_detect_host_ip: bool = True
    auto_detect_thread: bool = False
    
    # 日志分类配置
    default_category: str = "application"
```

#### 2. 修改 `core.py` 字段映射

```python
def __call__(self, message: Any) -> None:
    """Loguru sink 调用接口"""
    try:
        record = message.record
        
        # 基础字段映射
        log_data = {
            'timestamp': record['time'].timestamp(),
            'level': record['level'].name,
            'message': str(record['message']),
            'module': record.get('name', ''),
            'function': record.get('function', ''),
            'line': record.get('line', 0),
            
            # 新增必需字段
            'app_name': self.config.app_name,
            'version': self.config.app_version,
            'environment': self.config.environment,
            'category': self._get_log_category(record),
        }
        
        # 自动检测系统信息
        if self.config.auto_detect_hostname:
            log_data['hostname'] = self._get_hostname()
        
        if self.config.auto_detect_host_ip:
            log_data['host_ip'] = self._get_host_ip()
            
        if self.config.auto_detect_thread:
            log_data['thread'] = self._get_thread_info(record)
        
        # 处理 extra 字段
        record_extra = record.get('extra', {})
        if 'extra' in record_extra and record_extra['extra']:
            log_data['extra'] = record_extra['extra']
        
        self.log_queue.put(log_data)
```

#### 3. 添加辅助方法

```python
import socket
import threading
from typing import Dict, Any

class SlsSink:
    # ... 现有代码 ...
    
    def _get_hostname(self) -> str:
        """获取主机名"""
        try:
            return socket.gethostname()
        except Exception:
            return "unknown-host"
    
    def _get_host_ip(self) -> str:
        """获取主机IP"""
        try:
            # 获取本机IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "unknown-ip"
    
    def _get_thread_info(self, record: Dict[str, Any]) -> str:
        """获取线程信息"""
        try:
            thread_name = threading.current_thread().name
            thread_id = threading.get_ident()
            return f"{thread_name}({thread_id})"
        except Exception:
            return "unknown-thread"
    
    def _get_log_category(self, record: Dict[str, Any]) -> str:
        """获取日志分类"""
        # 可以根据模块名、级别等自动分类
        module_name = record.get('name', '')
        level = record['level'].name
        
        # 简单的分类逻辑
        if 'error' in level.lower() or 'exception' in str(record.get('message', '')).lower():
            return "error"
        elif 'api' in module_name.lower():
            return "api"
        elif 'business' in module_name.lower():
            return "business"
        else:
            return self.config.default_category
```

### 方案二：通过环境变量配置

#### 修改 `factory.py` 支持环境变量

```python
import os

def create_sls_sink(
    project: str,
    logstore: str,
    region: str,
    # ... 现有参数 ...
    app_name: Optional[str] = None,
    app_version: Optional[str] = None,
    environment: Optional[str] = None,
    **kwargs: Any
) -> Callable[[Dict[str, Any]], None]:
    """创建 SLS sink 函数"""
    
    # 从环境变量获取配置
    app_name = app_name or os.getenv('APP_NAME', 'unknown-app')
    app_version = app_version or os.getenv('APP_VERSION', '1.0.0')
    environment = environment or os.getenv('ENVIRONMENT', 'development')
    
    config = SlsConfig(
        # ... 现有配置 ...
        app_name=app_name,
        app_version=app_version,
        environment=environment,
        # ...
    )
```

### 方案三：配置文件支持

#### 修改 `logging.yaml` 配置

```yaml
handlers:
  - sink: "sls://yai-log-test/nexus-log?region=cn-beijing&pack_id_enabled=true&app_name=enterprise-demo&app_version=1.0.0&environment=production"
    level: "INFO"
    format: "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message} | {extra}"
```

## 配置示例

### 环境变量配置

```bash
# .env 文件
APP_NAME=enterprise-demo
APP_VERSION=1.2.3
ENVIRONMENT=production
SLS_AUTO_DETECT_HOSTNAME=true
SLS_AUTO_DETECT_HOST_IP=true
SLS_DEFAULT_CATEGORY=application
```

### 代码配置示例

```python
from yai_loguru_sinks.internal.factory import create_sls_sink

sls_sink = create_sls_sink(
    project="my-project",
    logstore="app-logs",
    region="cn-hangzhou",
    app_name="my-app",
    app_version="1.0.0",
    environment="production",
    auto_detect_hostname=True,
    auto_detect_host_ip=True,
    default_category="business"
)
```

## 实施优先级

### 高优先级（必须实现）
1. ✅ **app_name** - 应用标识，用于区分不同应用
2. ✅ **environment** - 环境标识，用于区分开发/测试/生产环境
3. ✅ **version** - 版本信息，用于问题追踪和版本对比
4. ✅ **hostname** - 主机标识，用于分布式环境下的问题定位

### 中优先级（建议实现）
5. 🔶 **category** - 日志分类，便于日志检索和分析
6. 🔶 **host_ip** - 主机IP，补充hostname信息

### 低优先级（可选实现）
7. 🔶 **thread** - 线程信息，用于并发问题调试

## 向后兼容性

- 所有新增字段都有默认值，不会破坏现有功能
- 现有的 `extra` 字段机制保持不变
- 现有的 PackId 功能保持不变
- 配置参数都是可选的，支持渐进式升级

## 测试验证

实施后需要验证以下内容：

1. **字段完整性**：确保所有必需字段都正确上报到SLS
2. **性能影响**：验证新增字段不会显著影响日志性能
3. **配置灵活性**：验证通过环境变量和配置文件都能正确配置
4. **向后兼容**：验证现有代码无需修改即可正常工作

## 总结

通过实施以上方案，可以让 SLS 日志上报包含完整的结构化字段，提升日志的可观测性和问题排查效率。建议优先实现高优先级字段，然后根据实际需求逐步完善其他字段。