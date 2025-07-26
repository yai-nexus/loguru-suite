# yai-loguru-sinks 示例项目

这是 `yai-loguru-sinks` 的官方示例项目，展示了如何在实际项目中使用企业级 Loguru Sink 工厂。

## 项目结构

```
examples/
├── README.md              # 项目说明文档
├── pyproject.toml         # 项目配置和依赖
├── src/                   # 源代码目录
│   └── usage_example.py   # 主要示例代码
├── configs/               # 配置文件目录
│   └── logging.yaml       # Loguru 配置文件
├── scripts/               # 脚本目录
│   └── run_examples.sh    # 运行示例的脚本
├── docs/                  # 文档目录
└── logs/                  # 日志输出目录
```

## 快速开始

### 方式一：使用脚本运行（推荐）

```bash
# 运行示例
./scripts/run_examples.sh
```

### 方式二：手动运行

```bash
# 安装依赖
uv sync

# 运行示例
uv run python src/usage_example.py
```

## 示例说明

### 主要示例文件

- **`src/usage_example.py`**: 展示了 5 种不同的使用方式：
  1. **配置驱动示例**: 完全通过配置文件驱动日志设置
  2. **直接使用 Sink 工厂**: 程序化创建和配置 sink
  3. **混合使用示例**: 配置文件 + 运行时动态添加
  4. **与旧插件系统对比**: 展示新架构的优势
  5. **多环境配置示例**: 根据环境变量选择不同配置

### 配置文件

- **`configs/logging.yaml`**: 标准的 Loguru 配置文件，包含：
  - SLS sink 配置（阿里云日志服务）
  - 本地文件 sink 配置
  - 控制台输出配置
  - 全局日志级别和格式设置

## 配置说明

### SLS Sink 配置

```yaml
sinks:
  sls_sink:
    sink: "sls://your-project/your-logstore?region=cn-hangzhou&topic=app"
    level: "INFO"
    format: "{time} | {level} | {name} | {message}"
```

### 文件 Sink 配置

```yaml
sinks:
  file_sink:
    sink: "logs/app.log"
    level: "DEBUG"
    rotation: "10 MB"
    retention: "7 days"
    compression: "zip"
```

## 环境变量支持

- `ENVIRONMENT`: 指定运行环境（development/staging/production）
- `LOG_LEVEL`: 覆盖默认日志级别
- `SLS_PROJECT`: SLS 项目名称
- `SLS_LOGSTORE`: SLS 日志库名称
- `SLS_REGION`: SLS 区域

## 最佳实践

1. **配置文件管理**: 为不同环境维护独立的配置文件
2. **敏感信息**: 使用环境变量存储 AccessKey 等敏感信息
3. **日志轮转**: 合理配置文件大小和保留策略
4. **性能优化**: 根据业务需求调整缓冲和批量发送参数

## 故障排除

### 常见问题

1. **依赖缺失**: 确保已安装 `loguru-config` 和 `aliyun-log-python-sdk`
2. **配置文件路径**: 检查配置文件是否在正确的 `configs/` 目录下
3. **SLS 连接**: 验证网络连接和 SLS 配置参数
4. **权限问题**: 确保有写入 `logs/` 目录的权限

### 调试模式

```bash
# 启用详细日志输出
export LOG_LEVEL=DEBUG
./scripts/run_examples.sh
```

## 相关链接

- [yai-loguru-sinks 主项目](../packages/yai-loguru-sinks/)
- [Loguru 官方文档](https://loguru.readthedocs.io/)
- [阿里云 SLS 文档](https://help.aliyun.com/product/28958.html)