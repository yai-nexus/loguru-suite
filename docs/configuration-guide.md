# 配置指南 - 方案一：环境变量优先配置

本文档介绍了 yai-loguru-sinks 项目采用的环境变量优先配置方案的实施和使用方法。

## 🎯 方案概述

**方案一：环境变量优先配置** 是推荐的配置方案，具有以下特点：

- ✅ **安全性最佳**：敏感凭证完全从配置文件中分离
- ✅ **配置简洁**：logging.yaml 配置文件简洁易读
- ✅ **灵活性强**：支持环境变量覆盖和特定参数配置
- ✅ **团队协作友好**：便于不同环境和团队成员使用

## 📁 项目结构

```
loguru-suite/
├── .env                    # 实际环境变量配置（不提交到版本控制）
├── .env.example           # 环境变量配置模板
├── examples/
│   ├── basic-demo/
│   │   └── logging.yaml   # 简化的日志配置
│   └── enterprise-demo/
│       └── logging.yaml   # 企业级日志配置
└── packages/yai-loguru-sinks/
```

## ⚙️ 配置文件

### 1. 环境变量配置 (.env)

```bash
# ========== SLS 认证信息（必需）==========
# 请替换为你的真实凭证
SLS_ACCESS_KEY_ID=LTAI5tXXXXXXXXXXXXXX
SLS_ACCESS_KEY_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# ========== 应用信息配置 ==========
APP_NAME=loguru-suite
APP_VERSION=1.0.0
ENVIRONMENT=development

# ========== SLS 服务配置（可选）==========
SLS_DEFAULT_REGION=cn-beijing
SLS_DEFAULT_PROJECT=yai-log-test
```

### 2. 日志配置 (logging.yaml)

#### Basic Demo 配置
```yaml
handlers:
  # 控制台输出
  - sink: ext://sys.stdout
    level: "INFO"
    format: "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}"
    colorize: true
    
  # 文件输出
  - sink: "logs/basic-demo.log"
    level: "DEBUG"
    format: "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    rotation: "10 MB"
    retention: "7 days"
    compression: "zip"
    
  # SLS 输出（使用环境变量配置）
  - sink: "sls://yai-log-test/nexus-log?region=cn-beijing"
    level: "WARNING"
    format: "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
```

#### Enterprise Demo 配置
```yaml
handlers:
  # 控制台输出
  - sink: ext://sys.stdout
    level: "INFO"
    format: "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    colorize: true
    
  # 文件输出
  - sink: "logs/enterprise-demo.log"
    level: "DEBUG"
    format: "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message} | {extra}"
    rotation: "10 MB"
    retention: "7 days"
    compression: "gz"
    
  # SLS 输出（使用环境变量配置）
  - sink: "sls://yai-log-test/nexus-log?region=cn-beijing"
    level: "INFO"
    format: "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message} | {extra}"
```

## 🚀 使用方法

### 1. 初始化配置

```bash
# 1. 复制环境变量模板
cp .env.example .env

# 2. 编辑 .env 文件，填入真实凭证
vim .env
```

### 2. 代码中使用

```python
import os
from pathlib import Path
from loguru import logger
from yai_loguru_sinks import register_protocol_parsers, create_config_from_file

def load_environment():
    """加载环境变量"""
    try:
        from dotenv import load_dotenv
        # 加载项目根目录的 .env 文件
        project_root = Path(__file__).parent.parent.parent
        env_path = project_root / ".env"
        load_dotenv(env_path)
        print("✅ 已加载环境变量")
    except ImportError:
        print("⚠️ 未安装 python-dotenv，跳过 .env 文件加载")

def main():
    # 加载环境变量
    load_environment()
    
    # 注册协议解析器
    register_protocol_parsers()
    
    # 加载日志配置
    config_path = Path(__file__).parent / "logging.yaml"
    create_config_from_file(str(config_path))
    
    # 开始使用日志
    logger.info("日志系统初始化完成")
```

### 3. 依赖配置

确保项目包含必要的依赖：

```toml
# pyproject.toml
dependencies = [
    "loguru>=0.7.0",
    "yai-loguru-sinks",
    "pyyaml>=6.0",
    "python-dotenv>=1.0.0",  # 用于加载 .env 文件
]
```

## 🔧 配置优先级

配置参数的优先级顺序（从高到低）：

1. **URL 参数**：在 SLS URL 中直接指定的参数
2. **环境变量**：在 .env 文件或系统环境变量中设置的参数
3. **默认值**：代码中定义的默认值

### 示例

```yaml
# 如果需要覆盖特定参数，可以在 URL 中指定
sink: "sls://yai-log-test/nexus-log?region=cn-beijing&topic=custom-topic"
```

## 🌍 多环境配置

### 开发环境
```bash
# .env
ENVIRONMENT=development
SLS_ACCESS_KEY_ID=dev_key_id
SLS_ACCESS_KEY_SECRET=dev_key_secret
```

### 生产环境
```bash
# 系统环境变量或容器环境变量
export ENVIRONMENT=production
export SLS_ACCESS_KEY_ID=prod_key_id
export SLS_ACCESS_KEY_SECRET=prod_key_secret
```

### CI/CD 环境
```yaml
# GitHub Actions 示例
env:
  ENVIRONMENT: testing
  SLS_ACCESS_KEY_ID: ${{ secrets.SLS_ACCESS_KEY_ID }}
  SLS_ACCESS_KEY_SECRET: ${{ secrets.SLS_ACCESS_KEY_SECRET }}
```

## 🔒 安全最佳实践

1. **永远不要提交 .env 文件**
   - .env 文件已添加到 .gitignore
   - 只提交 .env.example 模板

2. **定期轮换访问密钥**
   - 建议每 90 天轮换一次 AccessKey
   - 使用阿里云 RAM 角色限制权限

3. **设置文件权限**
   ```bash
   chmod 600 .env  # 仅所有者可读写
   ```

4. **使用密钥管理服务**
   - 生产环境建议使用 AWS Secrets Manager、Azure Key Vault 等
   - 容器环境使用 Kubernetes Secrets

## 🧪 测试验证

### 1. 运行示例
```bash
# 测试 Basic Demo
cd examples/basic-demo
uv run python main.py

# 测试 Enterprise Demo
cd examples/enterprise-demo
uv run python main.py
```

### 2. 运行测试套件
```bash
cd packages/yai-loguru-sinks
uv run python run_tests.py --fast
```

## 🆚 与其他方案对比

| 特性 | 方案一（环境变量优先） | 方案二（URL 变量引用） |
|------|----------------------|----------------------|
| 安全性 | ✅ 最佳 | ⚠️ 中等 |
| 配置简洁性 | ✅ 简洁 | ❌ 冗长 |
| 团队协作 | ✅ 友好 | ⚠️ 一般 |
| 维护成本 | ✅ 低 | ❌ 高 |
| 推荐度 | ✅ 强烈推荐 | ❌ 不推荐 |

## 📚 相关文档

- [API 参考文档](api-reference.md)
- [SLS 日志字段上报方案](../SLS日志字段上报方案建议.md)
- [项目 README](../README.md)

## 🤝 贡献

如果您在使用过程中遇到问题或有改进建议，欢迎：

1. 提交 Issue
2. 发起 Pull Request
3. 参与讨论

---

**最后更新**：2025-01-29  
**版本**：1.0.0