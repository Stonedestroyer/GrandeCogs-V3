import discord
from redbot.core import checks, commands
from redbot.core import Config
from redbot.core.data_manager import bundled_data_path
from aiohttp import web
import asyncio

BaseCog = getattr(commands, "Cog", object)

class WebServer(BaseCog):
    def __init__(self, bot):
        self.bot = bot
        self.host = "0.0.0.0"
        self.server = None
        self.app = web.Application()
        self.handler = None
        self.config = Config.get_conf(self, identifier=3723456754567, force_registration=True)
        self.config.register_global(port=8000)
        self.web = self.bot.loop.create_task(self.make_webserver())

    def __unload(self):
        self.web.cancel()
        asyncio.gather(runner.cleanup())

    @commands.group()
    async def webserver(self, ctx):
        """WebServer"""
        pass

    @webserver.command()
    @checks.is_owner()
    async def upload(self, ctx):
        """Upload website index.html"""
        attachments = ctx.message.attachments
        if len(attachments) > 1:
            await ctx.send("More than one file uploaded, please upload a single file called `index.html`.")
            return
        file = attachments[0]
        if file.filename != "index.html":
            await ctx.send("Invalid file, please upload a file called `index.html`.")
            return
        filepath = bundled_data_path(self) / 'index.html'
        await file.save(f"{filepath}")
        await ctx.send("New index set!")

    @webserver.command()
    @checks.is_owner()
    async def port(self, ctx, port:int):
        """Change webServer port."""
        await self.config.port.set(port)
        await ctx.send("Port updated!\nRestart to use the new port.")

    async def make_webserver(self):
        global runner
        routes = web.RouteTableDef()

        @routes.get("/")
        async def index(request):
            try:
                filepath = bundled_data_path(self) / "index.html"
                with open(filepath) as f:
                    body = f.read()
            except:
                filepath = bundled_data_path(self) / "default.html"
                with open(filepath) as f:
                    body = f.read()
            return web.Response(text=body, content_type="text/html")

        @routes.get("/*")
        async def index(request):
            print(request.path())
            try:
                filepath = bundled_data_path(self) / request.path()
                with open(filepath) as f:
                    body = f.read()
            except:
                try:
                    filepath = bundled_data_path(self) / "index.html"
                    with open(filepath) as f:
                        body = f.read()
                except:
                    filepath = bundled_data_path(self) / "default.html"
                    with open(filepath) as f:
                        body = f.read()
            return web.Response(text=body, content_type="text/html")

        await asyncio.sleep(10)
        app = web.Application()
        app.add_routes(routes)
        runner = web.AppRunner(app)
        await runner.setup()
        port = await self.config.port()
        site = web.TCPSite(runner, self.host, port)
        await site.start()
        print(f"[WEBSERVER] Serving on http://{self.host}:{port}")
