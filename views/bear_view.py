import discord
import logging

from config import BEAR1_ROLE_ID, BEAR2_ROLE_ID

logger = logging.getLogger("SAVGuardian")


class BearView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Bear 1",
        emoji="🐻",
        style=discord.ButtonStyle.primary,
        custom_id="bear_1_button"
    )
    async def bear1_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._assign_bear(interaction, "Bear 1")

    @discord.ui.button(
        label="Bear 2",
        emoji="🐻",
        style=discord.ButtonStyle.secondary,
        custom_id="bear_2_button"
    )
    async def bear2_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._assign_bear(interaction, "Bear 2")

    async def _assign_bear(self, interaction: discord.Interaction, bear_choice: str):
        logger.info(f"BearView callback déclenché — {interaction.user} → {bear_choice}")

        try:
            await interaction.response.defer(ephemeral=True)

            member = interaction.user
            bear1_role = interaction.guild.get_role(BEAR1_ROLE_ID)
            bear2_role = interaction.guild.get_role(BEAR2_ROLE_ID)

            if bear1_role is None or bear2_role is None:
                raise ValueError(f"Rôle introuvable — Bear1: {bear1_role}, Bear2: {bear2_role}")

            await member.remove_roles(bear1_role, bear2_role)

            if bear_choice == "Bear 1":
                await member.add_roles(bear1_role)
            else:
                await member.add_roles(bear2_role)

            await interaction.followup.send(
                f"✅ Check-In completed successfully!\n\n"
                f"Welcome to **SAV Family**! 🛡️\n\n"
                f"🐻 You have been assigned to **{bear_choice}**.",
                ephemeral=True
            )

        except Exception:
            logger.exception("BearView._assign_bear erreur")
            try:
                await interaction.followup.send(
                    "❌ Une erreur est survenue. Contacte un admin.",
                    ephemeral=True
                )
            except Exception:
                pass

    async def on_error(self, interaction: discord.Interaction, error: Exception, item):
        logger.exception(f"BearView.on_error — item: {item}, user: {interaction.user}", exc_info=error)