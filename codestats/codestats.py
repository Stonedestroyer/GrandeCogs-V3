import discord
from redbot.core import commands
import aiohttp
import math

BaseCog = getattr(commands, "Cog", object)

class CodeStats(BaseCog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)
    
    @commands.command()
    async def codestats(self, ctx, name):
        """CodeStats"""
        async with self.session.get(f"https://codestats.net/api/users/{name}") as resp:
            if resp.status is not 200:
                await ctx.send("User not found or private.")
                return
            data = await resp.json()
        
        user = data["user"]
        total_xp = data["total_xp"]
        recent_xp = data["new_xp"]
        level = self._getlevel(total_xp)
        langs = ""
        top_langs = dict(sorted(data['languages'].items(), key=lambda lang: lang[1]['xps'], reverse=True)[:5])
        for key, value in top_langs.items():
            langs += f"**{key}:** Level {self._getlevel(value['xps'])} ({value['xps']} xp)\n"
        
        embed = discord.Embed(description=f"[{user}](https://codestats.net/users/{user})", colour=discord.Colour.blue())
        embed.add_field(name="Overall", value=f"**Level:** {level}\n**Total XP:** {total_xp}\n**Recent XP:** {recent_xp}")
        embed.add_field(name="Top 5 Languages", value=f"{langs}")
        embed.set_thumbnail(url="https://codestats.net/images/Logo_crushed.png")
        await ctx.send(embed=embed)
    
    def _getlevel(self, xp, level_factor=0.025):
        return int(math.floor(level_factor * math.sqrt(xp)))

def setup(bot):
    bot.add_cog(CodeStats(bot))
