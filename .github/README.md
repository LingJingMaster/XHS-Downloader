# 🤖 GitHub Actions 自动构建

这个目录包含了 GitHub Actions 配置文件，用于自动构建多平台可执行文件。

## 🚀 快速开始

### 1. 提交配置文件
```bash
git add .github/
git commit -m "添加 GitHub Actions 自动构建"
git push origin main
```

### 2. 手动触发构建
1. 进入 GitHub 仓库页面
2. 点击 **Actions** 标签  
3. 选择 **"构建可执行文件"** workflow
4. 点击 **"Run workflow"** 按钮
5. 选择是否创建 Release，点击运行

### 3. 下载构建结果
- **Artifacts**: 在 workflow run 页面底部下载
- **Releases**: 在仓库主页右侧的 Releases 部分下载

## 📁 文件说明

| 文件 | 用途 |
|------|------|
| `build-releases.yml` | 完整构建，创建 Release |
| `test-build.yml` | 快速测试构建 |

## 🎯 支持平台

- ✅ **Windows x64** - `XHS-Downloader-windows-x64.zip`
- ✅ **macOS ARM64** - `XHS-Downloader-macos-arm64.tar.gz`
- ✅ **macOS Intel** - `XHS-Downloader-macos-x64.tar.gz`

## 💡 优势

- 🌐 **云端构建** - 无需本地安装多平台环境
- ⚡ **并行处理** - 多平台同时构建，节省时间
- 📦 **自动发布** - 构建完成自动创建 GitHub Release
- 🔒 **安全可靠** - GitHub 官方基础设施
- 💰 **免费使用** - 公开仓库免费使用 GitHub Actions

---

详细使用说明请查看：[GITHUB_ACTIONS_指南.md](../GITHUB_ACTIONS_指南.md)