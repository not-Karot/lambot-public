import discord, coc

class UpgradeService:
    def __init__(self, bot):
        self.bot = bot
    async def createUpgradeList(self, response):

        formatter = '```{0} {1}```'
        line = ""
        for item in response:

            player= await self.bot.coc.get_player(item[0])
            line += formatter.format(item[1], player.name)
        return line

    async def createUpgradesList(self, response, bot):

        embeds = []
        dictionary = {}
        for item in response:
            # Add target_th to dict if not exists
            if item[2] not in dictionary:
                dictionary[item[2]] = []

            dictionary[item[2]].append(item[:2])

        for item in dictionary.keys():
            descrizione = await self.createUpgradeList(dictionary.get(item))
            embed = discord.Embed(color=discord.Color.random(), description=descrizione, title=item)

            embeds.append(embed)

        return embeds