from discord.ext import commands
import discord
import coc
import utility
from service.WarService import WarService
from paginator import Paginator, Page


class WarManager(commands.Cog):
    def __init__(self, bot):

        self.bot = bot
        self.service = WarService(self.bot)
        self.bot.coc.add_events(
            self.on_war_attack,
            self.on_war_state_change
        )

        self.bot.coc.add_war_updates(*self.service.getClans())
        self.paginator = Paginator(self.bot)

    def cog_unload(self):
        self.bot.coc.remove_events(
            self.on_war_attack,
            self.on_war_state_change
        )
        self.bot.coc.stop_updates("war")

    @commands.command(name="claimclan", brief="Claim your war clan to a discord channel")
    @commands.has_role("Leader")
    async def claim_clan(self, ctx, clan_tag):
        """Clan attacks will be shown as they come"""
        if not clan_tag:
            return await ctx.send("You need to insert a clan tag")
        clan_tag = coc.utils.correct_tag(clan_tag)

        try:
            clan = await self.bot.coc.get_clan(clan_tag)
        except coc.errors.NotFound:
            return await ctx.send("Please insert valid tag")

        self.service.addElement(ctx.channel.id, clan_tag)

        self.bot.coc.add_war_updates(*self.service.getClans())

        await ctx.send(f"Clan {clan.name} has been linked to this channel ")

    @commands.command(name="post_hits", aliases=["posthits"], brief="Turn on/off post hits feature")
    @commands.has_role("Leader")
    async def post_hits(self, ctx, arg: str):
        """Type lb posthits false to turn off post hits
            Type lb posthits true to turn on post hits"""
        if arg.casefold() == "false" or arg == 0:
            arg = False

        elif arg.casefold() == "true" or arg == 1:
            arg = True

        else:
            return await ctx.send(
                "Sorry I can't understand your parameter. Type one of the following: [false, 0; true, 1]")
        self.service.updatePostHits(ctx.channel.id, arg)

        return await ctx.send(f"Post hits is now set to {arg}")

    @commands.command(name="unclaim_clan", aliases=["unclaimclan"])
    @commands.has_role("Leader")
    async def unclaim_clan(self, ctx):
        """Unclaim your war clan from a discord channel"""
        clan_tag = self.service.dict.get(ctx.channel.id, 0)

        if clan_tag == 0:
            return await ctx.send("No clan linked to this channel")

        self.service.deleteElement(ctx.channel.id)

        await ctx.send(f"Channel is now unlinked to the clan")

    @commands.command(name="my_clan", aliases=["myclan"])
    async def my_clan(self, ctx):
        """Returns clan linked to this discord channel"""
        clan_tag = self.service.dict.get(ctx.channel.id, 0)

        if clan_tag == 0:
            return await ctx.send("No clan linked to this channel")
        else:

            clan = await self.bot.coc.get_clan(clan_tag[0])

        return await ctx.send(f"Clan linked to this channel is {clan.name}")

    @coc.WarEvents.war_attack()
    async def on_war_attack(self, attack, war):
        # Registra un attacco nel db solo se:
        # • è effettuato da un membro del clan amico
        # • il livello del municipio del difensore è pari a quello dell'attaccante
        # • la guerra è di tipo friendly;

        if ((not attack.attacker.is_opponent) and (war.type == "friendly") and
                (attack.attacker.town_hall == attack.defender.town_hall)):
            self.bot.dbconn.attack.register_attack((attack.attacker_tag, war.clan.tag, attack.attacker.town_hall,
                                                    attack.stars, attack.is_fresh_attack, attack.destruction))

        for channel in self.service.getAllChannelsIDByTagPostTrue(war.clan.tag):
            try:
                await self.bot.get_channel(channel).send(self.service.on_war_attack_string(attack, war))
            except AttributeError as e:
                print('Trying to send attack, channel not found')

    @coc.WarEvents.state()
    async def on_war_state_change(self, current_state, war: coc.ClanWar):
        if war.state == "preparation":
            embed = discord.Embed(title=f'{war.clan.name} just found a war!', colour=utility.war_colors.get(war.type))
            embed.add_field(name="Opponent:", value=f"{war.opponent.name}\n" f"{war.opponent.tag}",
                            inline=False)
            embed.add_field(name='War type', value=war.type)
            embed.add_field(name='War size', value=str(war.team_size))
            embed.add_field(name="Start time (UTC):", value=war.start_time.time,
                            inline=False)
            embed.add_field(name="End time (UTC):", value=war.end_time.time,
                            inline=False)
            embed.add_field(name='Attacks per member', value=str(war.attacks_per_member))
            embed.set_thumbnail(url=war.clan.badge.url)
        elif war.state == "inWar":
            response = f"{war.type.capitalize()} war has just begun between **{war.clan.name}** and **{war.opponent.name}**."
            embed = discord.Embed(description=response, color=utility.war_colors.get(war.type))
        elif war.state == "warEnded":
            response = f"{war.type.capitalize()} war has just ended between **{war.clan.name}** and **{war.opponent.name}**.\n"
            if war.status == "won":
                response += f"{war.clan.name} won!"
                color = discord.Color.green()
            elif war.status == "lost":
                response += f"{war.clan.name} lost! :("
                color = discord.Color.red()
            else:
                response += "Looks like a tie!"
                color = discord.Color.dark_gold()
            score = f"The score is: {str(war.clan.stars)} ({str(war.clan.destruction)}%) - {str(war.opponent.stars)} ({str(war.opponent.destruction)}%)"
            embed = discord.Embed(title=score, description=response, color=color)
        else:
            response = f"War state is {war.state} for {war.clan.name}"
            embed = discord.Embed(description=response, color=discord.Color.dark_grey())
        for channel in self.service.getAllChannelsIDByTagPostTrue(war.clan.tag):
            try:
                await self.bot.get_channel(channel).send(embed=embed)
            except AttributeError as e:
                print('Trying to send status, channel not found')

    @commands.command(name="status", aliases=["getstatus", "war"])
    async def current_war_status(self, ctx):
        """Returns the current war status"""
        clan_tag = self.service.dict.get(ctx.channel.id, 0)
        if clan_tag == 0:
            return await ctx.send("No clan linked to this channel")
        else:
            clan_tag = clan_tag[0]

        try:
            war: coc.ClanWar = await self.bot.coc.get_current_war(clan_tag)
        except coc.PrivateWarLog:
            return await ctx.send("Clan has a private war log!")
        if war is None:
            return await ctx.send("Clan is in a strange CWL state!")
        if war.state == "warEnded":
            embed = discord.Embed(colour=utility.status_colors.get(war.status))
        else:
            embed = discord.Embed(colour=utility.status_colors.get(war.state))
        embed.add_field(name="War State:", value=war.state + ': ' + war.status, inline=False)

        if war.end_time:  # if state is notInWar we will get errors

            hours, remainder = divmod(int(war.end_time.seconds_until), 3600)
            minutes, seconds = divmod(remainder, 60)
            embed.add_field(name=war.clan.name, value=war.clan.tag)
            embed.add_field(name="Opponent:", value=f"{war.opponent.name}\n" f"{war.opponent.tag}",
                            inline=False)
            embed.add_field(name="War End Time:", value=f"{hours} hours {minutes} minutes {seconds} seconds",
                            inline=False)
            embed.add_field(name="Score",
                            value=f"{str(war.clan.stars)} ({str(war.clan.destruction)}%) - {str(war.opponent.stars)} ({str(war.opponent.destruction)}%)",
                            inline=False)
            embed.add_field(name='War type', value=war.type)
            embed.add_field(name='War size', value=str(war.team_size))
            embed.add_field(name='Attacks per member', value=str(war.attacks_per_member))
        return await ctx.send(embed=embed)

    @commands.command(name="attacks", aliases=["war_lineup", "warlineup", "goa", "getourattacks", "att"])
    async def attacks(self, ctx):
        """Returns the lineup of the current war"""
        clan_tag = self.service.dict.get(ctx.channel.id, 0)
        if clan_tag == 0:
            await ctx.send("No clan linked to this channel")
            return
        else:
            clan_tag = clan_tag[0]
        try:
            war = await self.bot.coc.get_current_war(clan_tag)
        except coc.PrivateWarLog:
            return await ctx.send("Clan is not in war or has a private war log!")

        if war is None or war.state == "notInWar":
            return await ctx.send("Clan is not in war")

        members = self.service.get_clanmates(war.members)
        pages = []
        if not war.attacks:
            while members:
                embed = self.service.getEmbedLineup(members[:10])
                del members[:10]
                embed.title = war.clan.name
                pages.append(Page(embed=embed))
        else:
            while members:
                embed = self.service.getEmbedAttacks(members[:10])
                del members[:10]
                embed.title = war.clan.name
                pages.append(Page(embed=embed))
        if pages:
            await self.paginator.send(ctx.channel, pages, type=utility.PAGINATOR_TYPE, author=ctx.author,
                                      disable_on_timeout=False)
        else:
            await ctx.send("Nothing to show")

    @commands.command(name="defenses", aliases=["gd", "getdefenses", "get_defenses", "def"])
    async def defenses(self, ctx):
        """Returns enemy attacks in the current war"""
        clan_tag = self.service.dict.get(ctx.channel.id, 0)
        if clan_tag == 0:
            await ctx.send("No clan linked to this channel")
            return
        else:
            clan_tag = clan_tag[0]
        try:
            war = await self.bot.coc.get_current_war(clan_tag)
        except coc.PrivateWarLog:
            return await ctx.send("Clan is not in war or has a private war log!")

        if war is None or war.state == "notInWar":
            return await ctx.send("Clan is not in war")

        members = self.service.get_opponentes(war.members)
        pages = []
        if not war.attacks:
            while members:
                embed = self.service.getEmbedLineup(members[:10])
                del members[:10]
                embed.title = war.opponent.name
                pages.append(Page(embed=embed))
        else:
            while members:
                embed = self.service.getEmbedAttacks(members[:10])
                del members[:10]
                embed.title = war.opponent.name
                pages.append(Page(embed=embed))
        if pages:
            await self.paginator.send(ctx.channel, pages, type=utility.PAGINATOR_TYPE, author=ctx.author,
                                      disable_on_timeout=False)
        else:
            await ctx.send("Nothing to show")

    @commands.command(name="last_wars", aliases=["getwars", "get_wars", "last", "lw"])
    async def last_wars(self, ctx, number=5):
        """Returns last n friendly wars.
         By default it returns last 5 wars, but you can add the number of wars you would like to see, for a max of 10.
         It only returns friendly war 5v5 1hit"""
        clan_tag = self.service.dict.get(ctx.channel.id, 0)
        if clan_tag == 0:
            await ctx.send("No clan linked to this channel")
            return
        else:
            clan_tag = clan_tag[0]
        if number > 10:
            await ctx.send('Maximum war retrievable is 10. Showing last 10 wars.')
        try:
            warlog: coc.ClanWarLogEntry = await self.bot.coc.get_warlog(clan_tag)
            warlog = [war for war in warlog if war.team_size == 5 and war.attacks_per_member == 1]
        except coc.PrivateWarLog:
            return await ctx.send("Clan is not in war or has a private war log!")
        if len(warlog):
            for war in warlog[:number]:
                if war.is_league_entry:
                    pass
                else:
                    embed = self.service.getWarLogEmbed(war)
                    await ctx.send(embed=embed)
        else:
            await ctx.send('No 5v5 1hit wars to show')

    @commands.command(name="war_log", aliases=["warlog", "pageslog", "pages", "log", "wlog"])
    async def war_log(self, ctx):
        """Returns clan war log.
         It only contains friedly war 5v5 1hit"""
        clan_tag = self.service.dict.get(ctx.channel.id, 0)
        if clan_tag == 0:
            await ctx.send("No clan linked to this channel")
            return
        else:
            clan_tag = clan_tag[0]
        try:
            warlog: coc.ClanWarLogEntry = await self.bot.coc.get_warlog(clan_tag)
            warlog = [war for war in warlog if war.team_size == 5 and war.attacks_per_member == 1]
        except coc.PrivateWarLog:
            return await ctx.send("Clan is not in war or has a private war log!")
        if len(warlog):
            pages = []
            for war in warlog:
                if war.is_league_entry:
                    pass
                else:
                    embed = self.service.getWarLogEmbed(war)
                    pages.append(Page(embed=embed))
            if pages:
                await self.paginator.send(ctx.channel, pages, type=utility.PAGINATOR_TYPE, author=ctx.author,
                                          disable_on_timeout=False)
        else:
            await ctx.send('No 5v5 1hit wars to show')

    @commands.command(name="current_wars", aliases=["currentwars", "wars", "cw"])
    async def current_wars(self, ctx):
        """Returns all current wars from linked clans"""
        msg = await ctx.send('Retrieving data...')
        pages = []
        for clan_tag in set(self.service.getClans()):
            try:
                war: coc.ClanWar = await self.bot.coc.get_current_war(clan_tag)
                if war.state == "inWar":
                    embed = discord.Embed(colour=utility.war_colors.get(war.type))
                    embed.set_author(name=war.clan.name)
                    embed.description = war.clan.tag
                    embed.add_field(name=war.opponent.name, value=f"{war.opponent.tag}",
                                    inline=False)
                    embed.add_field(name="Score",
                                    value=f"{str(war.clan.stars)} ({str(war.clan.destruction)}%) - {str(war.opponent.stars)} ({str(war.opponent.destruction)}%)",
                                    inline=False)
                    embed.set_thumbnail(url=war.clan.badge.url)
                    hours, remainder = divmod(int(war.end_time.seconds_until), 3600)
                    minutes, seconds = divmod(remainder, 60)
                    embed.set_footer(text=f"Ends in {hours} hours {minutes} minutes {seconds} seconds")
                    pages.append(Page(embed=embed))
            except coc.PrivateWarLog:
                pass
            except:
                pass
        await msg.delete()
        if pages:
            await self.paginator.send(ctx.channel, pages, type=utility.PAGINATOR_TYPE, author=ctx.author,
                                      disable_on_timeout=False)
        else:
            await ctx.send("No linked clans are currently in war!")

    @commands.command(name="clans_in_war", aliases=["clansinwar", "ciw", "inwar"])
    async def clans_in_war(self, ctx):
        """Returns all clans (linked) that currently are in a war"""
        wars = {}
        msg = await ctx.send('Retrieving data...')
        for clan_tag in set(self.service.getClans()):
            try:
                war: coc.ClanWar = await self.bot.coc.get_current_war(clan_tag)
                if war.state == "inWar":
                    hours, remainder = divmod(int(war.end_time.seconds_until), 3600)
                    minutes, seconds = divmod(remainder, 60)
                    wars[war.clan.name] = f"Ends in {hours} hours {minutes} minutes {seconds} seconds"
            except coc.PrivateWarLog:
                pass
            except:
                pass

        keys = list(wars.keys())
        pages = []
        while keys:
            embed = discord.Embed(title='Clans currently in a war', colour=discord.Color.dark_blue())
            for key in keys[:25]:
                embed.add_field(name=key, value=wars.get(key))
            del keys[:25]

            pages.append(Page(embed=embed))
        await msg.delete()
        if pages:
            await self.paginator.send(ctx.channel, pages, type=utility.PAGINATOR_TYPE, author=ctx.author,
                                      disable_on_timeout=False)
        else:
            await ctx.send("No linked clans are currently in war!")

    @commands.command(name="stats", aliases=["getstats", "score"])
    async def stats(self, ctx):
        """Returns the current or last war stats"""
        clan_tag = self.service.dict.get(ctx.channel.id, 0)
        if clan_tag == 0:
            return await ctx.send("No clan linked to this channel")
        else:
            clan_tag = clan_tag[0]

        try:
            war: coc.ClanWar = await self.bot.coc.get_current_war(clan_tag)
        except coc.PrivateWarLog:
            return await ctx.send("Clan has a private war log!")
        if war is None:
            return await ctx.send("Clan is in a strange CWL state!")
        if war.attacks_per_member != 1:
            await ctx.send("This command is currently supported only for 1 hit wars.")
            return await ctx.send("Try run `lb attacks` and `lb defenses` ")
        if war.state == "warEnded":
            embed = discord.Embed(colour=utility.status_colors.get(war.status))
        else:
            embed = discord.Embed(colour=utility.status_colors.get(war.state))

        embed.add_field(name="War State:", value=war.state + ': ' + war.status, inline=False)

        if war.end_time:  # if state is notInWar we will get errors

            hours, remainder = divmod(int(war.end_time.seconds_until), 3600)
            minutes, seconds = divmod(remainder, 60)
            embed.add_field(name=war.clan.name,
                            value=self.service.getStatsAttacks(self.service.get_clanmates(war.members)), inline=True)
            embed.add_field(name=war.opponent.name,
                            value=self.service.getStatsAttacks(self.service.get_opponentes(war.members)))
            embed.add_field(name="Score",
                            value=f"{str(war.clan.stars)} ({str(war.clan.destruction)}%) - {str(war.opponent.stars)} ({str(war.opponent.destruction)}%)",
                            inline=False)
            embed.set_footer(text=f"Ends in {hours} hours {minutes} minutes {seconds} seconds")
        return await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(WarManager(bot))
