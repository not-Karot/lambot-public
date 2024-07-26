import discord, utility
from service.AttackService import AttackService
from service.ClanService import ClanService


class LineupService:
    def __init__(self, bot):
        self.bot = bot
        self.attackService = AttackService(bot)
        self.clanService = ClanService(bot)

    def createPlayerLine(self, response):

        formatter = '```{0} {1} {2}  {3}```'
        line = ""
        for item in response:
            hits = str(item[5]) + "/" + str(item[4])
            percentage = str(int(item[5] / item[4] * 100)) + " %"
            line += formatter.format(item[1], item[2], hits, percentage)
        return line

    def createHittersList(self, response):
        # response.item= [th, tag, name, discord, total, triple]

        embeds = []
        dictionary = {}

        for item in response:
            # Add target_th to dict if not exists
            if item[0] not in dictionary:
                dictionary[item[0]] = []

            dictionary[item[0]].append(item)

        for item in dictionary.keys():
            descrizione = self.createPlayerLine(dictionary.get(item))
            embed = discord.Embed(color=discord.Color.random(), description=descrizione, title=utility.getTownHallimage(
                item) + " " + utility.sword + " " + utility.getTownHallimage(item))

            embeds.append(embed)

        return embeds

    def createLineup(self, clan, ths, league):

        response = self.bot.dbconn.attack.getBestLineup(clan, self.clanService.getLeagueId(league))
        dictionary = {}

        for item in response:
            # Add target_th to dict if not exists
            if item[0] not in dictionary:
                dictionary[item[0]] = []

            dictionary[item[0]].append(item)

        # Variabile di appoggio per prendere il livello corretto dei vari th necessari
        temp = utility.getLastTownHallLevelInt() - len(ths)
        levels = []

        for item in utility.th_list[:temp:-1]:
            # cicla la lista dall'ultimo elemento in poi, con range dei th necessari
            # aggiunge i th necessari alla lista levels in ordine decrescente
            levels.append(int(item[2:4]))
        lineup = []
        # dictionary: {key:th_level, value: lista players con quel th}
        # levels: lista dei livelli dei th da mettere in war
        # ths: lista che contiene il numero di players da mettere per ogni th presente in levels
        # lineup: lineup finale

        for level in levels:
            if level not in dictionary:
                dictionary[level] = []
            temp = dictionary[level]
            index = levels.index(level)
            if len(temp) < ths[index]:
                raise ValueError
            lineup.extend(temp[0:ths[index]])

        return self.formatLineup(lineup)

    def formatLineup(self, lineup):
        formatter = "`{0} {1} {2}`"
        formatted = []
        for player in lineup:
            formatted.append(formatter.format(player[0], player[1], player[2]))
        return formatted
