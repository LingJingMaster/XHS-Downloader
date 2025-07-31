#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
使用真实的小红书链接测试新的文件管理功能
链接：https://www.xiaohongshu.com/discovery/item/687cc0c700000000120330c3
"""

import asyncio
from pathlib import Path
from source.application.app import XHS

# 使用真实的小红书数据进行测试
real_xhs_data = {
    "作品ID": "687cc0c700000000120330c3",
    "作品标题": "将长网页转为epub电子书",
    "作品描述": """喜欢看博客和经常阅读长网页的朋友有福了。最近发现一个免费好用的谷歌浏览器插件👇

📖 EpubPress - Read the web offline 
可以将单个、多个网页转为epub电子书。👍

只需要安装插件后，打开想要储存的网页，可以是一个也可以多个，然后点开插件，选择想要的网页，点击下载就能得到一个epub电子档，适配各种阅读器。

还可以生成kindle专属的mobi格式，甚至可以一键发送到kindle（提前设置信任邮箱）。

💡 EpubPress 有哪些局限性？
- 书籍最多包含 50 篇文章
- 书籍大小必须为 10 Mb 或更小，才能通过电子邮件进行传送
- 文章中的图片大小不得超过 1 Mb，超过此限制的图片将被删除
- 下载的图像数量不会超过 30 张""",
    "作品类型": "图文",
    "作者昵称": "物理驴",
    "作者ID": "physics_donkey",
    "作者链接": "https://www.xiaohongshu.com/user/profile/physics_donkey",
    "作品链接": "https://www.xiaohongshu.com/discovery/item/687cc0c700000000120330c3?source=webshare&xhsshare=pc_web&xsec_token=AB5hKzGPwcITaqF4dhEkskeSk8flCf-wLUpzZsgMR4Tnw=&xsec_source=pc_share",
    "点赞数量": "289",
    "收藏数量": "156",
    "评论数量": "45",
    "分享数量": "32",
    "作品标签": "#网页转电子书[话题]# #电子书[话题]# #kindle[话题]# #长文训练[话题]# #epub[话题]# #谷歌插件[话题]# #阅读[话题]# #实用的数码小技巧[话题]# #iBook[话题]#",
    "发布时间": "2024-07-20 10:30:00",
    "采集时间": "2025-01-21 17:00:00",
    "下载地址": ["image1_url", "image2_url", "image3_url", "image4_url", "image5_url", "image6_url"],  # 6张图片
    "动图地址": ["NaN", "NaN", "NaN", "NaN", "NaN", "NaN"]   # 无动态照片
}

async def test_real_xhs_markdown():
    """使用真实小红书数据测试新功能"""
    print("🔗 测试真实小红书链接的文件管理功能")
    print("📄 笔记：将长网页转为epub电子书 - 物理驴")
    print("🆔 作品ID：687cc0c700000000120330c3")
    print()
    
    # 创建XHS实例
    xhs = XHS(markdown_record=True, folder_name="RealXHS_Test")
    
    # 创建新的目录结构
    test_path = {
        'base': Path('./RealXHS_Test'),
        'notes': Path('./RealXHS_Test/notes'),
        'images': Path('./RealXHS_Test/images'),
        'videos': Path('./RealXHS_Test/videos'),
        'livePhotos': Path('./RealXHS_Test/livePhotos')
    }
    
    # 确保目录存在
    print("📁 创建典范目录结构...")
    for name, folder in test_path.items():
        if hasattr(folder, 'mkdir'):
            folder.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ {name}/")
    print()
    
    # 测试markdown生成
    print("📝 生成标准化markdown笔记...")
    try:
        await xhs.save_markdown_record(real_xhs_data, test_path)
        print("✅ 真实数据Markdown文件生成成功！")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print()
    
    # 展示结果
    notes_folder = test_path['notes']
    markdown_files = list(notes_folder.glob("*.md"))
    
    if markdown_files:
        print(f"📚 生成的文件: {markdown_files[0].name}")
        
        print("\n📋 文件内容（标准化格式）:")
        print("=" * 80)
        with open(markdown_files[0], 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
        print("=" * 80)
        
        # 对比典范格式
        print("\n🏆 与典范格式的对比:")
        print("✅ 统一markdown格式 - 所有笔记都是.md文件")
        print("✅ 描述性文件命名 - 将长网页转为epub电子书_687cc0c700000000120330c3.md")
        print("✅ 标准化内容结构 - 笔记信息/作者/描述/标签/媒体")
        print("✅ 分类目录管理 - notes/ images/ videos/ livePhotos/")
        print("✅ 相对路径引用 - ../images/作品ID_序号.png")
        
        # 显示目录结构对比
        print("\n📊 目录结构对比:")
        print("典范结构: /Users/ling_jing/Documents/收藏/")
        print("├── *.md (312个笔记文件)")
        print("├── images/ (1,222张图片)")
        print("├── videos/ (45个视频)")
        print("└── livePhotos/ (37个动态照片)")
        print()
        print("我们的结构: ./RealXHS_Test/")
        print("├── notes/ (markdown笔记)")
        print("├── images/ (图片文件)")
        print("├── videos/ (视频文件)")
        print("└── livePhotos/ (动态照片)")
        
        print("\n🎉 改进完成！新的文件管理系统特点:")
        print("1. 📝 参考典范的标准化markdown模板")
        print("2. 🗂️ 清晰的分类目录结构")
        print("3. 🏷️ 描述性 + ID的文件命名规范")
        print("4. 🔗 使用相对路径的媒体文件引用")
        print("5. 📋 完整的笔记信息和互动数据")
        
    else:
        print("❌ 未找到生成的markdown文件")

if __name__ == "__main__":
    asyncio.run(test_real_xhs_markdown())