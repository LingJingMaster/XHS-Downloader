from asyncio import Event, Queue, QueueEmpty, create_task, gather, sleep
from contextlib import suppress
from datetime import datetime
from re import compile
from urllib.parse import urlparse
from pathlib import Path

from aiofiles import open
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

# from aiohttp import web
from pyperclip import copy, paste
from uvicorn import Config, Server

from source.expansion import (
    BrowserCookie,
    Cleaner,
    Converter,
    Namespace,
    beautify_string,
)
from source.module import (
    __VERSION__,
    ERROR,
    MASTER,
    REPOSITORY,
    ROOT,
    VERSION_BETA,
    VERSION_MAJOR,
    VERSION_MINOR,
    WARNING,
    DataRecorder,
    ExtractData,
    ExtractParams,
    IDRecorder,
    Manager,
    MapRecorder,
    logging,
    sleep_time,
)
from source.translation import _, switch_language

from ..module import Mapping
from .download import Download
from .explore import Explore
from .image import Image
from .request import Html
from .video import Video

__all__ = ["XHS"]


def data_cache(function):
    async def inner(
        self,
        data: dict,
    ):
        if self.manager.record_data:
            download = data["下载地址"]
            lives = data["动图地址"]
            await function(
                self,
                data,
            )
            data["下载地址"] = download
            data["动图地址"] = lives

    return inner


class XHS:
    VERSION_MAJOR = VERSION_MAJOR
    VERSION_MINOR = VERSION_MINOR
    VERSION_BETA = VERSION_BETA
    LINK = compile(r"https?://www\.xiaohongshu\.com/explore/\S+")
    SHARE = compile(r"https?://www\.xiaohongshu\.com/discovery/item/\S+")
    SHORT = compile(r"https?://xhslink\.com/\S+")
    ID = compile(r"(?:explore|item)/(\S+)?\?")
    __INSTANCE = None
    CLEANER = Cleaner()

    def __new__(cls, *args, **kwargs):
        if not cls.__INSTANCE:
            cls.__INSTANCE = super().__new__(cls)
        return cls.__INSTANCE

    def __init__(
        self,
        mapping_data: dict = None,
        work_path="",
        folder_name="Download",
        name_format="发布时间 作者昵称 作品标题",
        user_agent: str = None,
        cookie: str = "",
        proxy: str | dict = None,
        timeout=10,
        chunk=1024 * 1024,
        max_retry=5,
        record_data=False,
        image_format="PNG",
        image_download=True,
        video_download=True,
        live_download=False,
        folder_mode=False,
        download_record=True,
        author_archive=False,
        write_mtime=False,
        markdown_record=False,
        language="zh_CN",
        read_cookie: int | str = None,
        _print: bool = True,
        *args,
        **kwargs,
    ):
        switch_language(language)
        self.manager = Manager(
            ROOT,
            work_path,
            folder_name,
            name_format,
            chunk,
            user_agent,
            self.read_browser_cookie(read_cookie) or cookie,
            proxy,
            timeout,
            max_retry,
            record_data,
            image_format,
            image_download,
            video_download,
            live_download,
            download_record,
            folder_mode,
            author_archive,
            write_mtime,
            markdown_record,
            _print,
        )
        self.mapping_data = mapping_data or {}
        self.map_recorder = MapRecorder(
            self.manager,
        )
        self.mapping = Mapping(self.manager, self.map_recorder)
        self.html = Html(self.manager)
        self.image = Image()
        self.video = Video()
        self.explore = Explore()
        self.convert = Converter()
        self.download = Download(self.manager)
        self.id_recorder = IDRecorder(self.manager)
        self.data_recorder = DataRecorder(self.manager)
        self.clipboard_cache: str = ""
        self.queue = Queue()
        self.event = Event()
        # self.runner = self.init_server()
        # self.site = None
        self.server = None

    def __extract_image(self, container: dict, data: Namespace):
        container["下载地址"], container["动图地址"] = self.image.get_image_link(
            data, self.manager.image_format
        )

    def __extract_video(self, container: dict, data: Namespace):
        container["下载地址"] = self.video.get_video_link(data)
        container["动图地址"] = [
            None,
        ]

    async def __download_files(
        self,
        container: dict,
        download: bool,
        index,
        log,
        bar,
    ):
        name = self.__naming_rules(container)
        work_path = None
        if (u := container["下载地址"]) and download:
            if await self.skip_download(i := container["作品ID"]):
                logging(log, _("作品 {0} 存在下载记录，跳过下载").format(i))
            else:
                path_dict, result = await self.download.run(
                    u,
                    container["动图地址"],
                    index,
                    container["作者ID"]
                    + "_"
                    + self.CLEANER.filter_name(container["作者昵称"]),
                    name,
                    container["作品类型"],
                    container["时间戳"],
                    log,
                    bar,
                    work_id=container["作品ID"],  # 传递作品ID
                )
                work_path = path_dict
                await self.__add_record(i, result)
        elif not u:
            logging(log, _("提取作品文件下载地址失败"), ERROR)
        
        # 保存Markdown记录（如果启用且有下载路径，或者强制生成到默认路径）
        if work_path or self.manager.markdown_record:
            # 如果没有下载路径但启用了Markdown记录，创建默认路径字典
            if not work_path:
                # 创建新的目录结构
                base_folder = self.manager.folder
                work_path = {
                    'base': base_folder,
                    'notes': base_folder / "notes",
                    'images': base_folder / "images",
                    'videos': base_folder / "videos",
                    'livePhotos': base_folder / "livePhotos"
                }
                # 确保目录存在
                for folder in work_path.values():
                    if hasattr(folder, 'mkdir'):
                        folder.mkdir(exist_ok=True)
            
            await self.save_markdown_record(container, work_path)
        
        await self.save_data(container)

    @data_cache
    async def save_data(
        self,
        data: dict,
    ):
        data["采集时间"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["下载地址"] = " ".join(data["下载地址"])
        data["动图地址"] = " ".join(i or "NaN" for i in data["动图地址"])
        data.pop("时间戳", None)
        await self.data_recorder.add(**data)

    def generate_markdown_content(self, data: dict, work_id: str = None) -> str:
        """生成作品信息的Markdown格式内容 - 参考典范格式"""
        
        # 获取标题，用于文件名
        title = data.get('作品标题', '未知标题')
        work_id = work_id or data.get('作品ID', 'unknown')
        
        # 生成媒体文件引用
        media_content = self._generate_media_references(data, work_id)
        
        content = f"""# {title}

### 笔记信息
笔记链接：{data.get('作品链接', '#')}

作者：
{data.get('作者昵称', '未知')}
主页链接：{data.get('作者链接', '#')}

### 笔记描述
{data.get('作品描述', '暂无描述')}

{data.get('作品标签', '')}

### 互动数据
- 点赞：{data.get('点赞数量', '0')}
- 收藏：{data.get('收藏数量', '0')}  
- 评论：{data.get('评论数量', '0')}
- 分享：{data.get('分享数量', '0')}

{media_content}

"""
        return content

    def _generate_media_references(self, data: dict, work_id: str) -> str:
        """生成媒体文件的markdown引用"""
        media_refs = []
        
        # 获取下载地址信息
        download_urls = data.get('下载地址', [])
        if isinstance(download_urls, str):
            download_urls = download_urls.split()
        
        live_urls = data.get('动图地址', [])
        if isinstance(live_urls, str):
            live_urls = [i for i in live_urls.split() if i != 'NaN']
        elif isinstance(live_urls, list):
            live_urls = [i for i in live_urls if i and i != 'NaN']
        
        work_type = data.get('作品类型', '')
        
        if work_type == '视频':
            # 视频文件引用
            media_refs.append("### 视频")
            media_refs.append(f"[视频文件](../videos/{work_id}.mp4)")
        else:
            # 图片文件引用
            if download_urls:
                media_refs.append("### 图片")
                for i in range(len(download_urls)):
                    media_refs.append(f"![](../images/{work_id}_{i+1}.png)")
            
            # 动态照片引用
            if live_urls:
                media_refs.append("### 动态照片")
                for i in range(len(live_urls)):
                    media_refs.append(f"[动态照片{i+1}](../livePhotos/{work_id}_{i+1}.mp4)")
        
        return "\n".join(media_refs) if media_refs else ""

    async def save_markdown_record(self, data: dict, work_path):
        """将作品信息保存为Markdown文件到notes目录"""
        if not self.manager.markdown_record:
            return
        
        # 数据类型检查
        if not isinstance(data, dict):
            logging(None, _("生成Markdown记录失败: 数据格式不正确，需要字典类型"), ERROR)
            return
            
        try:
            # 创建一个副本来避免修改原始数据
            data_copy = data.copy()
            
            # 确保下载地址和动图地址是字符串格式
            if isinstance(data_copy.get('下载地址'), list):
                data_copy['下载地址'] = " ".join(data_copy['下载地址'])
            if isinstance(data_copy.get('动图地址'), list):
                data_copy['动图地址'] = " ".join(str(i) if i else "NaN" for i in data_copy['动图地址'])
            
            # 获取作品ID和标题
            work_id = data_copy.get('作品ID', 'unknown')
            title = data_copy.get('作品标题', '未知标题')
            
            # 清理标题用于文件名（移除特殊字符）
            clean_title = self.CLEANER.filter_name(title, replace="_")[:50]  # 限制长度
            
            # 生成Markdown内容
            markdown_content = self.generate_markdown_content(data_copy, work_id)
            
            # 构建文件路径 - 保存到notes目录，使用描述性命名
            if isinstance(work_path, dict):
                notes_folder = work_path['notes']
            else:
                # 兼容旧的路径格式
                notes_folder = work_path / "notes"
                notes_folder.mkdir(exist_ok=True)
            
            markdown_filename = f"{clean_title}_{work_id}.md"
            markdown_path = notes_folder / markdown_filename
            
            # 确保目录存在
            markdown_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 写入文件
            async with open(markdown_path, 'w', encoding='utf-8') as f:
                await f.write(markdown_content)
            
            logging(None, _("已生成作品Markdown记录: {0}").format(markdown_filename))
            
        except Exception as e:
            logging(None, _("生成Markdown记录失败: {0}").format(str(e)), ERROR)

    async def __add_record(self, id_: str, result: list) -> None:
        if all(result):
            await self.id_recorder.add(id_)

    async def extract(
        self,
        url: str,
        download=False,
        index: list | tuple = None,
        log=None,
        bar=None,
        data=True,
    ) -> list[dict]:
        # return  # 调试代码
        urls = await self.extract_links(url, log)
        if not urls:
            logging(log, _("提取小红书作品链接失败"), WARNING)
        else:
            logging(log, _("共 {0} 个小红书作品待处理...").format(len(urls)))
        # return urls  # 调试代码
        return [
            await self.__deal_extract(
                i,
                download,
                index,
                log,
                bar,
                data,
            )
            for i in urls
        ]

    async def extract_cli(
        self,
        url: str,
        download=True,
        index: list | tuple = None,
        log=None,
        bar=None,
        data=False,
    ) -> None:
        url = await self.extract_links(url, log)
        if not url:
            logging(log, _("提取小红书作品链接失败"), WARNING)
        else:
            await self.__deal_extract(
                url[0],
                download,
                index,
                log,
                bar,
                data,
            )

    async def extract_links(self, url: str, log) -> list:
        urls = []
        for i in url.split():
            if u := self.SHORT.search(i):
                i = await self.html.request_url(
                    u.group(),
                    False,
                    log,
                )
            if u := self.SHARE.search(i):
                urls.append(u.group())
            elif u := self.LINK.search(i):
                urls.append(u.group())
        return urls

    def extract_id(self, links: list[str]) -> list[str]:
        ids = []
        for i in links:
            if j := self.ID.search(i):
                ids.append(j.group(1))
        return ids

    async def __deal_extract(
        self,
        url: str,
        download: bool,
        index: list | tuple | None,
        log,
        bar,
        data: bool,
        cookie: str = None,
        proxy: str = None,
    ):
        if await self.skip_download(i := self.__extract_link_id(url)) and not data:
            msg = _("作品 {0} 存在下载记录，跳过处理").format(i)
            logging(log, msg)
            return {"message": msg}
        logging(log, _("开始处理作品：{0}").format(i))
        html = await self.html.request_url(
            url,
            log=log,
            cookie=cookie,
            proxy=proxy,
        )
        namespace = self.__generate_data_object(html)
        if not namespace:
            logging(log, _("{0} 获取数据失败").format(i), ERROR)
            return {}
        data = self.explore.run(namespace)
        # logging(log, data)  # 调试代码
        if not data:
            logging(log, _("{0} 提取数据失败").format(i), ERROR)
            return {}
        if data["作品类型"] == _("视频"):
            self.__extract_video(data, namespace)
        elif data["作品类型"] == _("图文"):
            self.__extract_image(data, namespace)
        else:
            data["下载地址"] = []
        await self.update_author_nickname(data, log)
        await self.__download_files(data, download, index, log, bar)
        logging(log, _("作品处理完成：{0}").format(i))
        await sleep_time()
        return data

    async def update_author_nickname(
        self,
        container: dict,
        log,
    ):
        if a := self.CLEANER.filter_name(
            self.mapping_data.get(i := container["作者ID"], "")
        ):
            container["作者昵称"] = a
        else:
            container["作者昵称"] = self.manager.filter_name(container["作者昵称"]) or i
        await self.mapping.update_cache(
            i,
            container["作者昵称"],
            log,
        )

    @staticmethod
    def __extract_link_id(url: str) -> str:
        link = urlparse(url)
        return link.path.split("/")[-1]

    def __generate_data_object(self, html: str) -> Namespace:
        data = self.convert.run(html)
        return Namespace(data)

    def __naming_rules(self, data: dict) -> str:
        keys = self.manager.name_format.split()
        values = []
        for key in keys:
            match key:
                case "发布时间":
                    values.append(self.__get_name_time(data))
                case "作品标题":
                    values.append(self.__get_name_title(data))
                case _:
                    values.append(data[key])
        return beautify_string(
            self.CLEANER.filter_name(
                self.manager.SEPARATE.join(values),
                default=self.manager.SEPARATE.join(
                    (
                        data["作者ID"],
                        data["作品ID"],
                    )
                ),
            ),
            length=128,
        )

    @staticmethod
    def __get_name_time(data: dict) -> str:
        return data["发布时间"].replace(":", ".")

    def __get_name_title(self, data: dict) -> str:
        return (
            beautify_string(
                self.manager.filter_name(data["作品标题"]),
                64,
            )
            or data["作品ID"]
        )

    async def monitor(
        self,
        delay=1,
        download=False,
        log=None,
        bar=None,
        data=True,
    ) -> None:
        logging(
            None,
            _(
                "程序会自动读取并提取剪贴板中的小红书作品链接，并自动下载链接对应的作品文件，如需关闭，请点击关闭按钮，或者向剪贴板写入 “close” 文本！"
            ),
            style=MASTER,
        )
        self.event.clear()
        copy("")
        await gather(
            self.__get_link(delay),
            self.__receive_link(delay, download, None, log, bar, data),
        )

    async def __get_link(self, delay: int):
        while not self.event.is_set():
            if (t := paste()).lower() == "close":
                self.stop_monitor()
            elif t != self.clipboard_cache:
                self.clipboard_cache = t
                create_task(self.__push_link(t))
            await sleep(delay)

    async def __push_link(
        self,
        content: str,
    ):
        await gather(
            *[self.queue.put(i) for i in await self.extract_links(content, None)]
        )

    async def __receive_link(self, delay: int, *args, **kwargs):
        while not self.event.is_set() or self.queue.qsize() > 0:
            with suppress(QueueEmpty):
                await self.__deal_extract(self.queue.get_nowait(), *args, **kwargs)
            await sleep(delay)

    def stop_monitor(self):
        self.event.set()

    async def skip_download(self, id_: str) -> bool:
        return bool(await self.id_recorder.select(id_))

    async def __aenter__(self):
        await self.id_recorder.__aenter__()
        await self.data_recorder.__aenter__()
        await self.map_recorder.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.id_recorder.__aexit__(exc_type, exc_value, traceback)
        await self.data_recorder.__aexit__(exc_type, exc_value, traceback)
        await self.map_recorder.__aexit__(exc_type, exc_value, traceback)
        await self.close()

    async def close(self):
        await self.manager.close()

    @staticmethod
    def read_browser_cookie(value: str | int) -> str:
        return (
            BrowserCookie.get(
                value,
                domains=[
                    "xiaohongshu.com",
                ],
            )
            if value
            else ""
        )

    # @staticmethod
    # async def index(request):
    #     return web.HTTPFound(REPOSITORY)

    # async def handle(self, request):
    #     data = await request.post()
    #     url = data.get("url")
    #     download = data.get("download", False)
    #     index = data.get("index")
    #     skip = data.get("skip", False)
    #     url = await self.__extract_links(url, None)
    #     if not url:
    #         msg = _("提取小红书作品链接失败")
    #         data = None
    #     else:
    #         if data := await self.__deal_extract(url[0], download, index, None, None, not skip, ):
    #             msg = _("获取小红书作品数据成功")
    #         else:
    #             msg = _("获取小红书作品数据失败")
    #             data = None
    #     return web.json_response(dict(message=msg, url=url[0], data=data))

    # def init_server(self, ):
    #     app = web.Application(debug=True)
    #     app.router.add_get('/', self.index)
    #     app.router.add_post('/xhs/', self.handle)
    #     return web.AppRunner(app)

    # async def run_server(self, log=None, ):
    #     try:
    #         await self.start_server(log)
    #         while True:
    #             await sleep(3600)  # 保持服务器运行
    #     except (CancelledError, KeyboardInterrupt):
    #         await self.close_server(log)

    # async def start_server(self, log=None, ):
    #     await self.runner.setup()
    #     self.site = web.TCPSite(self.runner, "0.0.0.0")
    #     await self.site.start()
    #     logging(log, _("Web API 服务器已启动！"))
    #     logging(log, _("服务器主机及端口: {0}".format(self.site.name, )))

    # async def close_server(self, log=None, ):
    #     await self.runner.cleanup()
    #     logging(log, _("Web API 服务器已关闭！"))

    async def run_server(
        self,
        host="0.0.0.0",
        port=6666,
        log_level="info",
    ):
        self.server = FastAPI(
            debug=self.VERSION_BETA,
            title="XHS-Downloader",
            version=__VERSION__,
        )
        self.setup_routes()
        config = Config(
            self.server,
            host=host,
            port=port,
            log_level=log_level,
        )
        server = Server(config)
        await server.serve()

    def setup_routes(self):
        @self.server.get("/")
        async def index():
            return RedirectResponse(url=REPOSITORY)

        @self.server.post(
            "/xhs/",
            response_model=ExtractData,
        )
        async def handle(extract: ExtractParams):
            url = await self.extract_links(extract.url, None)
            if not url:
                msg = _("提取小红书作品链接失败")
                data = None
            else:
                if data := await self.__deal_extract(
                    url[0],
                    extract.download,
                    extract.index,
                    None,
                    None,
                    not extract.skip,
                    extract.cookie,
                    extract.proxy,
                ):
                    msg = _("获取小红书作品数据成功")
                else:
                    msg = _("获取小红书作品数据失败")
                    data = None
            return ExtractData(message=msg, params=extract, data=data)
