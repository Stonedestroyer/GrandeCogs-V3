import discord
from redbot.core import checks, commands
from redbot.core.data_manager import bundled_data_path
from aiohttp import web

BaseCog = getattr(commands, "Cog", object)

class WebServer(BaseCog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.make_webserver())
        self.server = None
        self.app = web.Application()
        self.handler = None
        self.config = Config.get_conf(self, identifier=3723456754567, force_registration=True)
        self.config.register_global(port=8000)

    @commands.group()
    async def webserver(self, ctx):
        """WebServer"""
        pass

    @webserver.command()
    @checks.is_owner()
    async def upload(self, ctx):
        """Upload website index.html"""
        attachments = ctx.message.attachments
        if len(attachment) > 1:
            await ctx.send("More than one file uploaded, please upload a single file called `index.html`.")
            return
        file = attachments[0]
        if file.filename != "index.html":
            await ctx.send("Invalid file, please upload a file called `index.html`.")
            return
        filepath = bundled_data_path(self) / 'index.html'
        await file.save(filepath)
        await ctx.send("New index set!")

    @webserver.command()
    @checks.is_owner()
    async def port(self, ctx, port:int):
        """Change webServer port."""
        await self.config.port.set(port)
        await self.bot.say("Port updated!")

    async def make_webserver(self):

        async def page(request):
            body = self.settings['content']
            filepath = bundled_data_path(self) / 'index.html'
            with open(filepath) as f:
                body = f.read()
            return web.Response(text=body, content_type='text/html')

        self.app.router.add_get('/', page)
        self.handler = self.app.make_handler()
        port = await self.config.port()
        self.server = await self.bot.loop.create_server(self.handler, '0.0.0.0', port)
        print(f"Serving webserver on port {port}")

    def __unload(self):
        self.server.close()
        self.bot.loop.run_until_complete(self.server.wait_closed())
        self.bot.loop.run_until_complete(self.app.shutdown())
        self.bot.loop.run_until_complete(self.handler.finish_connections(60.0))
        self.bot.loop.run_until_complete(self.app.cleanup())