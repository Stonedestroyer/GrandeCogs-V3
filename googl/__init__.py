from .googl import Googl

def setup(bot):
    bot.add_cog(Googl(bot))
