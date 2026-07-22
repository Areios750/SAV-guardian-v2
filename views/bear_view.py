import discord
from .bear_select import BearSelect


class BearView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.add_item(BearSelect())