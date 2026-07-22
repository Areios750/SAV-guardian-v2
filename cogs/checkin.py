import discord
from discord import app_commands
from discord.ext import commands

from views.checkin_view import CheckInView


class CheckIn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="setup-checkin",
        description="Publie le panneau de Check-In."
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_checkin(self, interaction: discord.Interaction):
        # Acquitter immédiatement pour éviter un timeout si l'envoi est lent
        await interaction.response.defer(ephemeral=True)

        embed = discord.Embed(
            title="🛡️ Welcome to SAV Family",
            description=(
                "Welcome to the official SAV Family Discord!\n\n"
                "Before accessing the server, you must complete your Check-In."
            ),
            color=0xD4AF37
        )

        embed.add_field(
            name="📋 Required Information",
            value=(
                "• In-Game Name\n"
                "• Player ID\n"
                "• Current Alliance"
            ),
            inline=False
        )

        await interaction.channel.send(
            embed=embed,
            view=CheckInView()
        )

        await interaction.followup.send(
            "✅ Check-In panel created.",
            ephemeral=True
        )

    @setup_checkin.error
    async def setup_checkin_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "❌ You need Administrator permissions to use this command.",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(CheckIn(bot))