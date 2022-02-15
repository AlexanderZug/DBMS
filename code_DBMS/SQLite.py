import sqlite3

from abstract_strategy import DBWorker
from decorators import sql_error_handler
from code_DBMS.logger_config import logger


class SQLite(DBWorker):
    """
    The class working with local database using SQLite
    """

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
    @sql_error_handler
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

    # Getter and Setter are used to establish a connection from the database and the cursor if the user
    # changes database or selects it for the first time.
    @property
    def con(self):
        return self.__con

    @con.setter
    def con(self, user_db: str):
        self.__con = sqlite3.connect(user_db)
        self.__cur = self.__con.cursor()
