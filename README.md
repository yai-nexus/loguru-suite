# Loguru Suite

🚀 **企业级 Loguru 日志解决方案套件**

一个专为企业级应用设计的 Loguru 扩展生态系统，提供简洁、强大、可扩展的日志管理能力。

## 🎯 核心理念

- **简洁优雅**：基于 Loguru 的简洁设计理念，移除不必要的复杂性
- **配置驱动**：通过 YAML/JSON 配置文件管理所有日志设置
- **企业级**：专注于企业级日志需求，特别是阿里云 SLS 集成
- **开箱即用**：提供完整的示例和最佳实践

## 📦 项目结构

```
loguru-suite/
├── packages/                   # 核心包
│   └── yai-loguru-sinks/      # 企业级 Sink 工厂库
├── examples/                   # 示例项目
│   ├── basic-demo/            # 基础使用示例
│   └── enterprise-demo/       # 企业级功能示例
├── scripts/                   # 构建和发布脚本
└── docs/                      # 文档（规划中）
```

## 🚀 快速开始

### 1. 安装核心包

```bash
# 使用 uv（推荐）
uv add yai-loguru-sinks

# 或使用 pip
pip install yai-loguru-sinks
```

### 2. 基础使用

```python
from loguru import logger
from yai_loguru_sinks import register_protocol_parsers, create_config_from_file

# 注册协议解析器
register_protocol_parsers()

# 使用配置文件方式
create_config_from_file("logging.yaml")  # 配置文件中可以使用 sls:// 协议

# 或者直接使用 sink 工厂
from yai_loguru_sinks.internal.factory import create_sls_sink
sls_sink = create_sls_sink(
    project="my-project",
    logstore="app-logs", 
    region="cn-hangzhou"
)
logger.add(sls_sink)
```

### 3. 配置文件示例

```yaml
# logging.yaml
handlers:
  # 控制台输出
  - sink: sys.stdout
    level: INFO
    format: "<green>{time}</green> | <level>{level}</level> | {message}"
    
  # 文件输出
  - sink: logs/app.log
    level: DEBUG
    rotation: "10 MB"
    retention: "7 days"
    compression: "gz"
    
  # 阿里云 SLS（企业级）
  - sink: sls://my-project/my-logstore?region=cn-hangzhou&access_key_id=${SLS_ACCESS_KEY}&access_key_secret=${SLS_SECRET}
    level: WARNING
    format: '{time} | {level} | {message}'
```

## 📚 核心包介绍

### yai-loguru-sinks

企业级 Loguru Sink 工厂库，提供：

- **阿里云 SLS 集成**：无缝集成阿里云日志服务
- **PackId 支持**：自动生成和管理日志关联 ID
- **异步处理**：高性能异步日志发送
- **优雅降级**：云服务不可用时自动降级到本地日志
- **配置驱动**：基于 `loguru-config` 的统一配置体验

[查看详细文档 →](./packages/yai-loguru-sinks/README.md)

## 🎯 示例项目

### Basic Demo - 基础示例

适合初学者的简单示例，展示：
- 基本日志级别使用
- 控制台和文件双重输出
- 日志轮转和压缩

```bash
cd examples/basic-demo
./sync_and_run.sh
```

[查看详细说明 →](./examples/basic-demo/README.md)

### Enterprise Demo - 企业级示例

完整的企业级日志解决方案，展示：
- 阿里云 SLS 集成
- 结构化日志记录
- 多环境配置管理
- PackId 功能验证

```bash
cd examples/enterprise-demo
cp .env.example .env  # 配置你的 SLS 信息
./sync_and_run.sh
```

[查看详细说明 →](./examples/enterprise-demo/README.md)

## 🔧 开发指南

### 环境要求

- Python 3.10+
- uv（包管理器）

### 本地开发

```bash
# 克隆项目
git clone https://github.com/yai-nexus/loguru-suite.git
cd loguru-suite

# 进入核心包目录
cd packages/yai-loguru-sinks

# 安装依赖
uv sync

# 运行测试
uv run python -m pytest tests/

# 运行示例
cd ../../examples/basic-demo
uv run python main.py
```

### 发布流程

```bash
# 发布新版本
./scripts/publish.sh yai-loguru-sinks 0.6.0

# 测试发布
./scripts/publish.sh yai-loguru-sinks 0.6.0-beta.1 --test
```

## 🌟 特性亮点

### ✅ 简洁架构
- 移除复杂的插件抽象
- 直接提供 sink 工厂函数
- 基于成熟的 `loguru-config` 生态

### ✅ 企业级功能
- 阿里云 SLS 深度集成
- PackId 自动管理
- 异步高性能处理
- 优雅的错误处理

### ✅ 开发友好
- 完整的类型提示
- 丰富的示例代码
- 详细的文档说明
- 活跃的社区支持

## 📖 文档资源

- [API 文档](./packages/yai-loguru-sinks/README.md)
- [配置指南](./examples/README.md)
- [最佳实践](./docs/best-practices.md)（规划中）
- [故障排除](./docs/troubleshooting.md)（规划中）

## 🤝 贡献指南

我们欢迎所有形式的贡献！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🔗 相关链接

- [PyPI 页面](https://pypi.org/project/yai-loguru-sinks/)
- [GitHub 仓库](https://github.com/yai-nexus/loguru-suite)
- [问题反馈](https://github.com/yai-nexus/loguru-suite/issues)
- [更新日志](https://github.com/yai-nexus/loguru-suite/releases)

---

<div align="center">
  <strong>让企业级日志管理变得简单而强大</strong>
</div>