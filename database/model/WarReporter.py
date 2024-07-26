import mysql.connector
from mysql.connector import MySQLConnection


class WarReporter:

    def __init__(self, auth):
        self.auth = auth

    @property
    def connection(self):
        return MySQLConnection(**self.auth)

    def get_war_reporter(self):
        sql = "SELECT * FROM war_reporter"
        conn = self.connection
        cur = conn.cursor()
        row = []
        try:
            cur.execute(sql)
            row = cur.fetchall()
            conn.close()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
        return row

    def add_war_reporter(self, tuple_data):
        sql = "INSERT INTO war_reporter (discord_channel,clan_tag) VALUES (%s, %s)"
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

    def update_post_hits(self, tuple_data):
        sql = "UPDATE war_reporter SET post_hits = %s where discord_channel= %s"
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
    def deleteElement(self, channel):
        sql= "DELETE FROM war_reporter WHERE discord_channel= %s"
        try:
            conn = self.connection
            conn.cursor().execute(sql, (channel,))
            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
    def update_war_reporter(self, tuple_data):
        sql = "UPDATE war_reporter SET clan_tag = %s where discord_channel=%s"
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
