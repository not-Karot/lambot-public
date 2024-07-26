import coc
import discord
from discord.ext import tasks, commands
from coc import utils
import utility, typing
from service.PlayerService import PlayerService
from service.AttackService import AttackService
from disputils import BotEmbedPaginator


class PlayerManager(commands.Cog):
    """Description of what this file does"""

    def __init__(self, bot):
        self.bot = bot
        self.attackService = AttackService(bot)
        self.service = PlayerService()

    @commands.command(name="add_player", aliases=["avatar", "claim"], brief="Links a coc account to a discord user")
    async def add_player(self, ctx, player_tag, user: discord.Member = None):
        """If no user is given, default user is the command invoker"""

        if not player_tag:
            return await ctx.send("Please insert a tag")
        player_tag = utils.correct_tag(player_tag)
        try:
            player = await self.bot.coc.get_player(player_tag)
        except coc.errors.NotFound:
            return await ctx.send("Please insert valid tag")

        if not user:
            user = ctx.author
        self.bot.dbconn.player.register_user((player.tag, player.name, player.town_hall, user.id))
        await ctx.send(f"Account linked: {player.name}, {user.mention}")

    @commands.command(name="delete_player", aliases=["unclaim"], brief="Unlinks a coc account to a discord user")
    async def delete_player(self, ctx, player_tag):
        """If no user is given, default user is the command invoker"""

        if not player_tag:
            return await ctx.send("Please insert a tag")
        player_tag = utils.correct_tag(player_tag)
        try:
            player = await self.bot.coc.get_player(player_tag)
        except coc.errors.NotFound:
            return await ctx.send("Please insert valid tag")
        self.bot.dbconn.player.delete_player(player.tag)
        return await ctx.send(f"Account unlinked")

    @commands.command(name="get_all", aliases=["getall"], hidden=True)
    @commands.is_owner()
    async def get_all(self, ctx):

        response = self.bot.dbconn.player.get_players()
        if not response:
            return await ctx.send("Nothing to show")

        embeds = await self.service.createPlayersList(response, self.bot)

        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()

    @commands.command(name="get_all_linked", aliases=["list", "getme"],
                      brief="Returns all coc accounts linked to a discord user")
    async def get_all_linked(self, ctx, user: discord.Member = None):
        """If no user is given, default user is the command invoker"""

        if not user:
            user = ctx.author
        response = self.bot.dbconn.player.get_accounts_by_id(str(user.id))

        descrizione = self.service.createPlayerList(response)

        embed = discord.Embed(color=discord.Color.random(), description=descrizione)

        embed.set_image(url=utility.getRandomImage())
        embed.set_footer(text=f"Discord ID: {user.name}",
                         icon_url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="get_player_stats", aliases=["getplayerstats", "gps", "mystats"],
                      brief="Returns player stats")
    async def get_player_stats(self, ctx, user: typing.Optional[discord.Member] = None, clan_tag=None):
        """If no user is given, default user is the command invoker
            Type a clan tag to filter stats by a clan"""

        if not user:
            user = ctx.author
        if clan_tag:
            try:
                clan = await self.bot.coc.get_clan(clan_tag)
            except coc.errors.NotFound:
                return await ctx.send("Please insert valid tag")
        else:
            clan = None
        embed = self.attackService.getPlayerStats(user, clan)
        return await ctx.send(embed=embed)

    @commands.command(name="get_players_stats", aliases=["getplayersstats", "gpss", "allstats"], brief="Returns all players stats")
    async def get_players_stats(self, ctx, clan_tag=None):
        """Type a clan tag to filter stats by a clan"""
        if clan_tag:
            try:
                clan = await self.bot.coc.get_clan(clan_tag)
            except coc.errors.NotFound:
                return await ctx.send("Please insert valid tag")
        else:
            clan = None
        embeds = await self.attackService.getPlayersStats(clan)

        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()

    @commands.command(name="is_in_war", aliases=["isinwar"], hidden=True)
    async def is_in_war(self, ctx, player_tag):
        """Checks if a certain account is eligible for war or not"""
        # TODO
        if "todo" == "todo":
            return await ctx.send("COMMAND NOT IMPLEMENTED YET")
        if not player_tag:
            return await ctx.send("Please insert a tag")
        player_tag = utils.correct_tag(player_tag)
        try:
            player = await self.bot.coc.get_player(player_tag)
        except coc.errors.NotFound:
            return await ctx.send("Please insert valid tag")

        if player.war() is None:
            return ctx.send("Player is not in war")
        else:
            return ctx.send("player is in war")


def setup(bot):
    bot.add_cog(PlayerManager(bot))
