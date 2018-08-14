import discord
from redbot.core import commands
import aiohttp
from bs4 import BeautifulSoup

class OpenNIC:
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)
    
    @commands.group(aliases=["onic"])
    async def opennic(self, ctx):
        """OpenNIC"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help()
    
    @opennic.command()
    async def country(self, ctx, cc):
        """Grab all Tier 2 servers by country"""
        cc = cc.upper()
        html = await (await self.session.get("https://servers.opennicproject.org/view.php?tier=2")).text()
        soup = BeautifulSoup(html, "html.parser")
        cc_list = soup.find("ul", id="cc").get_text().split()[1:]
        cc_list.insert(0, "ANY")
        if cc not in cc_list:
            return await ctx.send("That country code doesn't exist.")
        servs = (soup.find("div", attrs={"name":f"ccg[{cc}]"})).find_all("p")
        servs_info = []
        for serv in servs:
            spans = serv.find_all("span")
            flags = spans[0].find_all("i")
            flags_info = []
            for flag in flags:
                flags_info.append(flag.get("title", ""))
            flags_info = filter(None, flags_info)
            host = spans[1]
            host_info = []
            host_info.append("".join(host.get("title", "").partition(")")[:2]))
            host_info.insert(0, host.a.get("id", ""))
            ipv4 = spans[2].get_text()
            ipv6 = spans[3].get_text()
            owner = spans[4].get_text()
            added = spans[5].get_text()
            status = spans[6].get_text()
            servs_info.append(f"```http\n\nHostname: {' '.join(host_info)}\nIPv4: {ipv4}\nIPv6: {ipv6}\nOwner: {owner}\nDate Added: {added}\nFlags: {', '.join(flags_info)}\nStatus: {status}\n```")
        for i in range(0,len(servs_info),5):
            tmp_list = servs_info[i:i+5]
            await ctx.send("".join(tmp_list))
