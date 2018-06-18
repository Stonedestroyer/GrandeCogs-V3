from .freelancer import Freelancer

def setup(bot):
    bot.add_cog(Freelancer(bot))
