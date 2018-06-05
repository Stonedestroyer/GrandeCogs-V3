import discord
from discord.ext import commands
import re
import aiohttp
import random

class Reddit:
    """Reddit commands."""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    @commands.group(aliases=["r"])
    async def reddit(self, ctx):
        """Reddit Commands"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help()

    @reddit.command()
    @commands.guild_only()
    async def image(self, ctx, subreddit):
        """Random Image From Subreddit"""
        query = f"https://www.reddit.com/r/{subreddit}.json?limit=100"
        try:
            res = await (await self.session.get(query)).json()
        except Exception as e:
            await ctx.send(e)
            return
        exts = ['.*.jpg$', '.*.png$', '.*.gif$', '.*.jpeg$'] 
        ext_search = re.compile('|'.join(exts), re.I) 
        result_urls = [x['data']['url'] for x in res['data']['children']] 
        found = []
        for url in result_urls: 
            if re.findall(ext_search, url): 
                found.append(url)
        if not found:
            await ctx.send("Nothing found.")
            return
        await ctx.send(random.choice(found))
