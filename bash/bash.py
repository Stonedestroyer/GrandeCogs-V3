import discord
from redbot.core import commands
import subprocess
import asyncio
from subprocess import Popen
import threading
from asyncio.subprocess import PIPE
from redbot.core.utils.chat_formatting import pagify

BaseCog = getattr(commands, "Cog", object)

class Bash(BaseCog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["shell"])
    @commands.is_owner()
    async def bash(self, ctx, *, arg):
        """Bash shell"""
        proc = await asyncio.create_subprocess_shell(arg, stdin=None, stderr=None, stdout=PIPE)
        out = await proc.stdout.read()
        msg = pagify(out.decode('utf-8'))
        await ctx.send(f"```ini\n\n[Bash Input]: {arg}\n```")
        for page in msg:
            await ctx.send("```py\n\n{}```".format(page))
