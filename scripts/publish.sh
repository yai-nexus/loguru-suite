#!/bin/bash

# yai-loguru-sinks 发布脚本
# 用法: ./scripts/publish.sh [version] [--test] [--prerelease]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PACKAGE_DIR="$PROJECT_ROOT/packages/yai-loguru-sinks"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}yai-loguru-sinks 发布脚本${NC}"
echo "=================================="

# 检查参数
VERSION=$1
TEST_MODE=""
PRERELEASE=""

for arg in "$@"; do
    case $arg in
        --test)
            TEST_MODE="true"
            echo -e "${YELLOW}测试模式：将发布到 TestPyPI${NC}"
            ;;
        --prerelease)
            PRERELEASE="--prerelease"
            echo -e "${YELLOW}预发布模式：将标记为预发布版本${NC}"
            ;;
    esac
done

if [[ -z "$VERSION" ]]; then
    echo -e "${RED}错误：请提供版本号${NC}"
    echo "用法: $0 <version> [--test] [--prerelease]"
    echo "示例: $0 0.2.1"
    echo "示例: $0 0.2.1 --test"
    echo "示例: $0 0.3.0-beta.1 --prerelease"
    exit 1
fi

echo "目标版本: $VERSION"
echo "包目录: $PACKAGE_DIR"

# 检查 gh CLI 是否安装
if ! command -v gh &> /dev/null; then
    echo -e "${RED}错误：未找到 gh CLI，请先安装${NC}"
    echo "安装命令: brew install gh"
    exit 1
fi

# 检查 gh 认证状态
if ! gh auth status &> /dev/null; then
    echo -e "${RED}错误：gh CLI 未认证，请先登录${NC}"
    echo "登录命令: gh auth login"
    exit 1
fi

# 检查工作目录是否干净
cd "$PROJECT_ROOT"
if [[ -n $(git status --porcelain) ]]; then
    echo -e "${RED}错误：工作目录不干净，请先提交所有更改${NC}"
    git status --short
    exit 1
fi

# 更新版本号
echo -e "${BLUE}更新版本号到 $VERSION...${NC}"
cd "$PACKAGE_DIR"
sed -i '' "s/version = \".*\"/version = \"$VERSION\"/" pyproject.toml

# 提交版本更新
cd "$PROJECT_ROOT"
git add "$PACKAGE_DIR/pyproject.toml"
git commit -m "bump: 更新 yai-loguru-sinks 版本到 $VERSION"

# 推送到远程
echo -e "${BLUE}推送到远程仓库...${NC}"
git push origin main

# 生成发布说明
RELEASE_NOTES_FILE="/tmp/release-notes-$VERSION.md"
cat > "$RELEASE_NOTES_FILE" << EOF
## yai-loguru-sinks v$VERSION

### 🚀 新功能
- 基于 sink 工厂的架构设计
- 支持多种 sink 类型（文件、控制台、JSON、自定义）
- 配置驱动的 sink 管理
- 协议解析器支持

### 📦 安装

\`\`\`bash
pip install yai-loguru-sinks==$VERSION
\`\`\`

### 🔧 使用示例

\`\`\`python
from yai_loguru_sinks import SinkFactory
from loguru import logger

# 创建文件 sink
sink = SinkFactory.create_file_sink("app.log")
logger.add(sink)
logger.info("Hello, World!")
\`\`\`

### 📚 文档

- [使用指南](https://github.com/yai-nexus/loguru-suite/tree/main/packages/yai-loguru-sinks)
- [示例代码](https://github.com/yai-nexus/loguru-suite/tree/main/examples)

### 🔗 相关链接

- [PyPI 页面](https://pypi.org/project/yai-loguru-sinks/$VERSION/)
- [更新日志](https://github.com/yai-nexus/loguru-suite/releases)
EOF

# 使用 gh CLI 创建 Release
echo -e "${BLUE}创建 GitHub Release...${NC}"
if [[ "$TEST_MODE" == "true" ]]; then
    # 测试模式：直接发布 Release（标记为测试版本）
    gh release create "v$VERSION" \
        --title "yai-loguru-sinks v$VERSION (Test)" \
        --notes-file "$RELEASE_NOTES_FILE" \
        $PRERELEASE
    echo -e "${GREEN}测试 Release 已发布！${NC}"
    echo "这将自动触发 TestPyPI 发布工作流"
else
    # 正式模式：直接发布 Release
    gh release create "v$VERSION" \
        --title "yai-loguru-sinks v$VERSION" \
        --notes-file "$RELEASE_NOTES_FILE" \
        $PRERELEASE
    echo -e "${GREEN}GitHub Release 已发布！${NC}"
    echo "这将自动触发 PyPI 发布工作流"
fi

# 清理临时文件
rm -f "$RELEASE_NOTES_FILE"

echo -e "${GREEN}发布完成！${NC}"
echo "版本: $VERSION"
echo "Release: https://github.com/yai-nexus/loguru-suite/releases/tag/v$VERSION"

if [[ "$TEST_MODE" == "true" ]]; then
    echo -e "${YELLOW}测试模式信息:${NC}"
    echo "- GitHub Release 已自动发布"
    echo "- TestPyPI 发布工作流已自动触发"
    echo "- 查看进度: https://github.com/yai-nexus/loguru-suite/actions"
    echo "- 测试安装: pip install --index-url https://test.pypi.org/simple/ yai-loguru-sinks==$VERSION"
else
    echo -e "${BLUE}自动化信息:${NC}"
    echo "- GitHub Release 已自动发布"
    echo "- PyPI 发布工作流已自动触发"
    echo "- 查看进度: https://github.com/yai-nexus/loguru-suite/actions"
    echo "- 安装命令: pip install yai-loguru-sinks==$VERSION"
fi