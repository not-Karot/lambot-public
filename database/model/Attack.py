import mysql.connector
from mysql.connector import MySQLConnection
from datetime import datetime


class Attack:
    discord_id: str
    name: str
    th: int
    stars: int
    is_fresh: bool
    destruction: int

    def __init__(self, auth=None, discord_id=None, name=None, th=None, stars=None, is_fresh=None, destruction=None):
        if auth:
            self.auth = auth
            return
        if discord_id:
            self.discord_id = discord_id
        if name:
            self.name = name
            self.th = th
            self.stars = stars
            self.is_fresh = is_fresh
            self.destruction = destruction

    @property
    def connection(self):
        return MySQLConnection(**self.auth)

    def register_attack(self, tuple_data):
        """Method is used to register a user by taking a tuple of data to commit"""
        sql = "INSERT INTO coc_attack (coc_player_tag, coc_war_clan, coc_player_th, stars, is_fresh, destruction) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            conn = self.connection
            conn.cursor().execute(sql, tuple_data)
            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)

    def getPlayerAttacks(self, discord_id):
        sql = ("SELECT p.coc_name, a.coc_player_th, a.stars, a.destruction, a.is_fresh"
               "                    FROM coc_attack A"
               "                        INNER JOIN coc_player P"
               "                          ON A.coc_player_tag= P.coc_tag"
               "                    	where p.discord_id= %s "
               "                    	order BY a.coc_player_th desc;")
        conn = self.connection
        cur = conn.cursor()
        response = []
        try:
            cur.execute(sql, (discord_id,))
            response = cur.fetchall()
            conn.close()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            return response
        result = []
        for row in response:
            result.append(Attack(auth=None, discord_id=None, name=row[0], th=row[1], stars=row[2], destruction=row[3],
                                 is_fresh=row[4]))

        return result

    def getPlayerAttacksInClan(self, discord_id, clan):
        sql = ("SELECT p.coc_name, a.coc_player_th, a.stars, a.destruction, a.is_fresh"
               "                    FROM coc_attack A"
               "                        INNER JOIN coc_player P"
               "                          ON A.coc_player_tag= P.coc_tag"
               "                    	where p.discord_id= %s  and a.coc_war_clan= %s"
               "                    	order BY a.coc_player_th desc;")
        conn = self.connection
        cur = conn.cursor()
        response = []
        try:
            cur.execute(sql, (discord_id, clan,))
            response = cur.fetchall()
            conn.close()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            return response
        result = []
        for row in response:
            result.append(Attack(auth=None, discord_id=None, name=row[0], th=row[1], stars=row[2], destruction=row[3],
                                 is_fresh=row[4]))

        return result

    def getAttacksSortedByID(self):
        sql = ("SELECT p.discord_id, p.coc_name, a.coc_player_th, a.stars, a.destruction, a.is_fresh"
               "                    FROM coc_attack A"
               "                        INNER JOIN coc_player P"
               "                          ON A.coc_player_tag= P.`coc_tag`"
               "                    	order BY p.discord_id, a.coc_player_th desc;")
        conn = self.connection
        cur = conn.cursor()
        response = []
        try:
            cur.execute(sql)
            response = cur.fetchall()
            conn.close()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            return response
        result = []
        for row in response:
            result.append(Attack(auth=None, discord_id=row[0], name=row[1], th=row[2], stars=row[3], destruction=row[4],
                                 is_fresh=row[5]))

        return result

    def getAttacksSortedByIDFilteredByClan(self, clan_tag):
        sql = ("SELECT p.discord_id, p.coc_name, a.coc_player_th, a.stars, a.destruction, a.is_fresh"
               "                    FROM coc_attack A"
               "                        INNER JOIN coc_player P"
               "                          ON A.coc_player_tag= P.`coc_tag`"
               "                        WHERE A.coc_war_clan= %s"
               "                    	order BY p.discord_id, a.coc_player_th desc;")
        conn = self.connection
        cur = conn.cursor()
        response = []
        try:
            cur.execute(sql, (clan_tag,))
            response = cur.fetchall()
            conn.close()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            return response
        result = []
        for row in response:
            result.append(Attack(auth=None, discord_id=row[0], name=row[1], th=row[2], stars=row[3], destruction=row[4],
                                 is_fresh=row[5]))

        return result

    def getHitrate(self, clan):
        if clan:
            sql = (
                """SELECT coc_th ,coc_tag, coc_name,  discord_id, count(*) as total, sum(case when stars=3 then 1 else 0 end) as triple
                    from coc_attack A INNER JOIN coc_player P
                    ON A.coc_player_tag= P.coc_tag and a.coc_player_th=p.coc_th
                    where a.coc_war_clan = %s
                    group by coc_player_th, p.discord_id
                    order by coc_th desc, (sum(case when stars=3 then 1 else 0 end))/count(*) desc, count(*) desc""")
        else:
            sql = (
                """SELECT 	coc_th ,coc_tag, coc_name, discord_id, count(*) as total, sum(case when stars=3 then 1 else 0 end) as triple
                    from coc_attack A INNER JOIN coc_player P
                    ON A.coc_player_tag= P.coc_tag and a.coc_player_th=p.coc_th
                    group by coc_player_th, p.discord_id
                    order by coc_th desc, (sum(case when stars=3 then 1 else 0 end))/count(*) desc, count(*) desc;""")
        conn = self.connection
        cur = conn.cursor()
        response = []
        try:
            if clan:
                cur.execute(sql, (clan.tag,))
            else:
                cur.execute(sql)
            response = cur.fetchall()
            conn.close()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            return response

        return response

    def getBestLineup(self, clan, league_id):

        sql = (
            """SELECT coc_th ,coc_tag, coc_name,  discord_id, count(*) as total, sum(case when stars=3 then 1 else 0 end) as triple
                from coc_attack A INNER JOIN coc_player P
                ON A.coc_player_tag= P.coc_tag and a.coc_player_th=p.coc_th
                where coc_tag in (select player_tag from master_roster where clan_tag=%s and league_id=%s)
                group by coc_player_th, p.discord_id
                order by coc_th desc, (sum(case when stars=3 then 1 else 0 end))/count(*) desc, count(*) desc;""")

        conn = self.connection
        cur = conn.cursor()
        response = []
        try:
            if clan:
                cur.execute(sql, (clan.tag, league_id,))
            else:
                cur.execute(sql)
            response = cur.fetchall()
            conn.close()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            return response

        return response
