import sqlite3

from code_DBMS.abstract_method import DBWorker
from code_DBMS.decorator import sql_error_handler, select_error
from loguru import logger
logger.add('logs/debug.log', level='DEBUG', format='{time} {level} {message}', rotation='300 MB', compression='zip')


class SQLite(DBWorker):
    def __init__(self):
        self.__con = sqlite3.connect('')
        self.__cur = self.__con.cursor()

    @logger.catch
    def get_all_tables(self):
        self.__cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
        return self.__cur.fetchall()

    @logger.catch
    def get_tables_header(self, table: str):
        self.__cur.execute("PRAGMA table_info('%s');" % table)
        return self.__cur.fetchall()

    @logger.catch
    @sql_error_handler
    def get_sql_requests(self, query: str):
        self.__cur.execute("""%s""" % query)
        self.__con.commit()

    @logger.catch
    @select_error
    def get_sql_select_requests(self, select_request: str):
        self.__cur.execute("""%s""" % select_request)
        return self.__cur.fetchall()

    @logger.catch
    def send_table_content_to_user(self, table: str):
        try:
            self.__cur.execute("""SELECT * FROM '%s'""" % table)
        except sqlite3.OperationalError:
            return []
        else:
            return self.__cur.fetchall()

    @property
    def con(self):
        return self.__con

    @con.setter
    def con(self, user_db: str):
        self.__con = sqlite3.connect(user_db)
        self.__cur = self.__con.cursor()