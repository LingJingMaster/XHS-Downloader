#!/usr/bin/env python3
"""
XHS-Downloader 构建脚本
支持 Windows 和 ARM macOS 编译
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_pyinstaller():
    """检查 PyInstaller 是否安装"""
    try:
        import PyInstaller
        print(f"✅ PyInstaller 已安装，版本: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("❌ PyInstaller 未安装")
        return False

def install_pyinstaller():
    """安装 PyInstaller"""
    print("正在安装 PyInstaller...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "build_requirements.txt"], 
                      check=True)
        print("✅ PyInstaller 安装成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ PyInstaller 安装失败")
        return False

def clean_build():
    """清理构建目录"""
    print("清理构建目录...")
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            import shutil
            shutil.rmtree(dir_name)
            print(f"✅ 已清理 {dir_name} 目录")

def build_executable():
    """构建可执行文件"""
    print("开始构建可执行文件...")
    
    # 获取系统信息
    system = platform.system()
    machine = platform.machine()
    
    print(f"🖥️  系统: {system}")
    print(f"🏗️  架构: {machine}")
    
    try:
        # 使用 spec 文件构建
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "xhs_downloader.spec"]
        subprocess.run(cmd, check=True)
        
        # 检查输出文件
        dist_dir = Path("dist")
        if system == "Windows":
            exe_file = dist_dir / "XHS-Downloader.exe"
        else:
            exe_file = dist_dir / "XHS-Downloader"
            
        if exe_file.exists():
            file_size = exe_file.stat().st_size / (1024 * 1024)  # MB
            print(f"✅ 构建成功!")
            print(f"📁 输出文件: {exe_file}")
            print(f"📊 文件大小: {file_size:.1f} MB")
            
            # 在 macOS 上设置执行权限
            if system != "Windows":
                os.chmod(exe_file, 0o755)
                print("✅ 已设置执行权限")
                
            return True
        else:
            print("❌ 构建失败，未找到输出文件")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False

def create_release_info():
    """创建发布信息文件"""
    system = platform.system()
    machine = platform.machine()
    
    # 确定平台标识
    if system == "Windows":
        platform_name = "windows-x64"
    elif system == "Darwin":
        if machine == "arm64":
            platform_name = "macos-arm64"
        else:
            platform_name = "macos-x64"
    else:
        platform_name = f"{system.lower()}-{machine}"
    
    dist_dir = Path("dist")
    info_file = dist_dir / f"XHS-Downloader-{platform_name}-info.txt"
    
    with open(info_file, "w", encoding="utf-8") as f:
        f.write(f"XHS-Downloader 可执行文件\n")
        f.write(f"===================\n\n")
        f.write(f"平台: {system} {machine}\n")
        f.write(f"构建时间: {subprocess.check_output(['date'], text=True).strip()}\n")
        f.write(f"Python 版本: {sys.version}\n\n")
        f.write(f"使用方法:\n")
        if system == "Windows":
            f.write(f"1. 双击 XHS-Downloader.exe 启动程序\n")
            f.write(f"2. 或在命令行中运行: XHS-Downloader.exe\n")
            f.write(f"3. 服务器模式: XHS-Downloader.exe server\n")
        else:
            f.write(f"1. 在终端中运行: ./XHS-Downloader\n")
            f.write(f"2. 服务器模式: ./XHS-Downloader server\n")
        f.write(f"\n注意事项:\n")
        f.write(f"- 首次运行时，程序会创建必要的配置文件\n")
        f.write(f"- 确保网络连接正常\n")
        f.write(f"- 支持的功能请参考项目文档\n")
    
    print(f"✅ 已创建发布信息: {info_file}")

def main():
    print("🚀 XHS-Downloader 构建工具")
    print("=" * 40)
    
    # 检查并安装 PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            sys.exit(1)
    
    # 清理构建目录
    clean_build()
    
    # 构建可执行文件
    if build_executable():
        create_release_info()
        print("\n🎉 构建完成!")
        print("📁 输出目录: dist/")
    else:
        print("\n❌ 构建失败!")
        sys.exit(1)

if __name__ == "__main__":
    main()