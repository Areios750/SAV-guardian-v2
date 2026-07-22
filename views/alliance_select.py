import discord

from modals.checkin_modal import CheckInModal


class AllianceSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="SAV", emoji="🛡️"),
            discord.SelectOption(label="Mini SAV", emoji="⚔️"),
            discord.SelectOption(label="SHE", emoji="🦅"),
            discord.SelectOption(label="LwT", emoji="🐺"),
            discord.SelectOption(label="STG", emoji="🔥"),
            discord.SelectOption(label="Other", emoji="❓"),
        ]

        super().__init__(
            placeholder="Choose your current alliance...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        alliance = self.values[0]

        await interaction.response.send_modal(
            CheckInModal(alliance)
        )


class AllianceSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(AllianceSelect())

    async def on_timeout(self):
        # Désactive le menu et informe l'utilisateur si le délai est dépassé
        for item in self.children:
            item.disabled = True
        # La vue est éphémère, on ne peut pas éditer le message depuis ici.
        # Le timeout désactive simplement les composants côté Discord.