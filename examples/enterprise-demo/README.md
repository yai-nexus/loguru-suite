# Enterprise Demo

企业级日志示例，展示 `yai-loguru-sinks` 的 SLS（阿里云日志服务）集成功能。

## 🎯 功能特点

- **多输出目标**：同时输出到控制台、文件和阿里云 SLS
- **结构化日志**：支持 JSON 格式的结构化日志记录
- **SLS 集成**：无缝集成阿里云日志服务
- **环境配置**：通过环境变量管理敏感信息
- **优雅降级**：SLS 不可用时自动降级到本地日志

## 📁 文件结构

```
enterprise-demo/
├── main.py                    # 主程序
├── pyproject.toml             # 项目配置
├── logging.yaml               # 日志配置
├── .env.example               # 环境变量模板
├── install_and_run.sh         # 安装和运行脚本
├── logs/                      # 日志输出目录
└── README.md                  # 说明文档
```

## 🚀 快速开始

### 1. 配置 SLS 环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 SLS 配置
vim .env
```

### 2. 运行示例

```bash
# 安装依赖并运行
./install_and_run.sh
```

## 📝 示例内容

### 基础日志记录
- DEBUG、INFO、WARNING、ERROR 级别日志
- 控制台彩色输出
- 文件持久化存储

### 结构化日志
- 用户操作日志（登录、操作记录）
- API 调用日志（请求响应信息）
- 业务指标日志（订单、支付等）

### SLS 云日志
- 实时日志传输到阿里云
- 支持日志检索和分析
- 企业级日志管理

### 错误处理
- 异常堆栈跟踪
- 结构化错误信息
- 自动错误分类

## ⚙️ 配置说明

### SLS 配置参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `SLS_ENDPOINT` | SLS 服务端点 | `https://cn-hangzhou.log.aliyuncs.com` |
| `SLS_ACCESS_KEY_ID` | 阿里云访问密钥 ID | `your_access_key_id` |
| `SLS_ACCESS_KEY_SECRET` | 阿里云访问密钥 Secret | `your_access_key_secret` |
| `SLS_PROJECT` | SLS 项目名称 | `your_project_name` |
| `SLS_LOGSTORE` | SLS 日志库名称 | `your_logstore_name` |

### 日志配置

- **控制台输出**：INFO 级别，彩色显示
- **文件输出**：DEBUG 级别，JSON 格式，10MB 轮转
- **SLS 输出**：INFO 级别，JSON 格式，批量发送

## 🔧 故障排除

### SLS 连接问题
1. 检查网络连接
2. 验证 SLS 配置参数
3. 确认访问密钥权限

### 依赖问题
```bash
# 重新安装依赖
uv sync --force
```

## 📚 下一步

- 查看 [yai-loguru-sinks 文档](../../packages/yai-loguru-sinks/README.md)
- 了解更多 SLS 配置选项
- 集成到你的生产环境