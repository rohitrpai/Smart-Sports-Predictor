from abc import ABC, abstractmethod

import MySQLdb
from flask import app
from flask_mysqldb import MySQL


class DatabaseBase(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def setup_cursor(self):
        pass

    @abstractmethod
    def setup_sql_instance(self):
        pass


class MySqlDatabase(DatabaseBase):
    def __init__(self):
        super().__init__()

    def connect(self):
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = 'Smart@1010'
        app.config['MYSQL_DB'] = 'predictor'

        print("Successfully connected to MySQL database!")

    def setup_sql_instance(self):
        mysql = MySQL(app)
        return mysql

    def setup_cursor(self):
        mysql = MySQL(app)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        return cursor

    def get(self):
        return "success"
