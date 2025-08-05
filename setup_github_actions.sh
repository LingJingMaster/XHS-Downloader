#!/bin/bash

# GitHub Actions 设置脚本

echo "🚀 设置 GitHub Actions 自动构建"
echo "================================="

# 检查是否在 git 仓库中
if [ ! -d ".git" ]; then
    echo "❌ 当前目录不是 Git 仓库，请先初始化："
    echo "   git init"
    echo "   git remote add origin https://github.com/用户名/仓库名.git"
    exit 1
fi

echo "✅ 检测到 Git 仓库"

# 检查 GitHub Actions 文件
if [ -f ".github/workflows/build-releases.yml" ]; then
    echo "✅ GitHub Actions 配置文件已存在"
else
    echo "❌ 未找到 GitHub Actions 配置文件"
    exit 1
fi

# 添加到 .gitignore
echo ""
echo "📝 更新 .gitignore 文件..."
if [ -f ".gitignore" ]; then
    if ! grep -q "# PyInstaller 构建目录" .gitignore; then
        echo "" >> .gitignore
        cat .gitignore_build >> .gitignore
        echo "✅ 已添加构建排除规则到 .gitignore"
    else
        echo "ℹ️  .gitignore 已包含构建排除规则"
    fi
else
    cp .gitignore_build .gitignore
    echo "✅ 已创建 .gitignore 文件"
fi

# 提交文件
echo ""
echo "📤 提交 GitHub Actions 配置..."
git add .github/ *.md build.* xhs_downloader.spec .gitignore

if git diff --cached --quiet; then
    echo "ℹ️  没有新文件需要提交"
else
    git commit -m "🤖 添加 GitHub Actions 自动构建配置

- 支持 Windows x64 和 macOS (ARM64/Intel) 构建
- 自动创建 GitHub Release
- 包含 SHA256 校验文件
- 提供完整的构建文档"
    
    echo "✅ 已提交配置文件"
    echo ""
    echo "🚀 下一步操作："
    echo "1. 推送到 GitHub: git push origin master"
    echo "2. 进入 GitHub 仓库页面"
    echo "3. 点击 Actions → 构建可执行文件 → Run workflow"
    echo ""
    echo "🎉 首次构建完成后，您将获得："
    echo "   • Windows 可执行文件 (.exe)"
    echo "   • macOS ARM64 可执行文件"  
    echo "   • macOS x64 可执行文件"
    echo "   • 自动创建的 GitHub Release"
fi