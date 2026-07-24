import discord
import logging
from .bear_select import BearSelect

logger = logging.getLogger("SAVGuardian")


class BearView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(BearSelect())

    async def on_error(self, interaction: discord.Interaction, error: Exception, item):
        logger.exception(f"BearView.on_error — item: {item}, user: {interaction.user}", exc_info=error)