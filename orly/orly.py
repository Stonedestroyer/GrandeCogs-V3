import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import aiohttp, textwrap, os
from redbot.core.data_manager import cog_data_path
from io import BytesIO

class ORly:
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)
    
    @commands.command()
    async def orly(self, ctx, box_text, title_text, small_text, image_url, hex):
        """O Rly?"""
        data_path = cog_data_path()
        orly_logo = os.path.join(data_path, 'CogManager', 'cogs', 'orly', 'data', 'orly-logo.png')
        gara_font = os.path.join(data_path, 'CogManager', 'cogs', 'orly', 'data', 'garamond.otf')
        gara_italic_font = os.path.join(data_path, 'CogManager', 'cogs', 'orly', 'data', 'garamond_italic.otf')
        print(orly_logo)
        W, H = (500, 700)
        try:
            hex = hex.replace("#", "")
        except:
            return await ctx.send("Invalid hex.")
        colour = tuple(int(hex[i:i+2], 16) for i in (0, 2 ,4))+(255,)
        im = Image.new("RGBA", (W,H), (255,255,255,255))
        draw = ImageDraw.Draw(im)
        box_font = ImageFont.truetype(gara_font, 80)
        box_size_w, box_size_h = draw.textsize(box_text, font=box_font)
        title_font = ImageFont.truetype(gara_italic_font, 18)
        title_size_w, title_size_h = draw.textsize(title_text, font=title_font)
        small_font = ImageFont.truetype(gara_italic_font, 24)
        small_size_w, small_size_h = draw.textsize(small_text, font=small_font)
        draw.line((20, 0, 480, 0), width=20, fill=colour)
        draw.line((20, 515, 480, 515), width=175, fill=colour)
        logo = Image.open(orly_logo).resize((100,40), Image.ANTIALIAS)
        im.paste(logo, (30,635), mask=logo)
        inp_im = Image.open(await self.getimage(image_url)).resize((350,350), Image.ANTIALIAS)
        im.paste(inp_im, (75,70), mask=inp_im)
        draw.text(((W-title_size_w)/2, 15), title_text, font=title_font, fill="black")
        draw.text((480-small_size_w, 605), small_text, font=small_font, fill="black")
        lines = textwrap.wrap(box_text, width=8)[:2]
        line_h, pad = 443, 10
        for line in lines:
            lw, lh = draw.textsize(line, font=box_font)
            draw.text((25, line_h), line, font=box_font)
            line_h += lh + pad
        img = BytesIO()
        im.save(img, "png")
        img.seek(0)
        await ctx.send(file=discord.File(img, "orly.png"))

    async def getimage(self, url):
        data = await (await self.session.get(url)).read()
        img = BytesIO(data)
        return img
