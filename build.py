#!/usr/bin/env python3
"""
XHS-Downloader Build Script
Supports Windows and ARM macOS compilation
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print(f"[OK] PyInstaller installed, version: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("[ERROR] PyInstaller not installed")
        return False

def install_pyinstaller():
    """Install PyInstaller"""
    print("Installing PyInstaller...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller>=6.0.0"], 
                      check=True)
        print("[OK] PyInstaller installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to install PyInstaller")
        return False

def clean_build():
    """Clean build directories"""
    print("Cleaning build directories...")
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            import shutil
            shutil.rmtree(dir_name)
            print(f"[OK] Cleaned {dir_name} directory")

def build_executable():
    """Build executable file"""
    print("Starting executable build...")
    
    # Get system information
    system = platform.system()
    machine = platform.machine()
    
    print(f"[INFO] System: {system}")
    print(f"[INFO] Architecture: {machine}")
    
    try:
        # Build using spec file
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "xhs_downloader.spec"]
        subprocess.run(cmd, check=True)
        
        # Check output file
        dist_dir = Path("dist")
        if system == "Windows":
            exe_file = dist_dir / "XHS-Downloader.exe"
        else:
            exe_file = dist_dir / "XHS-Downloader"
            
        if exe_file.exists():
            file_size = exe_file.stat().st_size / (1024 * 1024)  # MB
            print(f"[OK] Build successful!")
            print(f"[INFO] Output file: {exe_file}")
            print(f"[INFO] File size: {file_size:.1f} MB")
            
            # Set executable permissions on macOS/Linux
            if system != "Windows":
                os.chmod(exe_file, 0o755)
                print("[OK] Set executable permissions")
                
            return True
        else:
            print("[ERROR] Build failed, output file not found")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build failed: {e}")
        return False

def create_release_info():
    """Create release information file"""
    system = platform.system()
    machine = platform.machine()
    
    # Determine platform identifier
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
        f.write(f"XHS-Downloader Executable\n")
        f.write(f"========================\n\n")
        f.write(f"Platform: {system} {machine}\n")
        import datetime
        build_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Build Time: {build_time}\n")
        f.write(f"Python Version: {sys.version}\n\n")
        f.write(f"Usage:\n")
        if system == "Windows":
            f.write(f"1. Double-click XHS-Downloader.exe to start\n")
            f.write(f"2. Or run in command line: XHS-Downloader.exe\n")
            f.write(f"3. Server mode: XHS-Downloader.exe server\n")
        else:
            f.write(f"1. Run in terminal: ./XHS-Downloader\n")
            f.write(f"2. Server mode: ./XHS-Downloader server\n")
        f.write(f"\nNotes:\n")
        f.write(f"- Configuration files will be created on first run\n")
        f.write(f"- Ensure network connection is available\n")
        f.write(f"- See project documentation for supported features\n")
    
    print(f"[OK] Created release info: {info_file}")

def main():
    print("=== XHS-Downloader Build Tool ===")
    print("=" * 40)
    
    # Check and install PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            sys.exit(1)
    
    # Clean build directories
    clean_build()
    
    # Build executable
    if build_executable():
        create_release_info()
        print("\n[SUCCESS] Build completed!")
        print("[INFO] Output directory: dist/")
    else:
        print("\n[FAILED] Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()