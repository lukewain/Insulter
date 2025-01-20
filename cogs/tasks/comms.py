from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands, tasks

from logging import getLogger

from bot.Insulter import Insulter

log = getLogger("EXT.TASKS.COMMS")

class CommTasks(commands.Cog):
    def __init__(self, bot: Insulter):
        self.bot: Insulter = bot
        self.cleanup_old_messages.start()

    async def cog_load(self):
        log.debug("Running cog load")

        # Verify if the feature is in the table
        log.debug("Checking feature table for module TASKS-COMMS")
        d = await self.bot.prisma.feature.find_first(
            where={
                "registeredName": "tasks-comms"
            }
        )

        if not d:
            # Create the feature in the table
            await self.bot.prisma.feature.create(
                data={
                    "registeredName": "tasks-comms",
                    "name": "Task centre for Communication Extension",
                    "description": "A feature which allows for the creation of tasks and their completion",
                }
            )
        else:
            if not d.loaded:
                # Enable the feature
                await self.bot.prisma.feature.update(
                    where={
                        "registeredName": "tasks-comms"
                    },
                    data={
                        "enabled": True
                    }
                )

    async def cog_unload(self):
        log.debug("Running cog unload")

        # Verify if the feature is in the table
        log.debug("Checking feature table for module TASKS-COMMS")
        d = await self.bot.prisma.feature.find_first(
            where={
                "registeredName": "tasks-comms"
            }
        )

        if d:
            # Disable the feature
            await self.bot.prisma.feature.update(
                where={
                    "registeredName": "tasks-comms"
                },
                data={
                    "enabled": False
                }
            )


        self.cleanup_old_messages.cancel()


    @tasks.loop(minutes=5)
    async def cleanup_old_messages(self):
        log.debug("Running cleanup old messages")

        count = await self.bot.prisma.message.delete_many(where={"store_until": {"gte": discord.utils.utcnow()}})

        logentry = await self.bot.prisma.logchannels.find_first(where={"feature": "tasks-comms"})
        
        if logentry:
            channel = self.bot.get_channel(logentry.id)
            if not channel:
                channel = await self.bot.fetch_channel(logentry.id)

            if not type(channel) == discord.TextChannel:
                log.warning(f"Channel {logentry.id} is not a valid text channel".format(logentry.id))


            await channel.send(f"Deleted {count} old messages")
        
        else:
            log.info(f"Deleted {count} old messages")

    @cleanup_old_messages.before_loop()
    async def before_message_clean(self):
        log.debug("Waiting until ready")
        await self.bot.wait_until_ready()