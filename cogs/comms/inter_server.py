from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from logging import getLogger

from bot.Insulter import Insulter

log = getLogger("EXT.COMMS.INTER_SERVER")


class InterServer(commands.Cog):
    # Feature for inter-server commands
    # Create startup process which will verify if the feature is in the table
    def __init__(self, bot: Insulter):
        self.bot = bot

    async def cog_load(self):
        log.debug("Running cog load")

        # Verify if the feature is in the table
        log.debug("Checking feature table for module INTER-SERVER-COMMS")
        d = await self.bot.prisma.feature.find_first(
            where={
                "registeredName": "inter-server-comms"
            }
        )

        if not d:
            # Create the feature in the table
            await self.bot.prisma.feature.create(
                data={
                    "registeredName": "inter-server-comms",
                    "name": "Inter-Server Communications",
                    "description": "Fun commands which will allow for chats with other servers",
                }
            )
        else:
            if not d.loaded:
                # Enable the feature
                await self.bot.prisma.feature.update(
                    where={
                        "registeredName": "inter-server-comms"
                    },
                    data={
                        "enabled": True
                    }
                )

    async def cog_unload(self):
        log.debug("Running cog unload")

        # Verify if the feature is in the table
        log.debug("Checking feature table for module INTER-SERVER-COMMS")
        d = await self.bot.prisma.feature.find_first(
            where={
                "registeredName": "inter-server-comms"
            }
        )

        if d:
            # Disable the feature
            await self.bot.prisma.feature.update(
                where={
                    "registeredName": "inter-server-comms"
                },
                data={
                    "enabled": False
                }
            ) 

    async def interaction_check(self, interaction: discord.Interaction[Insulter]):
        # Pull blacklist data from table and check against user
        blacklistUser = await self.bot.prisma.blacklist.find_unique(where={"id": interaction.user.id})

        if blacklistUser:
            await interaction.response.send_message("You are blacklisted from using this bot", ephemeral=True)
            return False
        else:
            return True
        

    comms = app_commands.Group(name="comms", description="Inter-Server Communications")

    @comms.command(name="connect", description="Connect to another server")
    async def connect(self, interaction: discord.Interaction[Insulter]):
        await interaction.response.send_message("Connected to another server", ephemeral=True)