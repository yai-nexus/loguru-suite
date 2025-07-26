#!/bin/bash

# Basic Demo 安装和运行脚本
# 用于快速安装依赖并启动 basic-demo 示例

set -e

echo "🚀 启动 Basic Demo..."
echo "================================"

# 检查是否在正确的目录
if [ ! -f "main.py" ]; then
    echo "❌ 错误：请在 basic-demo 目录下运行此脚本"
    exit 1
fi

# 创建日志目录
mkdir -p logs

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 python3，请先安装 Python"
    exit 1
fi

# 检查 uv 工具
if ! command -v uv &> /dev/null; then
    echo "❌ 错误：未找到 uv，请先安装 uv"
    echo "💡 提示：curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 安装依赖
echo "📦 安装依赖..."
if [ -f "pyproject.toml" ]; then
    uv sync
else
    echo "⚠️ 警告：未找到 pyproject.toml，跳过依赖安装"
fi

# 检查依赖
echo "🔍 检查依赖..."
if ! uv run python -c "import yai_loguru_sinks" 2>/dev/null; then
    echo "⚠️ 警告：未找到 yai-loguru-sinks，请确保已安装"
    echo "💡 提示：请在项目根目录运行 'uv sync' 安装依赖"
    echo ""
fi

# 运行示例
echo "▶️ 运行示例..."
uv run main.py

echo ""
echo "✅ 示例运行完成！"
echo "📁 日志文件位置：logs/basic-demo.log"