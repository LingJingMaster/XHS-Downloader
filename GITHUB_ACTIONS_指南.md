# 🚀 GitHub Actions 自动构建指南

通过 GitHub Actions，您可以在云端自动构建多平台可执行文件，无需本地拥有所有平台的设备。

## 📋 功能特性

### ✅ 支持的平台
- **Windows x64** (windows-latest)
- **macOS ARM64** (macos-latest, Apple Silicon)  
- **macOS x64** (macos-13, Intel)

### 🔄 触发方式
1. **手动触发** - 在 GitHub 网页上手动运行
2. **推送触发** - 推送到 main/master 分支时自动构建
3. **Pull Request** - 提交 PR 时测试构建（不发布）

## 🎯 使用方法

### 方法1: 手动触发构建

1. **进入 GitHub 仓库页面**
2. **点击 "Actions" 标签**
3. **选择 "构建可执行文件" workflow**
4. **点击 "Run workflow" 按钮**
5. **选择是否创建 Release**，然后点击 "Run workflow"

### 方法2: 推送代码自动构建

```bash
# 提交代码变更
git add .
git commit -m "更新功能"
git push origin main

# GitHub Actions 会自动开始构建
```

### 方法3: 测试构建

对于开发中的功能，可以使用"测试构建" workflow：

1. 创建 Pull Request
2. 或手动运行 "测试构建" workflow
3. 验证代码可以正常构建，但不会创建 Release

## 📦 构建产物

### Artifacts（构建产物）
每次构建都会生成 Artifacts，保存 30 天：
- `XHS-Downloader-windows-x64` - Windows 版本
- `XHS-Downloader-macos-arm64` - macOS ARM 版本  
- `XHS-Downloader-macos-x64` - macOS Intel 版本

### GitHub Releases
推送到主分支或手动触发时会创建 Release：
- 自动生成版本号：`v2024.01.15-a1b2c3d`
- 包含所有平台的压缩包
- 提供 SHA256 校验文件
- 自动生成更新日志

## 🔧 配置文件说明

### 主要 Workflow 文件

| 文件 | 用途 | 触发条件 |
|------|------|---------|
| `build-releases.yml` | 完整构建和发布 | 推送到主分支 / 手动触发 |
| `test-build.yml` | 快速测试构建 | PR / 手动触发 |

### 构建矩阵

```yaml
strategy:
  matrix:
    include:
      - os: windows-latest      # Windows Server 2022
        platform: windows-x64
      - os: macos-latest        # macOS 14 (ARM64)
        platform: macos-arm64  
      - os: macos-13           # macOS 13 (Intel)
        platform: macos-x64
```

## 📋 构建流程

### 1. 环境准备
- ✅ 检出代码
- ✅ 设置 Python 3.12
- ✅ 缓存 pip 依赖

### 2. 依赖安装
- ✅ 安装项目依赖 (`requirements.txt`)
- ✅ 安装构建依赖 (`build_requirements.txt`)

### 3. 执行构建
- ✅ 运行 `python build.py`
- ✅ 验证构建结果

### 4. 后处理
- ✅ 重命名可执行文件（添加平台标识）
- ✅ 创建压缩包
- ✅ 生成 SHA256 校验文件
- ✅ 上传 Artifacts

### 5. 发布 (可选)
- ✅ 下载所有 Artifacts
- ✅ 创建 GitHub Release
- ✅ 附加所有平台的文件

## 💡 实用技巧

### 查看构建状态
- **GitHub 仓库页面** → **Actions** 标签
- 绿色 ✅ = 成功，红色 ❌ = 失败，黄色 🟡 = 进行中

### 下载构建产物
1. **进入完成的 workflow run**
2. **滚动到底部找到 "Artifacts" 部分**
3. **点击下载对应平台的文件**

### 调试构建失败
1. **点击失败的 job**
2. **展开失败的 step**
3. **查看错误日志**
4. **常见问题**：
   - 依赖版本冲突
   - 模块导入失败
   - 资源文件路径错误

## 🔒 安全说明

### Secrets 配置
当前配置使用默认的 `GITHUB_TOKEN`，具有以下权限：
- ✅ 读取仓库代码
- ✅ 创建 Releases
- ✅ 上传 Artifacts

如需额外功能（如发送通知），可在仓库设置中添加自定义 Secrets。

### 代码签名
目前未配置代码签名，用户首次运行时可能需要：
- **Windows**: 在 SmartScreen 中选择"仍要运行"
- **macOS**: 在"系统偏好设置 > 安全性与隐私"中允许运行

## 📈 优化建议

### 1. 构建时间优化
- ✅ 使用 pip 缓存
- ✅ 矩阵并行构建  
- 💡 可考虑使用 ccache（C 扩展编译缓存）

### 2. 存储优化
- ✅ Artifacts 保留 30 天
- 💡 可配置自动清理旧的 Releases

### 3. 通知集成
```yaml
# 可添加构建完成通知
- name: 发送通知
  if: always()
  run: |
    # 发送到 Slack/Discord/邮件等
```

## 🚀 快速开始

1. **确保文件已提交**：
   ```bash
   git add .github/workflows/
   git commit -m "添加 GitHub Actions 构建配置"
   git push origin main
   ```

2. **首次手动运行**：
   - GitHub 仓库 → Actions → 构建可执行文件 → Run workflow

3. **验证结果**：
   - 检查 Artifacts 是否生成
   - 测试下载的可执行文件

4. **配置自动发布** (可选)：
   - 默认推送到主分支会自动创建 Release
   - 可修改 workflow 文件调整触发条件

---

现在您只需要一台 ARM Mac，就能为用户提供 Windows 和 macOS 的可执行文件了！ 🎉