import random
from utils.core import logger
from pyrogram import Client
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName
import asyncio
from urllib.parse import unquote, quote
from data import config
import aiohttp
from fake_useragent import UserAgent
from aiohttp_socks import ProxyConnector


class BeerTap:
    def __init__(self, thread: int, session_name: str, phone_number: str, proxy: [str, None]):
        self.account = session_name + '.session'
        self.thread = thread
        self.tg_init_data = None
        self.proxy = f"{config.PROXY_TYPES['REQUESTS']}://{proxy}" if proxy is not None else None
        connector = ProxyConnector.from_url(self.proxy) if proxy else aiohttp.TCPConnector(verify_ssl=False)

        if proxy:
            proxy = {
                "scheme": config.PROXY_TYPES['TG'],
                "hostname": proxy.split(":")[1].split("@")[1],
                "port": int(proxy.split(":")[2]),
                "username": proxy.split(":")[0],
                "password": proxy.split(":")[1].split("@")[0]
            }

        self.client = Client(
            name=session_name,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            workdir=config.WORKDIR,
            proxy=proxy,
            lang_code='ru'
        )

        headers = {'User-Agent': UserAgent(os='android').random}
        self.session = aiohttp.ClientSession(headers=headers, trust_env=True, connector=connector)

    async def stats(self):
        await asyncio.sleep(random.uniform(*config.DELAYS['ACCOUNT']))
        await self.login()

        r = await (await self.session.get(
            f"https://beer-tg-prod.onrender.com/user?tgInitData={self.tg_init_data}&startParam=_6008239182")).json()
        balance = round(r.get('user').get('balance').get('lastBoonAmount'), 4)
        referrals_reward = round(
            r.get('user').get('ref').get('refState')[0]['earned'] + r.get('user').get('ref').get('refState')[1][
                'earned'], 4)
        referrals = r.get('user').get('ref').get('refState')[0]['amount']
        referral_link = f"https://t.me/BeerCoinTap_Bot/beertapapp?startapp=_{r.get('user').get('_id')}"

        r = await (await self.session.get(
            f"https://beer-tg-prod.onrender.com/game/uiLeaderboard?tgInitData={self.tg_init_data}&startParam=_6008239182")).json()
        leaderboard = r.get("user").get('position')

        await self.logout()

        await self.client.connect()
        me = await self.client.get_me()
        phone_number, name = "'" + me.phone_number, f"{me.first_name} {me.last_name if me.last_name is not None else ''}"
        await self.client.disconnect()

        proxy = self.proxy.replace('http://', "") if self.proxy is not None else '-'
        return [phone_number, name, str(balance), str(leaderboard), str(referrals_reward), str(referrals),
                referral_link, proxy]

    async def battery_taps(self, liters):
        json_data = {"liters": liters}
        url = f'https://beer-tg-prod.onrender.com/game/batteryTaps?tgInitData={self.tg_init_data}'

        resp = await self.session.post(url, json=json_data)
        return (await resp.json()).get('balance').get('lastBoonAmount')

    async def logout(self):
        await self.session.close()

    async def login(self):
        await asyncio.sleep(random.uniform(*config.DELAYS['ACCOUNT']))
        query = await self.get_tg_web_data()

        if query is None:
            logger.error(f"Thread {self.thread} | {self.account} | Session {self.account} invalid")
            await self.logout()
            return None

        self.tg_init_data = query

        await self.session.get(
            f'https://beer-tg-prod.onrender.com/user?tgInitData={self.tg_init_data}&startParam=_6008239182')
        return True

    async def get_tg_web_data(self):
        try:
            await self.client.connect()

            web_view = await self.client.invoke(RequestAppWebView(
                peer=await self.client.resolve_peer('BeerCoinTap_Bot'),
                app=InputBotAppShortName(bot_id=await self.client.resolve_peer('BeerCoinTap_Bot'),
                                         short_name="Beertapapp"),
                platform='android',
                write_allowed=True,
                start_param=f"_6008239182"
            ))
            await self.client.disconnect()
            auth_url = web_view.url

            return quote(string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))

        except:
            return None
