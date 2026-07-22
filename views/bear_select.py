import discord

from config import BEAR1_ROLE_ID, BEAR2_ROLE_ID


class BearSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Bear 1",
                emoji="🐻",
                description="Main Bear group"
            ),
            discord.SelectOption(
                label="Bear 2",
                emoji="🐻",
                description="Second Bear group"
            ),
        ]

        super().__init__(
            placeholder="Choose your Bear group...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        # Acquitter l'interaction immédiatement pour éviter le timeout de 3s
        # (surtout sur mobile où la latence est plus élevée)
        await interaction.response.defer(ephemeral=True)

        member = interaction.user

        bear1_role = interaction.guild.get_role(BEAR1_ROLE_ID)
        bear2_role = interaction.guild.get_role(BEAR2_ROLE_ID)

        # Retire les deux rôles Bear en un seul appel pour éviter les doublons
        # (Discord ignore silencieusement les rôles que le membre n'a pas)
        await member.remove_roles(bear1_role, bear2_role)

        # Attribue le rôle choisi
        if self.values[0] == "Bear 1":
            await member.add_roles(bear1_role)
        else:
            await member.add_roles(bear2_role)

        await interaction.followup.send(
            f"✅ Check-In completed successfully!\n\n"
            f"Welcome to **SAV Family**! 🛡️\n\n"
            f"🐻 You have been assigned to **{self.values[0]}**.",
            ephemeral=True
        )