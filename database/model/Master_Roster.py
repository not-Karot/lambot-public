import mysql.connector
from mysql.connector import MySQLConnection


class Master_Roster:
    def __init__(self, auth):
        self.auth = auth

    @property
    def connection(self):
        return MySQLConnection(**self.auth)

    def add_players(self, data_list):
        """Method is used to add multiple players to a master roster by taking a list of players to commit"""

        sql = "INSERT INTO master_roster (player_tag, clan_tag, league_id) VALUES (%s,%s,%s)"
        try:
            conn = self.connection
            conn.cursor().executemany(sql, data_list )
            conn.commit()
            conn.close()

        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            return False
        return True

    def remove_players(self, data_list):
        """Method is used to add multiple players to a master roster by taking a list of players to commit"""

        sql = "delete from master_roster where player_tag=%s AND clan_tag= %s and league_id=%s"

        try:
            conn = self.connection
            conn.cursor().executemany(sql, data_list)
            conn.commit()
            conn.close()

        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            return False
        return True

    def getMasterRoster(self, clan):
        sql = ("select distinct p.coc_th, p.coc_tag, p.coc_name, p.discord_id"
               "    from master_roster m inner join coc_player p"
               "        ON m.player_tag= P.coc_tag"
               "            where m.clan_tag= %s"
               "                order by p.coc_th desc;")

        try:
            conn = self.connection
            cur = conn.cursor()
            cur.execute(sql, (clan.tag,))

            response = cur.fetchall()
            conn.close()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            return False

        return response

    def getMasterRosterPerLeague(self, clan, league_id):
        sql = ("select distinct p.coc_th, p.coc_tag, p.coc_name, p.discord_id"
               "    from master_roster m inner join coc_player p"
               "        ON m.player_tag= P.coc_tag"
               "            where m.clan_tag= %s and m.league_id= %s"
               "                order by p.coc_th desc;")

        try:
            conn = self.connection
            cur = conn.cursor()
            cur.execute(sql, (clan.tag, league_id,))

            response = cur.fetchall()
            conn.close()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            return False

        return response
