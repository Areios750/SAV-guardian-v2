import discord
from .bear_select import BearSelect


class BearView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(BearSelect())