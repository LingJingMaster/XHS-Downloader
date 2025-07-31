#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试 XHS-Downloader 新增的 Markdown 记录功能
"""

from asyncio import run
from source import XHS


async def test_markdown_feature():
    """测试 Markdown 记录功能"""
    print("🧪 开始测试 Markdown 记录功能...")
    
    # 配置参数
    config = {
        "work_path": "./test_output",
        "folder_name": "TestDownload", 
        "folder_mode": True,  # 开启单独文件夹模式
        "markdown_record": True,  # 开启 Markdown 记录功能
        "record_data": False,  # 关闭数据库记录（测试用）
        "download_record": False,  # 关闭下载记录（测试用）
    }
    
    # 示例链接（需要替换为有效链接）
    test_url = ""  # 请在此处填入真实的小红书作品链接
    
    if not test_url:
        print("❌ 请在脚本中设置有效的小红书作品链接进行测试")
        return
    
    async with XHS(**config) as xhs:
        print(f"📥 开始处理链接: {test_url}")
        
        # 提取作品信息（不下载文件）
        result = await xhs.extract(test_url, download=False)
        
        if result:
            print("✅ 作品信息提取成功！")
            print(f"📝 作品标题: {result.get('作品标题', '未知')}")
            print(f"👤 作者昵称: {result.get('作者昵称', '未知')}")
            print(f"🆔 作品ID: {result.get('作品ID', '未知')}")
            
            # 检查是否生成了 Markdown 文件
            work_path = xhs.manager.folder / "TestDownload"
            if config["folder_mode"]:
                filename = xhs._XHS__naming_rules(result)
                work_path = work_path / filename
            
            markdown_file = work_path / f"{result.get('作品ID', 'unknown')}_info.md"
            
            if markdown_file.exists():
                print(f"✅ Markdown 记录文件已生成: {markdown_file}")
                print("📄 文件内容预览:")
                print("-" * 50)
                with open(markdown_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 只显示前500个字符
                    print(content[:500])
                    if len(content) > 500:
                        print("\n... (内容已截断)")
                print("-" * 50)
            else:
                print(f"❌ Markdown 记录文件未找到: {markdown_file}")
        else:
            print("❌ 作品信息提取失败")


def demo_markdown_content():
    """演示 Markdown 内容格式"""
    print("\n📋 Markdown 记录文件格式示例:")
    print("=" * 60)
    
    # 创建一个示例数据
    sample_data = {
        "作品标题": "美丽的风景照片",
        "作品ID": "12345678abcdef",
        "作品类型": "图文", 
        "发布时间": "2024-01-15_14:30:25",
        "最后更新时间": "2024-01-15_14:30:25",
        "作品链接": "https://www.xiaohongshu.com/explore/12345678abcdef",
        "作者昵称": "风景摄影师",
        "作者ID": "user123456",
        "作者链接": "https://www.xiaohongshu.com/user/profile/user123456",
        "点赞数量": "1234",
        "收藏数量": "567", 
        "评论数量": "89",
        "分享数量": "12",
        "作品描述": "今天在公园拍到的美丽日落，夕阳西下的景色真是太美了！",
        "作品标签": "摄影 风景 日落 夕阳",
        "下载地址": "https://example.com/image1.jpg https://example.com/image2.jpg",
        "动图地址": "NaN NaN",
        "采集时间": "2024-01-15 15:00:00"
    }
    
    # 创建临时的 XHS 实例来生成 Markdown
    from source.application.app import XHS
    xhs = XHS()
    markdown_content = xhs.generate_markdown_content(sample_data)
    
    print(markdown_content)
    print("=" * 60)


if __name__ == "__main__":
    print("🎯 XHS-Downloader Markdown 记录功能测试")
    print("=" * 60)
    
    # 先演示 Markdown 格式
    demo_markdown_content()
    
    # 提示用户如何进行实际测试
    print("\n💡 如需测试实际功能，请：")
    print("1. 在 test_url 变量中填入有效的小红书作品链接")
    print("2. 运行: python test_markdown_feature.py")
    print("3. 检查 ./test_output/TestDownload/ 目录下是否生成了 Markdown 文件")
    
    # 如果用户设置了链接，则运行实际测试
    # run(test_markdown_feature())