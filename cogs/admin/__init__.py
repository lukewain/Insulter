from .features import AdminFeatures

from bot.Insulter import Insulter

class Admin(AdminFeatures):
    def __init__(self, bot: Insulter):
        self.bot: Insulter = bot


async def setup(bot: Insulter):
    await bot.add_cog(Admin(bot))