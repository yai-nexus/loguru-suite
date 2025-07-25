# yai-loguru 插件系统使用示例

这个示例演示了如何使用 `yai-loguru` 的插件系统来扩展日志功能。通过插件系统，你可以轻松地添加各种日志输出目标，如文件、云服务等。

## 🚀 快速开始

### 1. 安装依赖

```bash
# 进入示例目录
cd examples/plugin-usage

# 安装依赖
pip install -e .
```

### 2. 运行示例

```bash
python main.py
```

## 📦 插件系统概述

`yai-loguru` 的插件系统提供了以下核心功能：

- **插件发现**: 自动发现已安装的插件
- **动态加载**: 运行时加载和卸载插件
- **配置管理**: 灵活的插件配置系统
- **批量管理**: 同时管理多个插件
- **状态验证**: 检查插件的运行状态

## 🔌 可用插件

### 文件插件 (`yai-loguru-file-sink`)

用于将日志输出到文件，支持：
- 日志轮转（按大小、时间）
- 压缩存档
- 自定义格式
- 多级别过滤

```python
file_config = {
    "file_path": "logs/app_{time:YYYY-MM-DD}.log",
    "level": "INFO",
    "format": "{time} | {level} | {message}",
    "rotation": "10 MB",
    "retention": "7 days",
    "compression": "zip"
}
manager.load_plugin("file_sink", file_config)
```

### SLS 插件 (`yai-loguru-sls-sink`)

用于将日志发送到阿里云 SLS，支持：
- 批量发送
- 自动重试
- 结构化日志
- 上下文绑定

```python
sls_config = {
    "endpoint": "your-project.log.aliyuncs.com",
    "access_key_id": "your_access_key",
    "access_key_secret": "your_secret",
    "project": "your_project",
    "logstore": "your_logstore",
    "topic": "application",
    "source": "web-server"
}
manager.load_plugin("sls_sink", sls_config)
```

## 💡 使用示例

### 基本使用

```python
from yai_loguru import PluginManager
from loguru import logger

# 初始化插件管理器
manager = PluginManager()

# 发现可用插件
plugins = manager.discover_plugins()
print(f"可用插件: {plugins}")

# 加载插件
config = {"file_path": "app.log", "level": "INFO"}
manager.load_plugin("file_sink", config)

# 使用日志
logger.info("Hello, Plugin System!")

# 清理
manager.cleanup_all()
```

### 批量配置

```python
# 同时配置多个插件
plugins_config = {
    "file_sink": {
        "file_path": "app.log",
        "level": "INFO"
    },
    "sls_sink": {
        "endpoint": "your-endpoint",
        "project": "your-project",
        # ... 其他配置
    }
}

manager.setup_plugins(plugins_config)
```

### 动态管理

```python
# 运行时加载插件
manager.load_plugin("file_sink", config)

# 检查插件状态
from yai_loguru import validate_plugin
is_valid = validate_plugin("file_sink")

# 卸载插件
manager.unload_plugin("file_sink")
```

## 📁 示例结构

```
plugin-usage/
├── main.py              # 主示例文件
├── pyproject.toml       # 项目配置
├── README.md           # 说明文档
└── ../../logs/         # 日志输出目录
    ├── plugin-demo_*.log
    ├── batch-demo_*.log
    └── dynamic-test.log
```

## 🔧 示例功能

### 1. 插件发现和加载
- 自动发现系统中安装的插件
- 演示插件的加载和配置过程

### 2. 文件插件演示
- 配置文件日志输出
- 演示日志轮转和压缩
- 展示自定义格式和过滤

### 3. SLS 插件演示
- 配置阿里云 SLS 连接
- 演示结构化日志发送
- 展示上下文绑定功能

### 4. 批量管理
- 同时配置多个插件
- 演示插件状态验证
- 展示批量清理功能

### 5. 高级功能
- 动态插件加载/卸载
- 插件状态检查
- 系统插件列表

## 🎯 学习要点

1. **插件架构**: 理解 yai-loguru 的插件系统设计
2. **配置管理**: 学习如何配置不同类型的插件
3. **动态管理**: 掌握运行时插件管理技巧
4. **最佳实践**: 了解插件使用的最佳实践
5. **错误处理**: 学习插件加载失败的处理方法

## 🔍 输出文件

运行示例后，会在 `../../logs/` 目录下生成以下文件：

- `plugin-demo_YYYY-MM-DD.log`: 文件插件演示日志
- `batch-demo_YYYY-MM-DD.log`: 批量配置演示日志
- `/tmp/dynamic-test.log`: 动态加载演示日志

## 📚 相关文档

- [yai-loguru 核心文档](../../README.md)
- [文件插件文档](../../yai-loguru-file-sink/README.md)
- [SLS 插件文档](../../yai-loguru-sls-sink/README.md)

## 🤝 扩展插件

想要开发自己的插件？参考：
1. 继承 `LoguruPlugin` 基类
2. 实现 `setup()` 和 `cleanup()` 方法
3. 配置插件入口点
4. 发布到 PyPI

示例插件模板可以参考现有的文件插件和 SLS 插件实现。