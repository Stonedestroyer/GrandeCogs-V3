import discord
from discord.ext import commands
import aiohttp
import locale
import io
from currency_converter import CurrencyConverter

class YuGiOh:
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)
    
    @commands.group(aliases=["ygo"])
    async def yugioh(self, ctx):
        """YuGiOhPrices.com"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Placeholder.")
    
    @yugioh.command()
    async def card(self, ctx, *, card):
        """Search for card"""
        em = await self.cardinfo(card)
        await ctx.send(embed=em)

    @yugioh.command()
    async def price(self, ctx, *, card):
        """Search for price"""
        em = await self.cardprice(card)
        await ctx.send(embed=em)
    
    async def cardinfo(self, card):
        async with self.session.get(f"https://www.ygohub.com/api/card_info?name={card}") as xd:
            data = await xd.json(content_type=None)
        if data["status"] == "error":
            em = discord.Embed(title=(data["error_msg"]).title(), color=0xff0000)
            em.set_footer(text="YGOHub.com")
            return em
        name = data["card"]["name"]
        em = discord.Embed(title=name, color=0x00ff00)
        
        image = data["card"]["image_path"]
        em.set_image(url=image)
        
        text = data["card"]["text"]
        em.add_field(name="Text", value=text, inline=False)
        
        type = data["card"]["type"]
        try:
            species = data["card"]["species"]
            attribute = data["card"]["attribute"]
            type = f"{type} ({attribute})\n[ {species} / " + " / ".join(data["card"]["monster_types"]) + " ]"
        except:
            pass
        em.add_field(name="Type", value=type)
        
        try:
            attack = data["card"]["attack"]
            defense = data["card"]["defense"]
            em.add_field(name="ATK/DEF", value=attack + "/" + defense)
        except:
            pass
        
        try:
            cur = CurrencyConverter()
            locale.setlocale(locale.LC_ALL, "en_GB.UTF-8")
            price_usd = data["card"]["price_avg"]
            price_gbp = cur.convert(price_usd, "USD", "GBP")
            price = locale.currency(price_gbp, grouping=True)
            tcgplayer = data["card"]["tcgplayer_link"]
            em.add_field(name="Average Price", value=f"{price} ([Shop]({tcgplayer}))")
        except:
            pass
        
        em.set_footer(text="YGOHub.com")
            
        return em
    
    async def cardprice(self, card):
        cur = CurrencyConverter()
        locale.setlocale(locale.LC_ALL, "en_GB.UTF-8")
        async with self.session.get(f"http://yugiohprices.com/api/get_card_prices/{card}") as xd:
            data = await xd.json()
        if data["status"] == "fail":
            await ctx.send(data["message"])
            return
        em = discord.Embed(title=card, description="Card Prices", color=0x00ff00)
        for i in data["data"]:
            try:
                price_usd = i['price_data']['data']['prices']['average']
                price_gbp = cur.convert(price_usd, "USD", "GBP")
                price = locale.currency(price_gbp, grouping=True)
                em.add_field(name=i['print_tag'], value=price)
            except:
                em.add_field(name=f"{i['print_tag']}", value="Unable to find prices for this card.")
        em.set_footer(text="YuGiOhPrices.com")
        return em
