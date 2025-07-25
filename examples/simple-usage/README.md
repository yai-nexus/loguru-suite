# Simple Usage - yai-loguru 基础使用示例

这个示例演示了如何使用 `yai-loguru` 核心库进行基本的日志配置和输出。虽然初始化了插件管理器，但不加载任何插件，专注于展示核心功能。

## 🎯 示例内容

- **基本日志配置**: 控制台输出和文件输出
- **日志级别**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **结构化日志**: 使用 `bind()` 添加上下文信息
- **异常处理**: 自动捕获异常堆栈
- **文件轮转**: 按日期轮转和压缩
- **多种格式**: 彩色控制台输出和 JSON 文件输出

## 🚀 运行示例

```bash
cd examples/simple-usage
python main.py
```

## 📁 输出文件

运行后会在 `../../logs/` 目录下生成以下文件：

- `simple-app_YYYY-MM-DD.log` - 标准格式的日志文件
- `simple-app-json_YYYY-MM-DD.log` - JSON 格式的日志文件

## 🔧 主要特性

### 1. 彩色控制台输出
```python
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | ...",
    colorize=True
)
```

### 2. 文件轮转和压缩
```python
logger.add(
    sink="logs/app_{time:YYYY-MM-DD}.log",
    rotation="00:00",      # 每天午夜轮转
    retention="7 days",    # 保留7天
    compression="zip"      # 压缩旧文件
)
```

### 3. 结构化日志
```python
logger.bind(user_id="123", request_id="456").info("用户操作")
```

### 4. JSON 格式输出
```python
logger.add(
    sink="logs/app-json.log",
    serialize=True,  # JSON 格式
    level="INFO"
)
```

## 📚 学习要点

1. **配置灵活性**: Loguru 提供了非常灵活的配置选项
2. **性能优化**: 支持异步写入和批量处理
3. **格式自定义**: 支持多种输出格式和自定义模板
4. **上下文绑定**: 轻松添加结构化信息
5. **异常处理**: 自动捕获和格式化异常信息

##  dissected 代码解析

`main.py` 的代码非常简洁，关键步骤如下：

```python
import asyncio
from loguru import logger
from yai_loguru_support.sls import AliyunSlsSink
from yai_loguru_support.utils import create_production_setup

async def main():
    # 1. 从环境变量自动创建 Sink 实例
    # Sink 是 loguru 的术语，代表一个日志输出目标。
    # .from_env() 方法会自动读取 SLS_* 环境变量并完成配置。
    sls_sink = AliyunSlsSink.from_env()
    
    # 2. 将 Sink 添加到 loguru
    # `serialize=True` 会将日志记录转换为 JSON 格式，便于云服务处理。
    logger.add(sls_sink, serialize=True, level="INFO")
    
    # 3. 设置优雅停机钩子
    # 这是关键一步！它能确保在程序退出时，所有在内存中排队的日志
    # 都能被完整发送出去，避免日志丢失。
    create_production_setup([sls_sink])
    
    # 4. 使用标准的 loguru API 发送日志
    logger.info("Hello SLS!", user_id="123", request_id="abc-xyz")
    
    # 5. 等待日志发送
    # 日志是批量异步发送的，这里等待几秒确保发送完成。
    # 在真实应用中，程序会持续运行。
    await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔌 扩展到其他服务

本示例展示了与阿里云 SLS 的集成，但 `yai-loguru-support` 的设计是可扩展的。您可以参照 `yai_loguru_support/sls` 的实现，轻松创建与其他云日志服务（如 Sentry, DataDog, Grafana Loki 等）集成的 Sink。

核心是实现一个遵循 `loguru` Sink 协议的类，并处理好批量发送和优雅停机。

## 💡 故障排查

- **认证失败?**
  请检查您的 Access Key ID 和 Secret 是否正确，并且该账户拥有对应 SLS Logstore 的写入权限。
- **连接超时?**
  请检查 `SLS_ENDPOINT` 是否正确，以及您的网络环境是否可以访问阿里云服务。
- **找不到项目或日志库?**
  请确保您已在阿里云控制台提前创建了对应的 Project 和 Logstore。