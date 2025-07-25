# PyPI 发布指南

本文档详细说明如何将 `yai-loguru-sinks` 包发布到 PyPI。

## 🚀 推荐方式：GitHub Release 自动发布

### 1. 配置 GitHub Secrets

在 GitHub 仓库设置中添加以下 Secrets：

- `PYPI_API_TOKEN`: 正式 PyPI 的 API Token
- `TEST_PYPI_API_TOKEN`: 测试 PyPI 的 API Token

### 2. 获取 PyPI API Token

#### 正式 PyPI (pypi.org)
1. 访问 https://pypi.org/account/login/
2. 登录后进入 Account settings
3. 点击 "Add API token"
4. 选择 "Entire account" 或特定项目
5. 复制生成的 token

#### 测试 PyPI (test.pypi.org)
1. 访问 https://test.pypi.org/account/login/
2. 重复上述步骤

### 3. 发布方式

#### 方式一：使用 gh CLI 发布脚本（推荐）

```bash
# 发布到测试 PyPI（预发布版本）
./scripts/publish.sh 0.2.1 --test

# 发布到正式 PyPI
./scripts/publish.sh 0.2.1

# 发布预发布版本到正式 PyPI
./scripts/publish.sh 0.2.1-beta.1 --prerelease
```

**工作流程：**
1. 脚本更新版本号并提交到 Git
2. 使用 `gh release create` 创建 GitHub Release
3. GitHub Release 自动触发 PyPI 发布工作流
4. 根据 Release 类型自动选择发布目标：
   - 预发布版本 → 测试 PyPI
   - 正式版本 → 正式 PyPI

#### 方式二：GitHub Actions 页面手动触发

1. 访问 GitHub 仓库的 Actions 页面
2. 选择 "发布到 PyPI" 工作流
3. 点击 "Run workflow"
4. 输入版本号和选择发布目标

### 4. 发布触发机制

- **GitHub Release 发布时自动触发**：
  - 正式 Release → 发布到正式 PyPI
  - 预发布 Release → 发布到测试 PyPI
- **手动触发**：可在 GitHub Actions 页面手动运行

### 5. 工作流功能

- ✅ 自动从 Release 标签获取版本号
- ✅ 构建和检查包
- ✅ 根据 Release 类型自动选择发布目标
- ✅ 发布到 PyPI/TestPyPI
- ✅ 完整的发布日志和状态反馈

### 2. 本地发布

如果需要本地发布，请按以下步骤操作。

#### 配置认证

**方式一：环境变量（推荐）**
```bash
export UV_PUBLISH_USERNAME="__token__"
export UV_PUBLISH_PASSWORD="pypi-your-api-token-here"
```

**方式二：交互式输入**
发布时会提示输入用户名和密码。

#### 发布流程

**测试发布（推荐先测试）**
```bash
./scripts/publish.sh 0.2.1 --test
```

**正式发布**
```bash
./scripts/publish.sh 0.2.1
```

## 发布验证

### 1. 检查 PyPI 页面

- 正式版本: https://pypi.org/project/yai-loguru-sinks/
- 测试版本: https://test.pypi.org/project/yai-loguru-sinks/

### 2. 测试安装

**从正式 PyPI 安装**
```bash
pip install yai-loguru-sinks==0.2.1
```

**从测试 PyPI 安装**
```bash
pip install --index-url https://test.pypi.org/simple/ yai-loguru-sinks==0.2.1
```

### 3. 验证功能

```python
from yai_loguru_sinks import SinkFactory
from loguru import logger

# 创建文件 sink
sink = SinkFactory.create_file_sink("test.log")
logger.add(sink)
logger.info("测试消息")
```

## 版本管理

### 语义化版本

遵循 [Semantic Versioning](https://semver.org/) 规范：

- `MAJOR.MINOR.PATCH` (如 `1.2.3`)
- `MAJOR`: 不兼容的 API 更改
- `MINOR`: 向后兼容的功能添加
- `PATCH`: 向后兼容的错误修复

### 版本示例

```bash
# 补丁版本（错误修复）
./scripts/publish.sh 0.2.1 --github

# 次要版本（新功能）
./scripts/publish.sh 0.3.0 --github

# 主要版本（破坏性更改）
./scripts/publish.sh 1.0.0 --github
```

## 故障排除

### 常见错误

**1. 版本已存在**
```
ERROR: File already exists
```
解决方案：更新版本号

**2. 认证失败**
```
ERROR: Invalid credentials
```
解决方案：检查 API Token 是否正确配置

**3. 包验证失败**
```
ERROR: Invalid distribution
```
解决方案：运行 `uv run twine check dist/*` 检查包

### 调试命令

```bash
# 检查包内容
cd packages/yai-loguru-sinks
uv build
uv run twine check dist/*

# 查看包信息
tar -tzf dist/yai_loguru_sinks-*.tar.gz

# 测试本地安装
pip install dist/yai_loguru_sinks-*.whl
```

### GitHub Actions 调试

1. 查看工作流日志：`Actions` > `发布到 PyPI`
2. 检查 Secrets 配置：`Settings` > `Secrets and variables`
3. 验证权限：确保 Actions 有写入权限

## 发布检查清单

发布前请确认：

- [ ] 代码已提交并推送到 main 分支
- [ ] 所有测试通过
- [ ] 版本号符合语义化版本规范
- [ ] CHANGELOG.md 已更新（如果存在）
- [ ] GitHub Secrets 已正确配置
- [ ] 先在 TestPyPI 测试发布

## 自动化发布流程

推荐的完整发布流程：

1. **开发完成**：确保所有功能完成并测试通过
2. **测试发布**：`./scripts/publish.sh 0.2.1 --test --github`
3. **验证测试**：从 TestPyPI 安装并测试
4. **正式发布**：`./scripts/publish.sh 0.2.1 --github`
5. **发布验证**：检查 PyPI 页面和 GitHub Release

这样可以确保发布的包质量和可靠性。