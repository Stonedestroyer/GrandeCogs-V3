import discord
from discord.ext import commands
import aiohttp
import io
from tabulate import tabulate
from bs4 import BeautifulSoup

class Freelancer:
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)
    
    @commands.group(aliases=["fl"])
    async def freelancer(self, ctx):
        """Freelancer Server Stats"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help()
    
    @freelancer.command()
    async def topservers(self, ctx, n=5):
        """Top Servers"""
        em = await self._top_n_servers(n)
        await ctx.send(embed=em)
    
    @freelancer.command()
    async def server(self, ctx, server, timeframe="day"):
        """Server Graph"""
        image = await self._server_graph(ctx, server, timeframe)
        try:
            if image.startswith("Timeframe"):
                return await ctx.send("Invalid timeframe.")
            if image.startswith("Server"):
                return await ctx.send("Invalid server.")
            if len(image) > 1:
                for img in image:
                    await ctx.send(file=discord.File(img, f"{timeframe}-graph.png"))
        except:
            pass
        await ctx.send(file=discord.File(image, f"{server}-{timeframe}-graph.png"))
    
    async def _top_n_servers(self, n):
        if (n < 3) or (n > 10):
            em = discord.Embed(description="Invalid number", color=0xff0000)
            return em
        html = await (await self.session.get("http://flserver.de/topservers.htm")).text()
        soup = BeautifulSoup(html, "html.parser")
        last_update = soup.find_all("h2", {"id": "INSTKEY"})[1].get_text("\n").split("\n")[2]
        rows = soup.find_all("tr")
        total_servers, total_players = rows[0].get_text("\n").split("\n")
        servers = rows[2:n+2]
        em = discord.Embed(title="Freelancer", color=0x0000ff)
        result = []
        for server in servers:
            rank, players, name = server.get_text("\n").split("\n")
            result.append([rank,players,name])
        headers = ["Rank","Players","Server"]
        table = tabulate(result, headers, tablefmt="psql", numalign="left")
        em.add_field(name="Top Servers by Player Count", value=f"```diff\n\n{table}\n```", )
        em.set_footer(text=f"Last Update: {last_update}")
        return em
    
    async def _server_graph(self, ctx, server, timeframe):
        timeframes = ["day","week","month","year"]
        if timeframe not in timeframes:
            return "Timeframe"
        html = await (await self.session.get(f"http://flserver.de/topservers.php?timeframe={timeframe}")).text(encoding="windows-1251")
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.find_all("tr")
        data = []
        for row in rows:
            if server.lower() in str(row).lower():
                data.append(row)
        if not data:
            return "Server"
        elif len(data) > 1:
            await ctx.send("There is more than one result for this server name, want to see them all?")
            def check(user, message):
                return user == ctx.author and message.content.lower() in ("yes", "no") and message.channel == ctx.channel
            try:
                msg = await self.bot.wait_for("message", timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("Request timed out, posting the first result:")
                image = "http://flserver.de/" + data[0].find("a")["href"]
                image = await (await self.session.get(image)).read()
                image = io.BytesIO(image)
                return image
            if msg.content.lower() == "yes":
                images = []
                for server in data:
                    image = "http://flserver.de/" + server.find("a")["href"]
                    image = await (await self.session.get(image)).read()
                    image = io.BytesIO(image)
                    images.append(image)
                return images
        else:
            image = "http://flserver.de/" + data[0].find("a")["href"]
            image = await (await self.session.get(image)).read()
            image = io.BytesIO(image)
            return image
