# API 参考文档

## yai-loguru-sinks API

### 核心函数

#### `register_protocol_parsers()`

注册所有支持的协议解析器，包括 SLS、CloudWatch、Elasticsearch、Kafka 等。

**函数签名：**
```python
def register_protocol_parsers() -> None
```

**使用示例：**
```python
from yai_loguru_sinks import register_protocol_parsers

# 注册所有协议解析器
register_protocol_parsers()
```

**注意事项：**
- 必须在使用任何协议 URL 之前调用
- 只需要调用一次，通常在应用启动时
- 支持的协议：`sls://`、`cloudwatch://`、`elasticsearch://`、`kafka://`

---

#### `create_config_from_file(config_path: str)`

从 YAML 或 JSON 配置文件加载日志配置。

**函数签名：**
```python
def create_config_from_file(config_path: str) -> None
```

**参数：**
- `config_path` (str): 配置文件路径，支持 YAML 和 JSON 格式

**使用示例：**
```python
from yai_loguru_sinks import create_config_from_file

# 从 YAML 文件加载配置
create_config_from_file('logging.yaml')

# 从 JSON 文件加载配置
create_config_from_file('logging.json')
```

**配置文件格式：**
```yaml
handlers:
  - sink: sls://project/logstore?region=cn-hangzhou
    level: INFO
    format: '{time} | {level} | {message}'
```

---

#### `create_config_from_dict(config_dict: dict)`

从字典对象加载日志配置。

**函数签名：**
```python
def create_config_from_dict(config_dict: dict) -> None
```

**参数：**
- `config_dict` (dict): 包含日志配置的字典对象

**使用示例：**
```python
from yai_loguru_sinks import create_config_from_dict

config = {
    "handlers": [
        {
            "sink": "sls://my-project/my-logstore?region=cn-hangzhou",
            "level": "INFO",
            "format": "{time} | {level} | {message}"
        }
    ]
}

create_config_from_dict(config)
```

---

### 内部 API

#### `create_sls_sink()`

直接创建阿里云 SLS sink 对象。

**函数签名：**
```python
def create_sls_sink(
    project: str,
    logstore: str,
    region: str,
    access_key_id: Optional[str] = None,
    access_key_secret: Optional[str] = None,
    endpoint: Optional[str] = None,
    **kwargs
) -> Callable
```

**参数：**
- `project` (str): SLS 项目名称
- `logstore` (str): SLS 日志库名称
- `region` (str): 阿里云地域
- `access_key_id` (str, optional): 访问密钥 ID
- `access_key_secret` (str, optional): 访问密钥 Secret
- `endpoint` (str, optional): 自定义端点

**使用示例：**
```python
from loguru import logger
from yai_loguru_sinks.internal.factory import create_sls_sink

# 创建 SLS sink
sls_sink = create_sls_sink(
    project="my-project",
    logstore="app-logs",
    region="cn-hangzhou",
    access_key_id="your_key_id",
    access_key_secret="your_key_secret"
)

# 添加到 logger
logger.add(sls_sink, level="INFO")
```

---

## 协议 URL 格式

### SLS 协议

**基本格式：**
```
sls://project/logstore?region=region&access_key_id=key&access_key_secret=secret
```

**参数说明：**
- `project`: SLS 项目名称
- `logstore`: SLS 日志库名称
- `region`: 阿里云地域（必需）
- `access_key_id`: 访问密钥 ID（可选，支持环境变量）
- `access_key_secret`: 访问密钥 Secret（可选，支持环境变量）
- `endpoint`: 自定义端点（可选）

**环境变量支持：**
```yaml
sink: sls://project/logstore?region=cn-hangzhou&access_key_id=${SLS_ACCESS_KEY}&access_key_secret=${SLS_SECRET}
```

**完整示例：**
```yaml
handlers:
  - sink: sls://my-project/app-logs?region=cn-hangzhou&access_key_id=${SLS_ACCESS_KEY}&access_key_secret=${SLS_SECRET}&endpoint=https://cn-hangzhou.log.aliyuncs.com
    level: INFO
    format: '{time} | {level} | {message}'
    serialize: true
```

---

## 错误处理

### 常见异常

#### `ValueError`
- 协议 URL 格式错误
- 必需参数缺失

#### `ConnectionError`
- 网络连接失败
- SLS 服务不可用

#### `AuthenticationError`
- 访问密钥错误
- 权限不足

### 错误处理最佳实践

```python
from yai_loguru_sinks import register_protocol_parsers, create_config_from_file
from loguru import logger

try:
    register_protocol_parsers()
    create_config_from_file('logging.yaml')
    logger.info("日志系统初始化成功")
except Exception as e:
    # 降级到基本日志配置
    logger.add("logs/fallback.log", level="INFO")
    logger.error(f"日志系统初始化失败，使用降级配置: {e}")
```