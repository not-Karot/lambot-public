import mysql.connector
from mysql.connector import MySQLConnection


class Upgrade:

    def __init__(self, auth):
        self.auth = auth

    @property
    def connection(self):
        return MySQLConnection(**self.auth)

    def clear_updates(self):
        sql = "DELETE FROM upgrade"
        try:
            conn = self.connection
            conn.cursor().execute(sql)
            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)

    def register_update(self, tuple_data):
        sql = "INSERT INTO upgrade (coc_tag, previous_th, target_th) VALUES (%s,%s,%s)"
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

    def get_upgrades(self):
        """Method gets all the registered users"""
        sql = "SELECT  * FROM upgrade ORDER BY target_th, previous_th desc"
        conn = self.connection
        cur = conn.cursor()
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
