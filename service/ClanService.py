import discord, utility


class ClanService:
    def __init__(self, bot):
        self.bot = bot

    def getLeagueInfos(self):
        return self.bot.dbconn.comm_league.get_leagues_infos()

    def getLeagueId(self, league):
        return self.bot.dbconn.comm_league.get_id((league[0], league[2], league[1]))[0]

    def addMasterRoster(self, clan, players, league):

        to_add = []

        for player in players:
            to_add.append((player, clan, self.getLeagueId(league)))
        return self.bot.dbconn.master_roster.add_players(to_add)

    def removeFromMasterRoster(self, clan, players, league):

        to_delete = []

        for player in players:
            to_delete.append((player, clan, self.getLeagueId(league)))
        return self.bot.dbconn.master_roster.remove_players(to_delete)

    def getMasterRoster(self, clan, league=None):
        if league:
            result = self.bot.dbconn.master_roster.getMasterRosterPerLeague(clan, self.getLeagueId(league))
        else:
            result = self.bot.dbconn.master_roster.getMasterRoster(clan)
        formatter = "`{0} {1} {2} {3}`"
        formatted = []
        for player in result:
            formatted.append(formatter.format(player[0], player[1], player[2], player[3]))
        return formatted
