#!/bin/bash

echo "🚀 开始安装 loguru-suite 开发环境..."

# 创建虚拟环境
echo "📦 创建虚拟环境..."
uv venv

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source .venv/bin/activate

# 安装workspace中的所有包
echo "📚 安装所有包..."
uv sync

echo "✅ 安装完成！"
echo "💡 使用 'source .venv/bin/activate' 激活虚拟环境"
echo "🧪 使用 './scripts/run-example.sh' 运行示例"