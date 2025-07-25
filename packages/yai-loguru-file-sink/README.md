# YAI Loguru File Sink Plugin

一个用于 `yai-loguru` 的文件日志输出插件，支持多种文件策略和配置选项。

## 功能特性

- 🗂️ **自动目录创建**: 自动创建日志文件所需的目录结构
- 🔄 **文件轮转**: 支持按大小、时间等策略进行文件轮转
- 🗜️ **压缩支持**: 支持自动压缩旧日志文件
- 📝 **灵活配置**: 支持自定义日志格式、级别、编码等
- 🧹 **资源管理**: 提供清理方法，确保资源正确释放

## 安装

```bash
# 通过 uv 安装
uv pip install yai-loguru-file-sink

# 或者在 monorepo 中开发模式安装
uv pip install -e packages/yai-loguru-file-sink
```

## 使用方法

### 基本用法

```python
from yai_loguru import PluginManager
from loguru import logger

# 创建插件管理器
manager = PluginManager()

# 配置文件日志插件
config = {
    "file_path": "logs/app.log",
    "level": "INFO",
    "rotation": "1 day",
    "retention": "7 days",
    "compression": "zip"
}

# 加载并设置插件
manager.load_plugin("file_sink", config)

# 正常使用 loguru
logger.info("这条日志会写入文件")
```

### 高级配置

```python
# 更详细的配置示例
config = {
    "file_path": "logs/detailed.log",
    "level": "DEBUG",
    "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    "rotation": "100 MB",  # 按文件大小轮转
    "retention": "30 days",  # 保留30天
    "compression": "gz",  # gzip压缩
    "encoding": "utf-8",
    "ensure_dir": True  # 自动创建目录
}
```

## 配置选项

| 选项 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `file_path` | str | ✅ | - | 日志文件路径 |
| `level` | str | ❌ | "INFO" | 日志级别 |
| `format` | str | ❌ | loguru默认 | 日志格式 |
| `rotation` | str/int | ❌ | - | 文件轮转策略 |
| `retention` | str/int | ❌ | - | 文件保留策略 |
| `compression` | str | ❌ | - | 压缩格式 (zip, gz, bz2) |
| `encoding` | str | ❌ | "utf-8" | 文件编码 |
| `ensure_dir` | bool | ❌ | True | 是否自动创建目录 |

## 开发

```bash
# 克隆项目
git clone https://github.com/yai-nexus/loguru-suite.git
cd loguru-suite

# 安装开发依赖
./scripts/install.sh

# 运行测试
uv run pytest packages/yai-loguru-file-sink/tests/
```

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。