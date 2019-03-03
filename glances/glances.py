import discord
from redbot.core import checks, commands
from selenium import webdriver
import asyncio

BaseCog = getattr(commands, "Cog", object)

class Glances(BaseCog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_owner()
    async def glances(self, ctx):
        """Glances monitor"""
        driver = webdriver.PhantomJS()
        driver.set_window_size(1920, 1080)
        driver.get("http://0.0.0.0:61208/")
        await asyncio.sleep(1)
        screenshot = driver.get_screenshot_as_png()
        driver.quit()
        await ctx.send(file=discord.File(screenshot, "screenshot.png"))
