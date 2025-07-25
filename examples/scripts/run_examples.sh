#!/bin/bash

# yai-loguru-sinks 示例运行脚本

set -e

# 获取脚本所在目录的父目录（examples 目录）
EXAMPLES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "yai-loguru-sinks 示例运行脚本"
echo "=================================="
echo "示例目录: $EXAMPLES_DIR"
echo ""

# 切换到 examples 目录
cd "$EXAMPLES_DIR"

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "正在创建虚拟环境..."
    uv venv
fi

# 安装依赖
echo "正在安装依赖..."
uv sync

# 运行示例
echo ""
echo "运行示例代码..."
echo "=================================="
uv run python src/usage_example.py

echo ""
echo "示例运行完成！"
echo "日志文件位置: $EXAMPLES_DIR/logs/"