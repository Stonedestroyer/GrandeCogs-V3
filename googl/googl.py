import discord
from redbot.core import commands
import aiohttp
import json
from redbot.core import Config

BaseCog = getattr(commands, "Cog", object)

class Googl(BaseCog):
    def __init__(self,bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)
        self.config = Config.get_conf(self, identifier=3715379173574, force_registration=True)
        self.config.register_global(api_key=False)

    @commands.group()
    async def googl(self, ctx):
        """Googl"""
        pass

    @googl.command()
    @commands.is_owner()
    async def setkey(self, ctx, key):
        """Set the Google api key"""
        await self.config.api_key.set(key)
        await ctx.send("Key updated!")
        await ctx.message.delete()

    @googl.command()
    async def shorten(self, ctx, url):
        """Shorten url"""
        key = await self.config.api_key()
        if key is False:
            await ctx.send("No API key is set, contact the bot owner.")
            return
        shorten = 'https://www.googleapis.com/urlshortener/v1/url?key=' + key
        payload = {"longUrl": url}
        headers = {"content-type": "application/json"}
        async with self.session.post(shorten,data=json.dumps(payload),headers=headers) as resp:
            data = await resp.json()
        await ctx.send(data['id'])

    @googl.command()
    async def expand(self, ctx, url):
        """Expand goo.gl url"""
        key = await self.config.api_key()
        if key is False:
            await ctx.send("No API key is set, contact the bot owner.")
            return
        async with self.session.get('https://www.googleapis.com/urlshortener/v1/url?key=' + key + '&shortUrl=' + url) as resp:
            print(resp.status)
            data = await resp.json()
        await ctx.send(data['longUrl'])

    @googl.command()
    async def analytics(self, ctx, url):
        """Analytics for url"""
        key = await self.config.api_key()
        if key is False:
            await ctx.send("No API key is set, contact the bot owner.")
            return
        async with self.session.get('https://www.googleapis.com/urlshortener/v1/url?key=' + key + '&shortUrl=' + url + '&projection=FULL') as resp:
            print(resp.status)
            data = await resp.json()
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.add_field(name="**Shortened Url:**",value=data['id'])
        embed.add_field(name="**Long Url:**",value=data['longUrl'])
        embed.add_field(name="**Date Created:**",value=data['created'])
        embed.add_field(name="**Clicks:**",value=data['analytics']['allTime']['shortUrlClicks'])
        embed.set_image(url="https://www.ostraining.com/cdn/images/coding/google-url-shortener-tool.jpg")
        await ctx.send(embed=embed)
