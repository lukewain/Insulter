from prisma import Prisma
import asyncio

from bot.Insulter import Insulter

import helpers

async def start():
    p = Prisma()
    await p.connect()

    bot = Insulter(config=helpers.Config.from_env(), prisma=p)

    await bot.start(bot.token)


if __name__ == "__main__":
    asyncio.run(start())