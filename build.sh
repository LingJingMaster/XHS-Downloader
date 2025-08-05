#!/bin/bash

# XHS-Downloader macOS/Linux 构建脚本

set -e

echo "🚀 XHS-Downloader macOS/Linux 构建脚本"
echo "========================================"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python 3.12"
    echo "macOS: brew install python@3.12"
    echo "Ubuntu: sudo apt-get install python3.12"
    exit 1
fi

echo "✅ Python 版本: $(python3 --version)"

# 检查系统架构
echo "🖥️  系统信息: $(uname -s) $(uname -m)"

# 安装依赖
echo "📦 安装项目依赖..."
python3 -m pip install -r requirements.txt

# 运行构建
echo "🔨 开始构建..."
python3 build.py

echo ""
echo "✅ 构建完成！"
echo "📁 可执行文件位置: dist/XHS-Downloader"
echo ""
echo "使用方法:"
echo "  ./dist/XHS-Downloader          # GUI 模式"
echo "  ./dist/XHS-Downloader server   # 服务器模式"
echo ""