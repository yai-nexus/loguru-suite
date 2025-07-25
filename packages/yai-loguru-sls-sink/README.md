# YAI Loguru SLS Sink Plugin

一个为 yai-loguru 提供阿里云 SLS（简单日志服务）集成的插件。

## 功能特性

- 🚀 异步批量发送日志到阿里云 SLS
- 🔧 支持环境变量配置
- 📦 完整的错误处理和重试机制
- 🎯 可配置的日志级别和格式
- 🔄 自动定时刷新和优雅停机

## 安装

```bash
# 安装SLS插件（会自动安装依赖）
uv add yai-loguru-sls-sink
```

## 配置

### 环境变量配置

```bash
export SLS_ENDPOINT=cn-hangzhou.log.aliyuncs.com
export SLS_AK_ID=your_access_key_id
export SLS_AK_KEY=your_access_key_secret
export SLS_PROJECT=my-log-project
export SLS_LOGSTORE=app-logs
export SLS_TOPIC=python-app  # 可选
export SLS_SOURCE=yai-loguru  # 可选
```

### 代码配置

```python
from yai_loguru import PluginManager
from loguru import logger

# 初始化插件管理器
manager = PluginManager()

# 配置SLS插件
sls_config = {
    "endpoint": "cn-hangzhou.log.aliyuncs.com",
    "access_key_id": "your_access_key_id",
    "access_key": "your_access_key_secret",
    "project": "my-log-project",
    "logstore": "app-logs",
    "topic": "python-app",
    "source": "my-service",
    "level": "INFO",
    "batch_size": 100,
    "flush_interval": 5.0
}

# 加载并启用SLS插件
if manager.load_plugin("sls_sink", sls_config):
    logger.info("SLS插件已启用")
    
    # 发送日志
    logger.info("这条日志会发送到阿里云SLS")
    logger.error("错误日志也会发送到SLS")
    
    # 清理插件
    manager.cleanup()
```

## 配置参数

| 参数 | 类型 | 必需 | 默认值 | 描述 |
|------|------|------|--------|------|
| `endpoint` | str | ✅ | - | SLS服务端点 |
| `access_key_id` | str | ✅ | - | 阿里云Access Key ID |
| `access_key` | str | ✅ | - | 阿里云Access Key Secret |
| `project` | str | ✅ | - | SLS项目名称 |
| `logstore` | str | ✅ | - | SLS日志库名称 |
| `topic` | str | ❌ | "python-app" | 日志主题 |
| `source` | str | ❌ | "yai-loguru" | 日志来源 |
| `level` | str | ❌ | "INFO" | 日志级别 |
| `batch_size` | int | ❌ | 100 | 批量发送大小 |
| `flush_interval` | float | ❌ | 5.0 | 定时刷新间隔（秒） |
| `max_retries` | int | ❌ | 3 | 最大重试次数 |
| `timeout` | float | ❌ | 30.0 | 请求超时时间（秒） |
| `compress` | bool | ❌ | True | 是否压缩传输 |

## 许可证

MIT License