import discord, utility


class AttackService:
    def __init__(self, bot):
        self.bot = bot

    def getPlayerStats(self, user, clan):
        if clan:
            response = self.bot.dbconn.attack.getPlayerAttacksInClan(user.id, clan.tag)
        else:
            response = self.bot.dbconn.attack.getPlayerAttacks(user.id)
        dictionary = {}
        for attack in response:
            # Add th to dict if not exists
            if attack.th not in dictionary:
                dictionary[attack.th] = []
            # Add all non-th attributes as a new list
            dictionary[attack.th].append(attack)
        stats = {}
        for key in dictionary.keys():
            counter = 0
            for item in dictionary.get(key):
                if item.stars == 3:
                    counter += 1
            stats[key] = [counter, len(dictionary.get(key))]
        embed = discord.Embed(title=user.name, color=discord.Color.random())
        for level in stats.keys():
            triples = stats.get(level)[0]
            all = stats.get(level)[1]
            percentuale = int(triples / all * 100)
            embed.add_field(
                name=utility.getTownHallimage(level) + " " + utility.sword + " " + utility.getTownHallimage(level),
                value="`" + str(triples) + "/" + str(all) + "\t " + str(percentuale) + "%" + "`", inline=False)
            if clan:
                embed.set_footer(text=f"Clan: {clan.name}")

        return embed

    def createStatsDict(self, response):
        dictionary = {}
        for attack in response:
            # Add th to dict if not exists
            if attack.discord_id not in dictionary:
                dictionary[attack.discord_id] = []
            # Add all non-th attributes as a new list
            dictionary[attack.discord_id].append(attack)

        for key in dictionary.keys():
            sub_dictionary = {}
            for attack in dictionary[key]:
                if attack.th not in sub_dictionary:
                    sub_dictionary[attack.th] = []
                # Add all non-th attributes as a new list
                sub_dictionary[attack.th].append(attack)
            dictionary[key] = sub_dictionary

        for key in dictionary.keys():
            stats = {}
            for sub_key in dictionary.get(key):
                counter = 0
                for item in dictionary.get(key).get(sub_key):
                    if item.stars == 3:
                        counter += 1

                stats[sub_key] = [counter, len(dictionary.get(key).get(sub_key))]
            dictionary[key] = stats
        return dictionary

    async def getPlayersStats(self, clan):
        if clan:
            response = self.bot.dbconn.attack.getAttacksSortedByIDFilteredByClan(clan.tag)
        else:
            response = self.bot.dbconn.attack.getAttacksSortedByID()
        dictionary = self.createStatsDict(response)
        embeds = []
        for key in dictionary.keys():
            user = await self.bot.fetch_user(int(key))
            embed = discord.Embed(title=user.name, color=discord.Color.random())

            for level in dictionary[key].keys():
                triples = dictionary[key].get(level)[0]
                all = dictionary[key].get(level)[1]
                percentuale = int(triples / all * 100)
                embed.add_field(
                    name=utility.getTownHallimage(level) + " " + utility.sword + " " + utility.getTownHallimage(level),
                    value="`" + str(triples) + "/" + str(all) + "\t " + str(percentuale) + "%" + "`", inline=False)
                if clan:
                    embed.set_footer(text=f"Clan: {clan.name}")
            embeds.append(embed)
        return embeds

    def getHitrate(self, clan, th):

        response = self.bot.dbconn.attack.getHitrate(clan)
        response = list(response)
        if th:

            temp = response
            response = []
            for line in temp:
                if line[0] == th:
                    response.append(line)

        return response
