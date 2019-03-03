from .glances import Glances

def setup(bot):
    bot.add_cog(Glances(bot))