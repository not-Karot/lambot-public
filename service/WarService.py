from typing import Dict, Any
import utility
import discord


class WarService:
    dict: Dict[int, list]

    def __init__(self, bot):
        self.bot = bot
        self.dict = self.getDict()

    def getDict(self):

        result = self.bot.dbconn.war_reporter.get_war_reporter()
        dictionary = {}
        for item in result:
            dictionary[item[0]] = [item[1], item[2]]

        return dictionary

    def getClans(self):
        lista = list(self.dict.values())

        clans = []
        for item in lista:
            clans.append(item[0])
        return clans

    def addElement(self, channel, clan_tag):
        if channel in self.dict.keys():
            self.bot.dbconn.war_reporter.update_war_reporter((clan_tag, channel))

        else:
            self.bot.dbconn.war_reporter.add_war_reporter((channel, clan_tag))

        self.dict[channel] = [clan_tag, 1]

    def updatePostHits(self, channel, arg):
        self.bot.dbconn.war_reporter.update_post_hits((arg, channel))
        self.dict[channel][1] = arg

    def getFirstChannelIDByTag(self, clan_tag):
        for channel, value in self.dict.items():
            if value[0] == clan_tag:
                return channel
        return -1

    def getAllChannelsIDByTagPostTrue(self, clan_tag):
        channels = []
        for channel, value in self.dict.items():
            if value[0] == clan_tag and value[1]:
                channels.append(channel)
        return channels

    def deleteElement(self, channel):
        self.bot.dbconn.war_reporter.deleteElement(channel)
        del self.dict[channel]

    def setStars(self, stars):
        if stars == 3:
            result = utility.star3
        elif stars == 2:
            result = utility.star2
        elif stars == 1:
            result = utility.star1
        else:
            result = utility.star0
        return result

    def on_war_attack_embed(self, attack, war):

        formatter = '{0} {1} {2} {3} {4} {5} {6} {7}'
        stars = self.setStars(attack.stars)
        destruction = str(attack.destruction)

        if attack.attacker.is_opponent:
            if attack.stars == 3:
                color = discord.Color.dark_red()
            else:
                color = discord.Color.dark_green()
            action = utility.shield
            home_name = attack.defender.name
            home_no = str(attack.defender.map_position)
            home_th = utility.getTownHallimage(attack.defender.town_hall)
            away_th = utility.getTownHallimage(attack.attacker.town_hall)
            away_no = str(attack.attacker.map_position)
        else:
            if attack.stars == 3:
                color = discord.Color.green()
            else:
                color = discord.Color.red()
            action = utility.sword
            home_name = attack.attacker.name
            home_no = str(attack.attacker.map_position)
            home_th = utility.getTownHallimage(attack.attacker.town_hall)
            away_no = str(attack.defender.map_position)
            away_th = utility.getTownHallimage(attack.defender.town_hall)

        descrizione = formatter.format(home_no, home_th, action, away_no, away_th, stars, destruction, home_name)

        return discord.Embed(description=descrizione, color=color)

    def on_war_attack_string(self, attack, war):

        formatter = '{0} {1} {2} {3} {4} {5} {6} {7}'
        stars = self.setStars(attack.stars)
        destruction = str(attack.destruction)

        if attack.attacker.is_opponent:
            if attack.stars == 3:
                color = discord.Color.dark_red()
            else:
                color = discord.Color.dark_green()
            action = utility.shield
            home_name = attack.defender.name
            home_no = str(attack.defender.map_position)
            home_th = utility.getTownHallimage(attack.defender.town_hall)
            away_th = utility.getTownHallimage(attack.attacker.town_hall)
            away_no = str(attack.attacker.map_position)
        else:
            if attack.stars == 3:
                color = discord.Color.green()
            else:
                color = discord.Color.red()
            action = utility.sword
            home_name = attack.attacker.name
            home_no = str(attack.attacker.map_position)
            home_th = utility.getTownHallimage(attack.attacker.town_hall)
            away_no = str(attack.defender.map_position)
            away_th = utility.getTownHallimage(attack.defender.town_hall)

        descrizione = formatter.format(home_no, home_th, action, away_no, away_th, stars, destruction, home_name)

        return descrizione

    def getAttacks(self, attacks):

        attacchi = {
            "firstAttack": [],
            "secondAttack": []
        }

        for member_attack in attacks:
            # ogni member_attack ha una lunghezza massima di due attacchi
            if len(member_attack) == 2:
                secondAttack = ""
                secondAttack += utility.getTownHallimage(member_attack[1].defender.town_hall) + self.setStars(
                    member_attack[1].stars) + str(member_attack[1].destruction)
                attacchi.get("secondAttack").append(secondAttack)
            else:

                attacchi.get("secondAttack").append("")
            if len(member_attack) > 0:
                firstAttack = ""
                firstAttack += utility.getTownHallimage(member_attack[0].defender.town_hall) + self.setStars(
                    member_attack[0].stars) + str(member_attack[0].destruction)
                attacchi.get("firstAttack").append(firstAttack)

            else:

                attacchi.get("firstAttack").append(".")

        return attacchi

    def getEmbedLineup(self, members):
        new_line = "\n"
        embed = discord.Embed(color=discord.Color.random())
        ths = new_line.join(utility.getTownHallimage(member.town_hall) for member in members)
        name = new_line.join(member.name for member in members)
        nos = new_line.join(str(member.map_position) for member in members)
        embed.add_field(name="Th", value=ths, inline=True)
        embed.add_field(name="N°", value=nos, inline=True)
        embed.add_field(name="Name", value=name, inline=True)
        return embed

    def getEmbedAttacks(self, members):
        new_line = "\n"
        embed = discord.Embed(color=discord.Color.random())
        ths = new_line.join(utility.getTownHallimage(member.town_hall) for member in members)
        nos = new_line.join(str(member.map_position) for member in members)
        dictionary = self.getAttacks(list(member.attacks for member in members))

        att1 = new_line.join(item for item in dictionary.get("firstAttack"))
        att2 = new_line.join(item for item in dictionary.get("secondAttack"))
        name = new_line.join((utility.getTownHallimage(member.town_hall) + member.name)
                             for member in members)
        embed.add_field(name="Player", value=name, inline=True)
        if not att1.strip() == "":
            embed.add_field(name="1° att", value=att1, inline=True)
        if not att2.strip() == "":
            embed.add_field(name="2° att", value=att2, inline=True)

        return embed
    def getStatsAttacks(self, members):
        new_line = "\n"

        dictionary = self.getAttacks(list(member.attacks for member in members))

        att1 = new_line.join(item for item in dictionary.get("firstAttack"))

        return att1

    def getWarLogEmbed(self, war):

        if war.result == "win":
            color = discord.Color.green()
        elif war.result == "lose":
            color = discord.Color.red()
        else:
            color = discord.Color.dark_gold()
        embed = discord.Embed(
            title=f'{str(war.clan.stars)} ({str(war.clan.destruction)}%) - {str(war.opponent.stars)} ({str(war.opponent.destruction)}%)',
            color=color)
        embed.set_author(name=war.clan.name)
        embed.set_thumbnail(url=war.opponent.badge.url)
        embed.add_field(name=war.opponent.name, value=f"{war.opponent.tag}",
                        inline=False)
        embed.set_footer(text=f"End time (UTC): {war.end_time.time}")
        return embed

    def get_clanmates(self, members):
        clanmates = []
        for member in members:
            if not member.is_opponent:
                clanmates.append(member)
        return clanmates

    def get_opponentes(self, members):
        opponentes = []
        for member in members:
            if member.is_opponent:
                opponentes.append(member)
        return opponentes