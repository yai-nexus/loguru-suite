# GitHub Actions 工作流说明

本目录包含项目的 GitHub Actions 工作流配置。

## 📋 工作流概览

### 1. CI 测试 (`ci.yml`)

**触发条件：**
- `main` 和 `develop` 分支的 `push` 事件
- `main` 分支的 `pull_request` 事件

**功能：**
- 🧪 多 Python 版本测试 (3.8-3.12)
- 🔍 代码格式检查 (black, ruff)
- 📝 类型检查 (mypy)
- ✅ 单元测试 (pytest)
- 📊 代码覆盖率报告 (codecov)
- 🏗️ 包构建验证
- 📦 示例代码测试

### 2. PyPI 发布 (`publish.yml`)

**触发条件：**
- GitHub Release 发布时自动触发
- 手动触发 (workflow_dispatch)

**功能：**
- 🚀 自动从 Release 标签获取版本号
- 📦 构建和检查包
- 🎯 智能发布目标选择：
  - 预发布 Release → 测试 PyPI
  - 正式 Release → 正式 PyPI
- 📝 完整的发布日志

## 🚀 使用方法

### 自动发布（推荐）

使用 `gh CLI` 发布脚本：

```bash
# 发布到测试 PyPI（预发布版本）
./scripts/publish.sh 0.2.1 --test

# 发布到正式 PyPI
./scripts/publish.sh 0.2.1

# 发布预发布版本
./scripts/publish.sh 0.2.1-beta.1 --prerelease
```

**工作流程：**
1. 脚本更新版本号并提交
2. 创建 GitHub Release
3. Release 自动触发 PyPI 发布工作流
4. 根据 Release 类型选择发布目标

### 手动触发

1. 访问 GitHub Actions 页面
2. 选择 "发布到 PyPI" 工作流
3. 点击 "Run workflow"
4. 输入版本号和选择发布目标

## ⚙️ 配置要求

### GitHub Secrets

在仓库设置中配置以下 Secrets：

| Secret 名称 | 用途 | 获取方式 |
|------------|------|----------|
| `PYPI_API_TOKEN` | 正式 PyPI 发布 | [PyPI Account Settings](https://pypi.org/manage/account/) |
| `TEST_PYPI_API_TOKEN` | 测试 PyPI 发布 | [TestPyPI Account Settings](https://test.pypi.org/manage/account/) |

### API Token 获取步骤

1. 访问 PyPI/TestPyPI 账户设置
2. 点击 "Add API token"
3. 设置 Token 名称（如 `yai-loguru-sinks-github-actions`）
4. 选择 Scope 为 "Entire account" 或特定项目
5. 复制生成的 Token 并添加到 GitHub Secrets

## 📊 工作流状态

可以在 README 中添加状态徽章：

```markdown
![CI](https://github.com/yai-nexus/loguru-suite/workflows/CI/badge.svg)
![PyPI Publish](https://github.com/yai-nexus/loguru-suite/workflows/发布到%20PyPI/badge.svg)
```

## 🔧 故障排除

### 常见问题

1. **PyPI 发布失败**
   - 检查 API Token 是否正确配置
   - 确认版本号未重复
   - 查看工作流日志获取详细错误信息

2. **测试失败**
   - 检查代码格式是否符合 black/ruff 标准
   - 确认类型注解是否正确
   - 查看测试日志定位具体失败原因

3. **包构建失败**
   - 检查 `pyproject.toml` 配置
   - 确认依赖版本兼容性
   - 验证包结构是否正确

### 调试步骤

1. **查看工作流日志**
   ```bash
   # 使用 gh CLI 查看最近的工作流运行
   gh run list
   gh run view [run-id]
   ```

2. **本地复现问题**
   ```bash
   # 运行 CI 检查
   cd packages/yai-loguru-sinks
   uv run black --check .
   uv run ruff check .
   uv run mypy .
   uv run pytest
   
   # 构建包
   uv build
   uv run --with twine twine check dist/*
   ```

3. **测试发布流程**
   ```bash
   # 测试发布到 TestPyPI
   ./scripts/publish.sh 0.2.1-test --test
   ```

## 📚 最佳实践

1. **版本管理**
   - 使用语义化版本 (SemVer)
   - 预发布版本使用 `-alpha`, `-beta`, `-rc` 后缀
   - 先发布到 TestPyPI 验证

2. **发布流程**
   - 确保所有测试通过
   - 更新文档和示例
   - 创建详细的 Release Notes
   - 验证发布后的包可正常安装使用

3. **安全考虑**
   - 定期轮换 API Token
   - 使用最小权限原则
   - 监控发布活动

## 🔗 相关文档

- [PyPI 发布指南](../docs/PYPI_PUBLISH.md)
- [发布脚本说明](../scripts/publish.sh)
- [GitHub Actions 官方文档](https://docs.github.com/en/actions)