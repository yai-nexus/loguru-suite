#!/bin/bash

# yai-loguru-sinks 发布脚本
# 用法: ./scripts/publish.sh [version] [--test] [--github]

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
GITHUB_MODE=""

for arg in "$@"; do
    case $arg in
        --test)
            TEST_MODE="--repository testpypi"
            echo -e "${YELLOW}测试模式：将发布到 TestPyPI${NC}"
            ;;
        --github)
            GITHUB_MODE="true"
            echo -e "${BLUE}GitHub 模式：将触发 GitHub Actions${NC}"
            ;;
    esac
done

if [[ -z "$VERSION" ]]; then
    echo -e "${RED}错误：请提供版本号${NC}"
    echo "用法: $0 <version> [--test] [--github]"
    echo "示例: $0 0.2.1"
    echo "示例: $0 0.2.1 --test"
    echo "示例: $0 0.2.1 --github"
    exit 1
fi

echo "目标版本: $VERSION"
echo "包目录: $PACKAGE_DIR"

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

# 创建标签
echo -e "${BLUE}创建 Git 标签...${NC}"
git tag -a "v$VERSION" -m "Release v$VERSION"

# 推送到远程
echo -e "${BLUE}推送到远程仓库...${NC}"
git push origin main

if [[ "$GITHUB_MODE" == "true" ]]; then
    # GitHub Actions 模式
    echo -e "${BLUE}推送标签以触发 GitHub Actions...${NC}"
    git push origin "v$VERSION"
    echo -e "${GREEN}GitHub Actions 已触发！${NC}"
    echo "请访问 https://github.com/yai-nexus/loguru-suite/actions 查看发布进度"
else
    # 本地发布模式
    git push origin "v$VERSION"
    
    # 构建包
    echo -e "${BLUE}构建包...${NC}"
    cd "$PACKAGE_DIR"
    uv build

    # 发布到 PyPI
    echo -e "${BLUE}发布到 PyPI...${NC}"
    if [[ -n "$TEST_MODE" ]]; then
        echo -e "${YELLOW}发布到 TestPyPI...${NC}"
        uv publish $TEST_MODE
    else
        echo -e "${GREEN}发布到正式 PyPI...${NC}"
        echo -e "${YELLOW}请确保已配置 PyPI 认证信息${NC}"
        uv publish
    fi
fi

echo -e "${GREEN}发布完成！${NC}"
echo "版本: $VERSION"
echo "标签: v$VERSION"

if [[ "$GITHUB_MODE" == "true" ]]; then
    echo -e "${BLUE}GitHub Actions 信息:${NC}"
    echo "- 工作流将自动构建和发布包"
    echo "- 将自动创建 GitHub Release"
    echo "- 查看进度: https://github.com/yai-nexus/loguru-suite/actions"
elif [[ -n "$TEST_MODE" ]]; then
    echo -e "${YELLOW}测试安装命令:${NC}"
    echo "pip install --index-url https://test.pypi.org/simple/ yai-loguru-sinks==$VERSION"
else
    echo -e "${GREEN}安装命令:${NC}"
    echo "pip install yai-loguru-sinks==$VERSION"
fi