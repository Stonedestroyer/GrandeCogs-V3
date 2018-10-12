from .codestats import CodeStats

def setup(bot):
    bot.add_cog(CodeStats(bot))
