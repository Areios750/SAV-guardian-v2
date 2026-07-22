import logging

import discord
from config import (
    NEWCOMER_ROLE_ID,
    SAVAGE_ROLE_ID,
    SAV_ROLE_ID,
    MINI_SAV_ROLE_ID,
    SHE_ROLE_ID,
    LWT_ROLE_ID,
    STG_ROLE_ID,
    OTHER_ROLE_ID,
    GENERAL_CHANNEL_ID,
    MEMBER_LOG_CHANNEL_ID,
)
from views.bear_view import BearView

logger = logging.getLogger("SAVGuardian")


class CheckInModal(discord.ui.Modal, title="Complete Check-In"):

    def __init__(self, alliance: str):
        super().__init__()

        self.alliance = alliance

        self.ingame_name = discord.ui.TextInput(
            label="In-Game Name",
            placeholder="Enter your in-game name...",
            required=True,
            max_length=30
        )

        self.player_id = discord.ui.TextInput(
            label="Player ID",
            placeholder="Enter your Player ID...",
            required=True,
            max_length=20
        )

        self.add_item(self.ingame_name)
        self.add_item(self.player_id)

    async def on_submit(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)

        try:
            if not self.player_id.value.isdigit():
                await interaction.followup.send(
                    "❌ Player ID must contain numbers only.",
                    ephemeral=True
                )
                return

            newcomer_role = interaction.guild.get_role(NEWCOMER_ROLE_ID)
            savage_role = interaction.guild.get_role(SAVAGE_ROLE_ID)
            member = interaction.user

            if newcomer_role not in member.roles:
                await interaction.followup.send(
                    "❌ You must have the Newcomer role before completing Check-In.",
                    ephemeral=True
                )
                return

            # Rôle d'alliance — on résout uniquement celui choisi
            alliance_role_ids = {
                "SAV": SAV_ROLE_ID,
                "Mini SAV": MINI_SAV_ROLE_ID,
                "SHE": SHE_ROLE_ID,
                "LwT": LWT_ROLE_ID,
                "STG": STG_ROLE_ID,
                "Other": OTHER_ROLE_ID,
            }

            selected_role = interaction.guild.get_role(alliance_role_ids[self.alliance])

            # Ajoute Savage + rôle d'alliance en un seul appel, puis retire Newcomer
            await member.add_roles(savage_role, selected_role)
            await member.remove_roles(newcomer_role)

            # Change le pseudo
            try:
                await member.edit(nick=self.ingame_name.value)
            except (discord.Forbidden, discord.HTTPException):
                pass

            # Message de bienvenue
            general = interaction.guild.get_channel(GENERAL_CHANNEL_ID)

            if general:
                await general.send(
                    f"🎉 Welcome {member.mention} to **SAV Family**! 🛡️"
                )

            # Logs
            member_log = interaction.guild.get_channel(MEMBER_LOG_CHANNEL_ID)

            if member_log:
                await member_log.send(f"""📝 **New Check-In**

👤 Discord : {member.mention}
🎮 In-Game Name : **{self.ingame_name.value}**
🆔 Player ID : **{self.player_id.value}**
🏰 Alliance : **{self.alliance}**
""")

            # Si SAV → choix Bear
            if self.alliance == "SAV":
                await interaction.followup.send(
                    "🐻 Choose your Bear group:",
                    view=BearView(),
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    "✅ Check-In completed successfully!\n\nWelcome to **SAV Family**! 🛡️",
                    ephemeral=True
                )

        except Exception as e:
            logger.exception("Check-In error")
            await interaction.followup.send(
                "❌ An error occurred during Check-In. Please contact an admin.",
                ephemeral=True
            )