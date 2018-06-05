from .scanport import ScanPort

def setup(bot):
    bot.add_cog(ScanPort(bot))
