import coc, numpy as np
import discord
from discord.ext import commands
from coc import utils
import utility, typing
from service.AttackService import AttackService
from service.WarService import WarService
from service.PlayerService import PlayerService
from service.LineupService import LineupService
from service.ClanService import ClanService
from disputils import BotEmbedPaginator


class Lineupmanager(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.attackService = AttackService(bot)
        self.warService = WarService(self.bot)
        self.playerService = PlayerService()
        self.clanService = ClanService(bot)
        self.service = LineupService(bot)

    @commands.command(name="get_best_hitters", aliases=["gbh", "get_hitrate", "getbesthitters"],
                      brief="Returns best attackers")
    async def get_best_hitters(self, ctx, th: typing.Optional[int] = None, clan_tag=None):
        """Add th level to filter on th level and/or clan to filter on a clan
            NOTE: if channel is linked to a clan, clan filter will be applied"""
        # Se non viene fornito un clan_tag si controlla se c'è un clan linkato al canale e in caso affermativo si usa
        # quello, in caso negativo non viene effettuato il filtering sul clan

        if clan_tag:
            try:
                clan = await self.bot.coc.get_clan(clan_tag)
            except coc.errors.NotFound:
                return await ctx.send("Please insert valid tag")
        else:
            clan_tag = self.warService.dict.get(ctx.channel.id, 0)

            if clan_tag == 0:
                clan = None
            else:
                clan_tag = clan_tag[0]
                clan = await self.bot.coc.get_clan(clan_tag)
        response = self.attackService.getHitrate(clan, th)

        embeds = self.service.createHittersList(response)
        if not embeds:
            return await ctx.send("Nothing to show")
        if not th:
            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()
        else:

            return await ctx.send(embed=embeds[0])

    @commands.command(name="create_lineup", aliases=["createlineup"],
                      brief="Creates lineup based on best clan attackers")
    @commands.has_role("Leader")
    @commands.has_role("Co-leader")
    async def create_lineup(self, ctx, league_name=None, league_season=None, league_division=None, *ths):
        """Please provide the war breakdown from max th level to min required
            Ex: lb create_lineup 0 5 10 15"""
        if not league_name or not league_season or not league_division:
            return await ctx.send(
                "Please insert a valid league parameters. You can check them by typing `lb get_league_infos`")

        league = [league_name, league_season, league_division]
        check = False
        for item in self.clanService.getLeagueInfos():
            inner_check = np.array_equal(np.array(league).sort(),
                                         np.array(item).sort())
            if inner_check:
                check = True
                break
        if not check:
            return await ctx.send(
                "Please insert a valid league parameters. You can check them by typing `lb get_league_infos`")
        if not ths:
            return await ctx.send("Please insert a valid war format")
        clan_tag = self.warService.dict.get(ctx.channel.id, 0)

        if clan_tag == 0:
            return await ctx.send("No clan linked to this channel. You need to link a clan first.")
        else:
            clan_tag = clan_tag[0]
            clan = await self.bot.coc.get_clan(clan_tag)
        size = 0
        ths_list = []
        for th in ths:
            try:
                size += int(th)
                ths_list.append(int(th))
            except ValueError:
                return await ctx.send("Please insert a valid th level")
        if size % 5 != 0 or size > 50:
            return await ctx.send("Please insert a valid war format")
        try:
            lineup = self.service.createLineup(clan, ths_list, league)
        except ValueError:
            return await ctx.send("I'm sorry, not enough players in my database to fill the war breakdown")

        for player in lineup:
            await ctx.send(player)


def setup(bot):
    bot.add_cog(Lineupmanager(bot))
