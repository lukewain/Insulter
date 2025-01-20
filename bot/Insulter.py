import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import setup_logging

from prisma import Prisma
from logging import getLogger

import helpers

setup_logging()
log = getLogger(__name__)

class Insulter(commands.Bot):
    def __init__(self, *, config: helpers.Config, prisma: Prisma):
        """
        Initialize the bot with the given configuration and Prisma instance.

        Args:
            config: The bot configuration.
            prisma: The Prisma instance to use for database operations.
        """
        
        log.debug("Running bot initializer")    
        
        self.config: helpers.Config = config
        self.prisma: Prisma = prisma
        self.owner_id: int = config.owner_id
        self.token = config.bot_token

        intents = discord.Intents.all()
        

        super().__init__(
            command_prefix="ib.",
            intents=intents
        )

    async def __aenter__(self):
        ...

    
    async def __aexit__(self, exc_type, exc, tb):
        ...

    
    async def setup_hook(self):
        log.debug("Running setup hook")

        '''
        Keep only the required cogs for startup

        Jishaku
        Cog loading features

        Load features on demand.
        '''

        # Add jishaku to load on startup
        await self.load_extension("jishaku")

    async def on_ready(self):
        log.debug("Running on ready")
        log.info(f"Logged in as {self.user.name}#{self.user.discriminator}")