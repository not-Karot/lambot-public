from discord.ext import tasks, commands


class DatabaseManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update.start()

    @tasks.loop(minutes=6.0)
    async def update(self):
        """This method updates the database every 6 minutes"""
        tags = self.bot.dbconn.player.get_players()
        tag_list = [tag[1] for tag in tags]
        async for player in self.bot.coc.get_players(tag_list):
            self.bot.dbconn.player.update_player((player.town_hall, player.name, player.tag))

    @update.before_loop
    async def before_update(self):
        """This method prevents the task from running before the bot is connected"""
        await self.bot.wait_until_ready()

    @commands.command(name="update_db", aliases=["updatedb", "dbupdate"], hidden=True)
    @commands.is_owner()
    async def update_db(self, ctx):
        try:
            await self.update()
            return await ctx.send("Database is now up to date")
        except:
            return await ctx.send("Something went wrong")

    @commands.command(name="create_league", aliases=["createleague", "addleague"], hidden=True)
    @commands.is_owner()
    async def create_league(self, ctx, name, season, division, description):
        if name:
            self.bot.dbconn.comm_league.add_league((name, season, division, description))
            await ctx.send(f"League {name} has been created")
        else:
            await ctx.send("Please insert a valid name")


def setup(bot):
    bot.add_cog(DatabaseManager(bot))
