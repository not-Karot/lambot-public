import coc
from coc import utils
import discord
import numpy as np
from discord.ext import tasks, commands
from service.ClanService import ClanService
from service.WarService import WarService


class ClanManager(commands.Cog):
    """Description of what this file does"""

    def __init__(self, bot):
        self.bot = bot
        self.service = ClanService(bot)
        self.leagues = self.service.getLeagueInfos()
        self.warService = WarService(bot)
        self.update.start()

    @tasks.loop(minutes=600.0)
    async def update(self):
        """Ogni 10 ore aggiorna la lista delle leghe disponibili"""
        self.leagues = self.service.getLeagueInfos()

    @commands.command(name="update_leagues", aliases=["updateleagues", "updateleague"], hidden=True)
    @commands.is_owner()
    async def update_leagues(self, ctx):
        self.leagues = self.service.getLeagueInfos()
        await ctx.send("Leagues are now up to date")

    @commands.command(name="get_clan", aliases=["getclan", "clan"])
    async def get_clan(self, ctx, clan_tag):
        """Returns clan infos"""
        # This line uses a utility in the coc.py library to correct clan tags (case, missing #, etc.)
        if not clan_tag:
            return await ctx.send("You need to insert a clan tag")
        clan_tag = coc.utils.correct_tag(clan_tag)

        try:
            clan = await self.bot.coc.get_clan(clan_tag)
        except coc.errors.NotFound:
            return await ctx.send("Please insert valid tag")

        content = f"The clan name for {clan_tag} is {clan.name}.\n"
        content += f"{clan.name} currently has {clan.member_count} members.\n\n"

        war = await self.bot.coc.get_current_war(clan_tag)
        if war:
            content += f"Current war state is {war.state}\n"
            if war.state != "notInWar":
                content += f"Opponent: {war.opponent}"

        await ctx.send(content)

    @commands.command(name="get_league_infos", aliases=["getleagueinfos", "gli", "getleaguenames"],
                      brief="Returns league infos")
    async def get_league_infos(self, ctx):
        """Returns league infos in order to update master roster properly"""
        if not self.leagues:
            return ctx.send("Nothing to show")
        new_line = "\n"
        names = new_line.join(item[0] for item in self.leagues)
        seasons = new_line.join(item[1] for item in self.leagues)
        divisions = new_line.join(item[2] for item in self.leagues)
        embed = discord.Embed(title="League infos")
        embed.add_field(name="Name", value=names)
        embed.add_field(name="Season", value=seasons)
        embed.add_field(name="Division", value=divisions)

        await ctx.send(embed=embed)

    @commands.command(name="add_to_master_roster", aliases=["addmr", "addtomr", "mradd", "addtomasterroster"],
                      brief="Add player to league master roster")
    @commands.has_role("Leader")
    async def add_to_master_roster(self, ctx, league_name=None, league_season=None, league_division=None, *player_tags):
        """Add player to league master roster
        You can provide multiple players too"""
        if not league_name or not league_season or not league_division:
            return await ctx.send(
                "Please insert a valid league parameters. You can check them by typing `lb get_league_infos`")
        clan_tag = self.warService.dict.get(ctx.channel.id, 0)

        if clan_tag == 0:
            return await ctx.send("No clan linked to this channel. You need to link a clan first.")
        else:
            clan_tag = clan_tag[0]
        league = [league_name, league_season, league_division]
        check = False
        for item in self.leagues:
            inner_check = np.array_equal(np.array(league).sort(),
                                         np.array(item).sort())
            if inner_check:
                check = True
                break
        if not check:
            return await ctx.send(
                "Please insert a valid league parameters. You can check them by typing `lb get_league_infos`")

        if not player_tags:
            return await ctx.send("Please insert a tag")
        corrected_tags = []
        for player_tag in player_tags:

            corrected_tags.append(utils.correct_tag(player_tag))
            try:
                player = await self.bot.coc.get_player(player_tag)
            except coc.errors.NotFound:
                return await ctx.send("Please insert valid tag")

        if self.service.addMasterRoster(clan_tag, corrected_tags, league):
            return await ctx.send("Everything went good!")
        else:
            return await ctx.send("Ops, something went wrong")

    @commands.command(name="remove_from_master_roster",
                      aliases=["removemr", "removefrommr", "mrremove", "removefrommasterroster"],
                      brief="Remove player from league master roster")
    @commands.has_role("Leader")
    async def remove_from_master_roster(self, ctx, league_name=None, league_season=None, league_division=None,
                                        *player_tags):
        """Remove player from league master roster
        You can provide multiple players too"""
        if not league_name or not league_season or not league_division:
            return await ctx.send(
                "Please insert a valid league parameters. You can check them by typing `lb get_league_infos`")
        clan_tag = self.warService.dict.get(ctx.channel.id, 0)

        if clan_tag == 0:
            return await ctx.send("No clan linked to this channel. You need to link a clan first.")
        else:
            clan_tag = clan_tag[0]
        league = [league_name, league_season, league_division]
        check = False
        for item in self.leagues:
            inner_check = np.array_equal(np.array(league).sort(),
                                         np.array(item).sort())
            if inner_check:
                check = True
                break
        if not check:
            return await ctx.send(
                "Please insert a valid league parameters. You can check them by typing `lb get_league_infos`")

        if not player_tags:
            return await ctx.send("Please insert a tag")
        for player_tag in player_tags:

            player_tag = utils.correct_tag(player_tag)
            try:
                player = await self.bot.coc.get_player(player_tag)
            except coc.errors.NotFound:
                return await ctx.send("Please insert valid tag")

        if self.service.removeFromMasterRoster(clan_tag, player_tags, league):
            return await ctx.send("Everything went good!")
        else:
            return await ctx.send("Ops, something went wrong")

    @commands.command(name="get_master_roster", aliases=["getmasterroster", "gmr"])
    @commands.has_role("Leader")
    async def get_master_roster(self, ctx, league_name=None, league_season=None, league_division=None):

        """Returns all linked accounts who played in clan
        Can be filtered to league"""
        clan_tag = self.warService.dict.get(ctx.channel.id, 0)
        if clan_tag == 0:
            return await ctx.send("No clan linked to this channel")
        else:
            clan_tag = clan_tag[0]
            clan = await self.bot.coc.get_clan(clan_tag)
        league = None
        if league_name:
            if league_season and league_division:
                league = [league_name, league_season, league_division]
                check = False
                for item in self.leagues:
                    inner_check = np.array_equal(np.array(league).sort(),
                                                 np.array(item).sort())
                    if inner_check:
                        check = True
                        break
                if not check:
                    return await ctx.send(
                        "Please insert a valid league parameters. You can check them by typing `lb get_league_infos`")
            else:
                return await ctx.send(
                    "Please insert a valid league parameters. You can check them by typing `lb get_league_infos`")

        result = self.service.getMasterRoster(clan, league)
        for player in result:
            await ctx.send(player)


def setup(bot):
    bot.add_cog(ClanManager(bot))
