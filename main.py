from prisma import Prisma
import asyncio

p = Prisma()

async def test():
    await p.connect()
    # Query db to ensure proper connection
    await p.admin.find_first()
    print("Connected to database")
    await p.disconnect()

asyncio.run(test())