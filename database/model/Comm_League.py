import mysql.connector
from mysql.connector import MySQLConnection


class Comm_League:
    def __init__(self, auth):
        self.auth = auth

    @property
    def connection(self):
        return MySQLConnection(**self.auth)

    def add_league(self, tuple_data):
        """Method is used to create a league by taking a tuple of data to commit"""

        sql = "INSERT INTO comm_league (name, season, division, description) VALUES (%s,%s,%s,%s)"
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
            return False
        return True

    def get_leagues_infos(self):

        sql = "SELECT name, season, division from comm_league"
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
            return False

        return row

    def get_id(self, tuple_data):

        sql = "SELECT id from comm_league where name=%s and division=%s and season =%s"
        conn = self.connection
        cur = conn.cursor()
        row = []
        try:

            cur.execute(sql, tuple_data)
            row = cur.fetchone()
            conn.close()

        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            return False

        return row
