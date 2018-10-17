import discord
from redbot.core import commands
import socket

BaseCog = getattr(commands, "Cog", object)

class ScanPort(BaseCog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def scanport(self, ctx, ip, port:int):
        """Scan an IP for open ports"""
        resp = self._scanport(ip, port)
        if resp == True:
            data = discord.Embed(description="Port Scan", colour=(await ctx.embed_colour()))
            data.add_field(name="**Success**", value=f"IP: {ip}\nPort: {port}")
            await ctx.send(embed=data)
        else:
            await ctx.send(resp)

    def _scanport(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            socket.inet_aton(ip)
        except OSError as e:
            return f"Invalid IP address passed: `{e}`"
        try:
            sock.connect((ip, port))
            return True
        except socket.gaierror:
            return "Could not be resolved."
        except socket.error:
            return "Failed to connect to port."
