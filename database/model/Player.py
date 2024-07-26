import mysql.connector
from mysql.connector import MySQLConnection


class Player:

    def __init__(self, auth):
        self.auth=auth

    @property
    def connection(self):
        return MySQLConnection(**self.auth)

    def register_user(self, tuple_data):
        """Method is used to register a user by taking a tuple of data to commit"""
        if len(tuple_data)<5:
            l= list(tuple_data)
            l.append(tuple_data[3])
            tuple_data= tuple(l)

        sql = "INSERT INTO coc_player (coc_tag, coc_name, coc_th, discord_id, runner) VALUES (%s,%s,%s,%s,%s)"
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

    def update_player(self, tuple_data):
        """Method updates the account of the registered users"""
        sql = "UPDATE coc_player SET coc_th= %s, coc_name=%s where coc_tag=%s"
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

    def get_players(self):
        """Method gets all the registered users"""
        sql = "SELECT  coc_name, coc_tag, coc_th, discord_id FROM coc_player ORDER BY discord_id, coc_th desc"
        conn = self.connection
        cur = conn.cursor()
        row=[]
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

    def get_accounts_by_id(self, discord_id):
        """Gets all accounts linked to a discord user"""

        sql = "SELECT coc_name, coc_tag, coc_th FROM coc_player WHERE discord_id = %s ORDER BY coc_th DESC"
        conn = self.connection
        cur = conn.cursor()
        try:
            cur.execute(sql, (discord_id,))
            row = cur.fetchall()
            conn.close()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)

        return row

    def delete_player(self, coc_tag):
        sql = "DELETE FROM coc_player WHERE coc_tag=%s"
        try:
            conn = self.connection
            conn.cursor().execute(sql, (coc_tag,))
            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
