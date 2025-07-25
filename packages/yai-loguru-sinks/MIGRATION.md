# 迁移指南：从插件系统到 Sink 工厂模式

本指南将帮助您从传统的 `yai-loguru` 插件系统迁移到新的基于 `loguru-config` 的 sink 工厂模式。

## 🎯 迁移概述

### 旧架构（插件系统）
- 复杂的插件抽象层
- 手动插件注册和配置
- 分散的配置管理
- 冗余的生命周期管理

### 新架构（Sink 工厂）
- 简洁的工厂函数
- 配置驱动的设计
- 统一的配置文件
- 利用 `loguru-config` 生态

## 📋 迁移步骤

### 步骤 1：安装新依赖

```bash
# 安装新的 yai-loguru-sinks 包
uv add yai-loguru-sinks

# 安装 loguru-config（如果尚未安装）
uv add loguru-config

# 可选：移除旧的插件包（迁移完成后）
# uv remove yai-loguru-sls-sink
```

### 步骤 2：代码迁移

#### 旧代码（插件系统）

```python
from yai_loguru import PluginManager
from yai_loguru_sls_sink import SlsSinkPlugin

# 创建插件管理器
manager = PluginManager()

# 注册插件
manager.register_plugin('sls', SlsSinkPlugin())

# 配置插件
manager.setup_plugin('sls', {
    'endpoint': 'https://cn-hangzhou.log.aliyuncs.com',
    'access_key_id': 'your-access-key-id',
    'access_key': 'your-access-key-secret',
    'project': 'my-project',
    'logstore': 'my-logstore',
    'topic': 'python-app',
    'level': 'WARNING',
    'batch_size': 50,
    'flush_interval': 5.0
})

# 使用 logger
from loguru import logger
logger.info("Hello World")

# 清理
manager.cleanup_all()
```

#### 新代码（配置驱动）

```python
from yai_loguru_sinks import setup_extended_config
from loguru_config import LoguruConfig
from loguru import logger

# 注册企业级协议解析器
setup_extended_config()

# 从配置文件加载
config = LoguruConfig()
config.load('logging.yaml')

# 直接使用 logger
logger.info("Hello World")

# 无需手动清理，loguru 自动管理
```

#### 新代码（直接使用工厂）

```python
from yai_loguru_sinks import create_sls_sink
from loguru import logger

# 创建 SLS sink
sls_sink = create_sls_sink(
    project="my-project",
    logstore="my-logstore",
    region="cn-hangzhou",
    access_key_id="your-access-key-id",
    access_key_secret="your-access-key-secret",
    topic="python-app",
    batch_size=50,
    flush_interval=5.0
)

# 添加到 logger
logger.add(sls_sink, level="WARNING")

# 使用 logger
logger.info("Hello World")
```

### 步骤 3：配置文件迁移

#### 旧配置（Python 代码）

```python
plugin_configs = {
    'sls': {
        'endpoint': 'https://cn-hangzhou.log.aliyuncs.com',
        'access_key_id': 'your-access-key-id',
        'access_key': 'your-access-key-secret',
        'project': 'my-project',
        'logstore': 'my-logstore',
        'topic': 'python-app',
        'level': 'WARNING',
        'batch_size': 50,
        'flush_interval': 5.0
    }
}
```

#### 新配置（YAML 文件）

```yaml
# logging.yaml
handlers:
  # 阿里云 SLS - 错误和警告日志
  - sink: sls://my-project/my-logstore?region=cn-hangzhou&topic=python-app&batch_size=50&flush_interval=5.0
    level: WARNING
    format: "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
    
  # 本地文件 - 所有日志
  - sink: logs/app.log
    level: INFO
    rotation: "1 day"
    retention: "30 days"
    compression: gz
    
  # 控制台 - 调试信息
  - sink: sys.stderr
    level: DEBUG
    format: "<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | {message}"

# 全局配置
level: INFO
extra:
  app_name: "my-application"
  version: "1.0.0"
```

### 步骤 4：环境变量配置

```bash
# .env 文件
SLS_ACCESS_KEY_ID=your-access-key-id
SLS_ACCESS_KEY_SECRET=your-access-key-secret

# AWS CloudWatch（可选）
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1

# Elasticsearch（可选）
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_USERNAME=elastic
ELASTICSEARCH_PASSWORD=password
```

## 🔄 配置映射对照表

| 旧插件配置 | 新 URL 协议 | 说明 |
|-----------|------------|------|
| `endpoint` | `region` 参数 | 从完整 endpoint 简化为 region |
| `access_key_id` | 环境变量 `SLS_ACCESS_KEY_ID` | 安全性提升 |
| `access_key` | 环境变量 `SLS_ACCESS_KEY_SECRET` | 安全性提升 |
| `project` | URL 路径第一部分 | `sls://project/logstore` |
| `logstore` | URL 路径第二部分 | `sls://project/logstore` |
| `topic` | URL 参数 `topic` | `?topic=value` |
| `batch_size` | URL 参数 `batch_size` | `?batch_size=50` |
| `flush_interval` | URL 参数 `flush_interval` | `?flush_interval=5.0` |
| `level` | handler 配置 | 移到 handler 级别 |

## 🚀 高级迁移场景

### 场景 1：多环境配置

#### 旧方式
```python
if env == 'production':
    manager.setup_plugin('sls', prod_config)
elif env == 'staging':
    manager.setup_plugin('sls', staging_config)
```

#### 新方式
```python
# 使用不同的配置文件
config_file = f'logging-{env}.yaml'
config = LoguruConfig()
config.load(config_file)
```

### 场景 2：动态配置

#### 旧方式
```python
# 运行时修改配置
manager.cleanup_plugin('sls')
manager.setup_plugin('sls', new_config)
```

#### 新方式
```python
# 动态添加新的 sink
if condition:
    extra_sink = create_sls_sink(**extra_config)
    logger.add(extra_sink, level="ERROR")
```

### 场景 3：多个 SLS 项目

#### 旧方式
```python
manager.register_plugin('sls1', SlsSinkPlugin())
manager.register_plugin('sls2', SlsSinkPlugin())
manager.setup_plugin('sls1', config1)
manager.setup_plugin('sls2', config2)
```

#### 新方式
```yaml
handlers:
  - sink: sls://project1/logstore1?region=cn-hangzhou
    level: ERROR
  - sink: sls://project2/logstore2?region=cn-beijing
    level: WARNING
```

## ⚠️ 注意事项

### 1. 依赖管理
- 新架构依赖 `loguru-config`，确保版本兼容
- 旧的插件包可以在迁移完成后移除

### 2. 配置安全
- 敏感信息（如密钥）应使用环境变量
- 避免在配置文件中硬编码凭据

### 3. 性能考虑
- 新架构移除了插件抽象层，性能更好
- 批量发送和异步处理逻辑保持不变

### 4. 错误处理
- 新架构提供更好的类型安全
- 配置错误会在启动时立即发现

## 🧪 测试迁移

### 1. 并行运行测试
```python
# 同时运行新旧系统进行对比
def test_migration():
    # 旧系统
    old_manager = PluginManager()
    # ... 配置旧系统
    
    # 新系统
    setup_extended_config()
    config = LoguruConfig()
    config.load('logging.yaml')
    
    # 发送测试日志
    logger.info("Migration test message")
    
    # 验证两个系统都收到日志
```

### 2. 配置验证
```python
from yai_loguru_sinks import setup_extended_config
from loguru_config import LoguruConfig

def validate_config():
    try:
        setup_extended_config()
        config = LoguruConfig()
        config.load('logging.yaml')
        print("✅ 配置验证成功")
    except Exception as e:
        print(f"❌ 配置验证失败: {e}")
```

## 📚 更多资源

- [yai-loguru-sinks 文档](./README.md)
- [loguru-config 官方文档](https://github.com/erezinman/loguru-config)
- [配置示例](./examples/)
- [故障排除指南](./TROUBLESHOOTING.md)

## 🆘 获取帮助

如果在迁移过程中遇到问题：

1. 查看 [故障排除指南](./TROUBLESHOOTING.md)
2. 参考 [示例代码](./examples/)
3. 提交 [Issue](https://github.com/your-org/yai-loguru-sinks/issues)

---

**迁移完成后，您将享受到：**
- ✅ 更简洁的代码
- ✅ 统一的配置管理
- ✅ 更好的类型安全
- ✅ 利用成熟的生态系统
- ✅ 更容易的测试和调试