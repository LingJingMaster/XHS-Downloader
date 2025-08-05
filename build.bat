@echo off
chcp 65001 >nul
echo 🚀 XHS-Downloader Windows 构建脚本
echo ========================================

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 Python，请先安装 Python 3.12
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 安装依赖
echo 📦 安装项目依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

REM 运行构建
echo 🔨 开始构建...
python build.py
if errorlevel 1 (
    echo ❌ 构建失败
    pause
    exit /b 1
)

echo.
echo ✅ 构建完成！
echo 📁 可执行文件位置: dist\XHS-Downloader.exe
echo.
pause