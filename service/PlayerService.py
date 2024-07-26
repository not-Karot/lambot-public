import discord, utility


class PlayerService:
    def createPlayerList(self, response):

        formatter = '```{0} {1} {2}```'
        line = ""
        for item in response:
            line += formatter.format(item[2], item[1], item[0])
        return line

    async def createPlayersList(self, response, bot):

        embeds = []
        dictionary = {}
        for item in response:
            # Add user to dict if not exists
            if item[3] not in dictionary:
                dictionary[item[3]] = []
            # Add all non-user attributes as a new list
            dictionary[item[3]].append(item[:3])

        for item in dictionary.keys():
            descrizione = self.createPlayerList(dictionary.get(item))

            user = await bot.fetch_user(int(item))
            embed = discord.Embed(color=discord.Color.random(), description=descrizione, title=user.name)
            embed.set_footer(text=f"Discord ID: {user.id}",
                             icon_url=user.avatar_url)
            embeds.append(embed)

        return embeds
