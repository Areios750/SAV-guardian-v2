import os
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv

from views.checkin_view import CheckInView

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing from .env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("SAVGuardian")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


class SAVGuardian(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):
        # Enregistre la vue persistante pour que le bouton survive aux redémarrages
        self.add_view(CheckInView())

        await self.load_extension("cogs.checkin")

        # tree.sync() ne doit être appelé qu'après un changement de commandes.
        # Commenter cette ligne une fois les commandes déployées.
        await self.tree.sync()
        logger.info("Extension 'checkin' chargée et slash commands synchronisées.")


bot = SAVGuardian()


@bot.event
async def on_ready():
    logger.info("=" * 40)
    logger.info(f"Connecté en tant que {bot.user} (ID: {bot.user.id})")
    logger.info("=" * 40)


bot.run(TOKEN)