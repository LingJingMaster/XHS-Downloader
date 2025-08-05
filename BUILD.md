# XHS-Downloader 可执行文件构建指南

本指南将帮助您将 XHS-Downloader 编译成可执行文件，用户无需安装 Python 环境即可直接运行。

## 支持的平台

- ✅ Windows (x64)
- ✅ macOS (ARM64/Apple Silicon)
- ✅ macOS (Intel x64)
- ✅ Linux (x64)

## 快速开始

### 方法一：自动构建（推荐）

1. **安装 Python 3.12**（仅构建时需要）
   ```bash
   # macOS (使用 Homebrew)
   brew install python@3.12
   
   # Windows: 从 python.org 下载安装包
   ```

2. **安装项目依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行构建脚本**
   ```bash
   python build.py
   ```

4. **获取可执行文件**
   - 构建完成后，可执行文件将位于 `dist/` 目录
   - Windows: `dist/XHS-Downloader.exe`
   - macOS/Linux: `dist/XHS-Downloader`

### 方法二：手动构建

1. **安装 PyInstaller**
   ```bash
   pip install pyinstaller>=6.0.0
   ```

2. **清理旧的构建文件**
   ```bash
   rm -rf build dist __pycache__
   ```

3. **使用 spec 文件构建**
   ```bash
   pyinstaller --clean xhs_downloader.spec
   ```

## 平台特定说明

### Windows

- **系统要求**: Windows 10 或更高版本
- **输出文件**: `XHS-Downloader.exe`
- **文件大小**: 约 80-120 MB
- **使用方法**:
  ```cmd
  # GUI 模式
  XHS-Downloader.exe
  
  # 服务器模式
  XHS-Downloader.exe server
  
  # CLI 模式
  XHS-Downloader.exe --help
  ```

### macOS (ARM64/Apple Silicon)

- **系统要求**: macOS 11.0 (Big Sur) 或更高版本
- **输出文件**: `XHS-Downloader`
- **文件大小**: 约 90-130 MB
- **使用方法**:
  ```bash
  # 添加执行权限（如果需要）
  chmod +x XHS-Downloader
  
  # GUI 模式
  ./XHS-Downloader
  
  # 服务器模式
  ./XHS-Downloader server
  ```

### macOS (Intel)

- **系统要求**: macOS 10.15 (Catalina) 或更高版本
- **构建要求**: 需要在 Intel Mac 上构建
- **其他说明**: 与 ARM64 版本使用方法相同

## 跨平台构建

如果您需要为其他平台构建可执行文件，请在对应平台上运行构建脚本：

```bash
# 在 Windows 上构建 Windows 版本
python build.py

# 在 macOS ARM 上构建 macOS ARM 版本
python3 build.py

# 在 macOS Intel 上构建 macOS Intel 版本
python3 build.py
```

## 构建选项说明

### spec 文件配置 (`xhs_downloader.spec`)

- **包含的资源文件**:
  - `settings.json` - 配置文件
  - `static/` - 图标、样式文件
  - `locale/` - 多语言支持文件

- **隐藏导入模块**: 确保所有依赖都被正确包含
- **图标设置**: Windows 使用 `.ico`，macOS 使用 `.icns`
- **控制台模式**: 启用，以支持命令行交互

### 构建优化

- **UPX 压缩**: 启用，减小文件大小
- **排除模块**: 移除不需要的模块（如 tkinter、测试模块等）
- **单文件模式**: 所有依赖打包成一个可执行文件

## 故障排除

### 常见问题

1. **构建失败: 模块找不到**
   ```bash
   # 确保所有依赖都已安装
   pip install -r requirements.txt
   ```

2. **可执行文件启动失败**
   ```bash
   # 检查是否缺少系统库
   # macOS: 安装 Xcode Command Line Tools
   xcode-select --install
   ```

3. **文件过大**
   - 单文件模式会比较大（80-130MB），这是正常的
   - 包含了完整的 Python 运行时和所有依赖

4. **权限问题 (macOS/Linux)**
   ```bash
   chmod +x XHS-Downloader
   ```

### 调试构建

如果构建失败，可以启用详细输出：

```bash
pyinstaller --clean --debug=all xhs_downloader.spec
```

## 发布建议

1. **文件命名**: 建议按平台命名
   - `XHS-Downloader-windows-x64.exe`
   - `XHS-Downloader-macos-arm64`
   - `XHS-Downloader-macos-x64`

2. **压缩发布**: 
   ```bash
   # Windows
   zip XHS-Downloader-windows-x64.zip XHS-Downloader.exe
   
   # macOS
   tar -czf XHS-Downloader-macos-arm64.tar.gz XHS-Downloader
   ```

3. **校验文件**: 提供 SHA256 校验值
   ```bash
   # Windows
   certutil -hashfile XHS-Downloader.exe SHA256
   
   # macOS/Linux
   sha256sum XHS-Downloader
   ```

## 注意事项

- 可执行文件仅包含应用程序，不包含用户数据
- 首次运行时会在当前目录创建配置文件
- 确保运行目录有写入权限
- 网络功能需要系统网络权限
- 某些杀毒软件可能误报，这是 PyInstaller 的常见问题

## 技术支持

如果在构建过程中遇到问题，请：

1. 检查 Python 版本（需要 3.12）
2. 确保所有依赖都已正确安装
3. 查看构建日志中的错误信息
4. 参考 PyInstaller 官方文档