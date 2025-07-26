#!/bin/bash

# Enterprise Demo 安装和运行脚本
# 用于快速安装依赖并启动 enterprise-demo 示例

set -e

echo "🏢 启动 Enterprise Demo..."
echo "================================"

# 检查是否在正确的目录
if [ ! -f "main.py" ]; then
    echo "❌ 错误：请在 enterprise-demo 目录下运行此脚本"
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

# 检查环境变量配置
echo "🔍 检查 SLS 配置..."
if [ -f ".env" ]; then
    echo "✅ 找到 .env 文件，加载环境变量"
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️ 未找到 .env 文件"
    echo "💡 提示：复制 .env.example 为 .env 并配置 SLS 信息以启用云日志功能"
    echo ""
fi

# 检查依赖
echo "🔍 检查依赖..."
if ! python3 -c "import yai_loguru_sinks" 2>/dev/null; then
    echo "⚠️ 警告：未找到 yai-loguru-sinks，请确保已安装"
    echo "💡 提示：请在项目根目录运行 'uv sync' 安装依赖"
    echo ""
fi

# 运行示例
echo "▶️ 运行示例..."
python3 main.py

echo ""
echo "✅ 示例运行完成！"
echo "📁 本地日志文件：logs/enterprise-demo.log"
if [ -f ".env" ]; then
    echo "☁️ 如果配置正确，日志已发送到阿里云 SLS"
fi