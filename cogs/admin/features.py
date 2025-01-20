from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from logging import getLogger

from bot.Insulter import Insulter

log = getLogger("EXT.ADMIN.FEATURES")

__all__ = ("AdminFeatures")

class AdminFeatures(commands.Cog):
    def __init__(self, bot: Insulter):
        self.bot: Insulter = bot

    async def cog_load(self):
        log.debug("Running cog load")

        # Verify if the feature is in the table
        log.debug("Checking feature table for module ADMIN-FEATURES")
        d = await self.bot.prisma.feature.find_first(
            where={
                "registeredName": "admin-features"
            }
        )

        if not d:
            # Create the feature in the table
            await self.bot.prisma.feature.create(
                data={
                    "registeredName": "admin-features",
                    "frontendName": "Admin features",
                    "description": "Admin features",
                }
            )
        else:
            if not d.loaded:
                # Enable the feature
                await self.bot.prisma.feature.update(
                    where={
                        "registeredName": "admin-features"
                    },
                    data={
                        "enabled": True
                    }
                ) 

        
    async def cog_unload(self):
        log.debug("Running cog unload")

        # Verify if the feature is in the table
        log.debug("Checking feature table for module ADMIN-FEATURES")
        d = await self.bot.prisma.feature.find_first(
            where={
                "registeredName": "admin-features"
            }
        )

        if d:
            # Disable the feature
            await self.bot.prisma.feature.update(
                where={
                    "registeredName": "admin-features"
                },
                data={
                    "enabled": False
                }
            )

        
    admin = app_commands.Group(name="admin", description="Admin features")
    features = app_commands.Group(name="features", description="Admin features", parent=admin)

    @features.command(name="list", description="List all features")
    @app_commands.describe(ephemeral="Show message to only you")
    @app_commands.describe(onlyactive="Only show active features")
    async def adminFeaturesList(self, interaction: discord.Interaction[Insulter], ephemeral: bool, onlyactive: bool = False):
        if onlyactive:
            features = await self.bot.prisma.feature.find_many(where={"enabled": True})
        else:
            features = await self.bot.prisma.feature.find_many()
        
        if len(features) == 0:
            await interaction.response.send_message("No features found", ephemeral=ephemeral)
            return
    
        embeds: list[discord.Embed] = []
        
        for feature in features:
            embed = discord.Embed(title="Features", color=discord.Color.green())
            embed.add_field(name=feature.frontendName, value=f"{'✔' if feature.loaded else '❌'} {feature.description}", inline=False)
            embeds.append(embed)

        await interaction.response.send_message(embeds=embeds)

    
    @features.command(name="enable", description="Enable a feature")
    async def adminFeaturesEnable(self, interaction: discord.Interaction[Insulter], feature: str):
        await self.bot.prisma.feature.update(
            where={
                "frontendName": feature
            },
            data={
                "enabled": True
            }
        )