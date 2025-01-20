from .comms import CommTasks

from bot.Insulter import Insulter

class Tasks(CommTasks):
    def __init__(self, bot: Insulter):
        self.bot: Insulter = bot


async def cog_load(self, bot: Insulter):
    await bot.add_cog(Tasks(bot))