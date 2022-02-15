import psycopg2

from psycopg2 import errors
from abstract_strategy import DBWorker
from tkinter import messagebox as mbox
from decorators import sql_error_handler_postgres, postgres_init_massages
from code_DBMS.logger_config import logger


class PostgreSQL(DBWorker):
    """
    The class working with remote database using PostgreSQL
    """

    @postgres_init_massages
    def __init__(self):
        self.__con = psycopg2.connect(database=None, user=None, password=None, host=None)
        self.__con.autocommit = True
        self.__cur = self.__con.cursor()

    @logger.catch
    def get_all_tables(self):
        try:
            self.__cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema='public'""")
        except AttributeError:
            return []
        return self.__cur.fetchall()

    @logger.catch
    @sql_error_handler_postgres
    def get_tables_header(self, table: str):
        self.__cur.execute("""SELECT * FROM %s LIMIT 1""" % table)
        return self.__cur.description

    @logger.catch
    @sql_error_handler_postgres
    def get_sql_requests(self, query: str):
        self.__cur.execute("""%s""" % query)

    @logger.catch
    @sql_error_handler_postgres
    def get_sql_select_requests(self, select_request: str):
        self.__cur.execute("""%s""" % select_request)
        return self.__cur.fetchall()

    @logger.catch
    def send_table_content_to_user(self, table: str):
        try:
            self.__cur.execute("""SELECT * FROM %s""" % table)
        except psycopg2.errors.SyntaxError:
            return []
        else:
            return self.__cur.fetchall()

    @property
    def con(self):
        return self.__con

    @con.setter
    def con(self, user_data: tuple):
        try:
            self.__con = psycopg2.connect(database=user_data[3], user=user_data[0], password=user_data[1],
                                          host=user_data[2])
            self.__con.autocommit = True
            self.__cur = self.__con.cursor()
        except psycopg2.OperationalError as ex:
            mbox.showerror('', f'Произошла ошибка: {ex}')
