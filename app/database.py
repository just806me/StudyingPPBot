from os import environ
import sqlite3
import threading


class Database:
    def __init__(self) -> None:
        self.thread_local = threading.local()
        self.__create_tables_if_not_exist__()

    def __create_tables_if_not_exist__(self) -> None:
        cursor = self.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS "users" (
                "id"          BIGINT      PRIMARY KEY,
                "name"        TEXT        NOT NULL,
                "username"    TEXT        NOT NULL,
                "deleted_at"  DATETIME
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS "problems" (
                "id"          BIGINT      PRIMARY KEY,
                "group"       BIGINT      NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS "submissions" (
                "id"          BIGINT      PRIMARY KEY,
                "user_id"     BIGINT      NOT NULL,
                "problem_id"  BIGINT      NOT NULL,
                "score"       TINYINT     NOT NULL,
                UNIQUE ("user_id", "problem_id") ON CONFLICT REPLACE
            )
        ''')
        self.commit()

    def __connection__(self) -> sqlite3.Connection:
        try:
            return self.thread_local.connection
        except AttributeError:
            self.thread_local.connection = sqlite3.connect(environ['DATABASE'])
            return self.thread_local.connection

    def cursor(self) -> sqlite3.Cursor:
        return self.__connection__().cursor()

    def commit(self) -> None:
        self.__connection__().commit()
