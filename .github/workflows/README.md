# GitHub Actions 工作流

本目录包含 `yai-loguru-sinks` 项目的 GitHub Actions 工作流配置。

## 工作流概览

### 1. CI 测试 (`ci.yml`)

**触发条件：**
- 推送到 `main` 或 `develop` 分支
- 针对 `main` 分支的 Pull Request

**功能：**
- 多 Python 版本测试 (3.8-3.12)
- 代码格式检查 (black, ruff)
- 类型检查 (mypy)
- 单元测试和覆盖率报告
- 示例代码测试
- 包构建验证

### 2. PyPI 发布 (`publish.yml`)

**触发条件：**
- 推送以 `v` 开头的标签 (如 `v0.2.1`)
- 手动触发 (`workflow_dispatch`)

**功能：**
- 自动更新版本号
- 构建和验证包
- 发布到 TestPyPI 或正式 PyPI
- 创建 GitHub Release
- 支持测试模式

## 使用方法

### 自动发布

1. **使用发布脚本（推荐）：**
   ```bash
   ./scripts/publish.sh 0.2.1 --github
   ```

2. **手动推送标签：**
   ```bash
   git tag v0.2.1
   git push origin v0.2.1
   ```

### 手动触发发布

1. 访问 GitHub Actions 页面
2. 选择 "发布到 PyPI" 工作流
3. 点击 "Run workflow"
4. 填写参数：
   - `version`: 版本号 (如 `0.2.1`)
   - `test_pypi`: 是否发布到测试 PyPI

## 配置要求

### GitHub Secrets

在仓库设置中配置以下 Secrets：

| Secret 名称 | 描述 | 必需 |
|------------|------|------|
| `PYPI_API_TOKEN` | PyPI API Token | ✅ |
| `TEST_PYPI_API_TOKEN` | TestPyPI API Token | ❌ |

### 获取 API Token

1. 访问 [PyPI Account Settings](https://pypi.org/manage/account/)
2. 点击 "Add API token"
3. 设置名称：`yai-loguru-sinks-github-actions`
4. 选择 Scope：`Entire account` 或项目特定
5. 复制 Token 并添加到 GitHub Secrets

## 工作流状态

### CI 状态徽章

```markdown
[![CI](https://github.com/yai-nexus/loguru-suite/actions/workflows/ci.yml/badge.svg)](https://github.com/yai-nexus/loguru-suite/actions/workflows/ci.yml)
```

### 发布状态徽章

```markdown
[![PyPI](https://github.com/yai-nexus/loguru-suite/actions/workflows/publish.yml/badge.svg)](https://github.com/yai-nexus/loguru-suite/actions/workflows/publish.yml)
```

## 故障排除

### 常见问题

1. **发布失败：认证错误**
   - 检查 `PYPI_API_TOKEN` 是否正确配置
   - 确认 Token 权限范围

2. **CI 失败：依赖安装**
   - 检查 `pyproject.toml` 依赖配置
   - 确认 Python 版本兼容性

3. **版本冲突**
   - 确保版本号唯一
   - 检查是否已存在相同版本

### 调试步骤

1. 查看工作流日志
2. 检查 Secrets 配置
3. 验证权限设置
4. 本地测试构建

## 最佳实践

1. **发布前测试**：先发布到 TestPyPI
2. **版本管理**：遵循语义化版本规范
3. **代码质量**：确保 CI 通过后再发布
4. **文档更新**：发布前更新相关文档

## 相关文档

- [PyPI 发布指南](../docs/PYPI_PUBLISH.md)
- [发布脚本说明](../scripts/publish.sh)
- [项目文档](../README.md)