from astrbot.api.message_components import *
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
import aiohttp
import logging

# 设置日志记录
logger = logging.getLogger(__name__)

@register("astrbot_plugin_setu", "czqwq", "从API获取图片。使用 /img 获取一张随机图片。", "1.0")
class SetuPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        self.api_url = config.get("api_url", "")
        # 获取自定义指令列表，默认为 ["img"]
        self.custom_commands = config.get("custom_commands", ["img"])
        # 获取最大重试次数，默认为3次
        self.max_retries = config.get("max_retries", 3)

    @filter.command("img")
    async def get_setu(self, event: AstrMessageEvent):
        # 检查指令是否在自定义指令列表中
        if "img" not in self.custom_commands:
            return
            
        # 检查黑白名单权限
        if not self.check_permission(event):
            # 如果没有权限，不返回任何内容，静默忽略
            return
        
        return await self._fetch_and_send_image(event)
    
    @filter.command("setu")
    async def get_setu_alt1(self, event: AstrMessageEvent):
        # 检查指令是否在自定义指令列表中
        if "setu" not in self.custom_commands:
            return
            
        # 检查黑白名单权限
        if not self.check_permission(event):
            # 如果没有权限，不返回任何内容，静默忽略
            return
        
        return await self._fetch_and_send_image(event)
        
    @filter.command("image")
    async def get_setu_alt2(self, event: AstrMessageEvent):
        # 检查指令是否在自定义指令列表中
        if "image" not in self.custom_commands:
            return
            
        # 检查黑白名单权限
        if not self.check_permission(event):
            # 如果没有权限，不返回任何内容，静默忽略
            return
        
        return await self._fetch_and_send_image(event)
        
    @filter.command("pic")
    async def get_setu_alt3(self, event: AstrMessageEvent):
        # 检查指令是否在自定义指令列表中
        if "pic" not in self.custom_commands:
            return
            
        # 检查黑白名单权限
        if not self.check_permission(event):
            # 如果没有权限，不返回任何内容，静默忽略
            return
        
        return await self._fetch_and_send_image(event)
    
    async def _fetch_and_send_image(self, event: AstrMessageEvent):
        """
        获取并发送图片的核心逻辑
        """
        # 检查是否配置了API URL
        if not self.api_url:
            return event.plain_result("\n请先在配置文件中设置API地址")
            
        # 创建一个不验证SSL的连接上下文
        ssl_context = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=ssl_context) as session:
            for attempt in range(self.max_retries):
                try:
                    # 使用配置中的API URL发送GET请求
                    async with session.get(self.api_url) as response:
                        data = await response.json()
                        
                        if data["error"]:
                            logger.warning(f"第{attempt + 1}/{self.max_retries}次请求失败：{data['error']}")
                            if attempt < self.max_retries - 1:  # 不是最后一次尝试
                                continue
                            return event.plain_result(f"\n获取图片失败：{data['error']}")
                        
                        if not data["data"]:
                            logger.warning(f"第{attempt + 1}/{self.max_retries}次请求未获取到图片数据")
                            if attempt < self.max_retries - 1:  # 不是最后一次尝试
                                continue
                            return event.plain_result("\n未获取到图片")
                        
                        # 获取图片信息
                        image_data = data["data"][0]
                        image_url = image_data["urls"]["original"]
                        title = image_data["title"]
                        author = image_data["author"]
                        
                        # 构建消息链
                        chain = [
                            Image.fromURL(image_url)  # 从URL加载图片
                        ]
                        
                        return event.chain_result(chain)
                        
                except Exception as e:
                    logger.warning(f"第{attempt + 1}/{self.max_retries}次请求异常: {str(e)}")
                    if attempt < self.max_retries - 1:  # 不是最后一次尝试
                        continue
                    return event.plain_result(f"\n请求失败: {str(e)}")
    
    def check_permission(self, event: AstrMessageEvent) -> bool:
        """
        检查用户是否有权限使用本插件
        """
        # 获取群ID和用户ID
        gid = event.get_group_id()
        uid = event.get_sender_id()
        bid = event.get_self_id()  # bot自己的ID
        
        # 如果是私聊，允许使用
        if not gid:
            return True
            
        # 如果是自己发的消息，不响应
        if uid == bid:
            return False
            
        # 检查是否是管理员
        is_admin = event.is_admin()
        
        # 管理员可以在所有群组中使用命令
        if is_admin:
            return True
        
        # 群聊白名单检查
        group_whitelist = self.config.get("group_whitelist", [])
        if group_whitelist and gid not in group_whitelist:
            return False
            
        # 群聊黑名单检查
        group_blacklist = self.config.get("group_blacklist", [])
        if gid in group_blacklist:
            return False
            
        # 用户黑名单检查
        user_blacklist = self.config.get("user_blacklist", [])
        if uid in user_blacklist:
            return False
            
        return True