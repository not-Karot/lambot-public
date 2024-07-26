import mysql.connector
from mysql.connector import MySQLConnection
from database.model.Player import Player
from database.model.WarReporter import WarReporter
from database.model.Attack import Attack
from database.model.Upgrade import Upgrade
from database.model.Comm_League import Comm_League
from database.model.Master_Roster import Master_Roster

import creds


class BotDatabase:
    def __init__(self):
        self.player = Player(self.auth)
        self.war_reporter = WarReporter(self.auth)
        self.attack = Attack(self.auth)
        self.upgrade = Upgrade(self.auth)
        self.comm_league = Comm_League(self.auth)
        self.master_roster = Master_Roster(self.auth)

    @property
    def auth(self):
        return {'user': creds.db_user,
                'password': creds.db_password,
                'host': creds.db_host,
                'database': creds.db_name}

    @property
    def connection(self):
        return MySQLConnection(**self.auth)
