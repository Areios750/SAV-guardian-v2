import discord

from views.alliance_select import AllianceSelectView


class CheckInView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="📝 Complete Check-In",
        style=discord.ButtonStyle.green,
        custom_id="checkin_button"
    )
    async def checkin_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "Please choose your current alliance:",
            view=AllianceSelectView(),
            ephemeral=True
        )