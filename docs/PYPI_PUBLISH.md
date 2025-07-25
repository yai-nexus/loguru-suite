# PyPI 发布指南

## 准备工作

### 1. 配置 PyPI 认证

#### 方法一：使用 API Token（推荐）
1. 访问 [PyPI Account Settings](https://pypi.org/manage/account/)
2. 创建 API Token
3. 配置环境变量：
```bash
export UV_PUBLISH_USERNAME="__token__"
export UV_PUBLISH_PASSWORD="your-api-token"
```

#### 方法二：使用用户名密码
```bash
export UV_PUBLISH_USERNAME="your-username"
export UV_PUBLISH_PASSWORD="your-password"
```

### 2. 测试发布（可选）
首先发布到 TestPyPI 进行测试：
```bash
./scripts/publish.sh 0.2.1 --test
```

## 发布流程

### 自动发布（推荐）
使用发布脚本：
```bash
# 发布新版本
./scripts/publish.sh 0.2.1

# 测试发布
./scripts/publish.sh 0.2.1 --test
```

### 手动发布
1. 更新版本号：
```bash
cd packages/yai-loguru-sinks
# 编辑 pyproject.toml 中的 version
```

2. 构建包：
```bash
uv build
```

3. 发布：
```bash
# 发布到正式 PyPI
uv publish

# 发布到测试 PyPI
uv publish --repository testpypi
```

4. 提交和标签：
```bash
git add .
git commit -m "bump: 更新版本到 x.x.x"
git tag -a vx.x.x -m "Release vx.x.x"
git push origin main
git push origin vx.x.x
```

## 验证发布

### 检查 PyPI 页面
- 正式版本：https://pypi.org/project/yai-loguru-sinks/
- 测试版本：https://test.pypi.org/project/yai-loguru-sinks/

### 测试安装
```bash
# 从正式 PyPI 安装
pip install yai-loguru-sinks==x.x.x

# 从测试 PyPI 安装
pip install --index-url https://test.pypi.org/simple/ yai-loguru-sinks==x.x.x
```

## 版本管理

### 语义化版本
- **主版本号**：不兼容的 API 修改
- **次版本号**：向下兼容的功能性新增
- **修订号**：向下兼容的问题修正

### 版本示例
- `0.1.0` - 初始版本
- `0.2.0` - 重大重构（当前版本）
- `0.2.1` - Bug 修复
- `0.3.0` - 新功能添加
- `1.0.0` - 稳定版本

## 故障排除

### 常见错误

1. **认证失败**
```
HTTP Error 403: Invalid or non-existent authentication information
```
解决：检查 UV_PUBLISH_USERNAME 和 UV_PUBLISH_PASSWORD 环境变量

2. **版本已存在**
```
HTTP Error 400: File already exists
```
解决：更新版本号，PyPI 不允许重复上传相同版本

3. **包名冲突**
```
HTTP Error 403: The user 'xxx' isn't allowed to upload to project 'xxx'
```
解决：检查包名是否已被占用，或确认你有上传权限

### 调试命令
```bash
# 检查包信息
uv build --verbose

# 检查包内容
tar -tzf dist/yai_loguru_sinks-x.x.x.tar.gz
unzip -l dist/yai_loguru_sinks-x.x.x-py3-none-any.whl
```