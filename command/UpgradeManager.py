import coc
import discord
from discord.ext import tasks, commands
from coc import utils
from service.UpgradeService import UpgradeService


class UpgradeManager(commands.Cog):
    """Description of what this file does"""

    def __init__(self, bot):
        self.bot = bot
        self.service = UpgradeService(self.bot)

    @commands.command(name="add_upgrade", aliases=["upgrade", "setugrade", "set_upgrade"])
    async def add_upgrade(self, ctx, player_tag, previous_th=0, target_th=1):
        """Adds an account upgrade to the database"""
        try:
            int(previous_th)
            int(target_th)
        except ValueError:
            await ctx.send("Please insert valid Townhall levels")
            return

        player_tag = utils.correct_tag(player_tag)

        try:
            player = await self.bot.coc.get_player(player_tag)
        except coc.errors.NotFound:
            await ctx.send("Please insert valid tag")
            return
        if previous_th != 0 and target_th != 1:
            if target_th <= previous_th:
                return await ctx.send("Please insert valid Townhall levels")
        else:
            previous_th = player.town_hall
            target_th += previous_th
        self.bot.dbconn.upgrade.register_update((player.tag, previous_th, target_th))

        await ctx.send(f"Account set to upgrade: {player.name}, from TH{previous_th} to TH{target_th}. Enjoy farming")

    @commands.command(name="get_upgrades", aliases=["upgrades", "getupgrades"])
    async def get_upgrades(self, ctx):
        """Returns all upgrades currently ongoing"""
        response = self.bot.dbconn.upgrade.get_upgrades()

        embeds = await self.service.createUpgradesList(response, self.bot)
        for embed in embeds:
            await ctx.send(embed=embed)

    @commands.command(name="delete_upgrades", aliases=["clear_upgrades"])
    @commands.is_owner()
    async def delete_upgrades(self, ctx):
        """Deletes all upgrades currently ongoing"""

        self.bot.dbconn.upgrade.clear_updates()
        await ctx.send("All updates are now cleared")


def setup(bot):
    bot.add_cog(UpgradeManager(bot))
