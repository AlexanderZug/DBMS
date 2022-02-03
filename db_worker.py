import sqlite3
from decorator import sql_error_handler, select_error


class DBWorker:
    def __init__(self):
        self.__con = sqlite3.connect('')
        self.__cur = self.__con.cursor()

    def get_all_tables(self):
        self.__cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
        return self.__cur.fetchall()

    def get_tables_header(self, table: str):
        self.__cur.execute("PRAGMA table_info('%s');" % table)
        return self.__cur.fetchall()

    @property
    def con(self):
        return self.__con

    @con.setter
    def con(self, user_db: str):
        self.__con = sqlite3.connect(user_db)
        self.__cur = self.__con.cursor()

    @sql_error_handler
    def get_sql_requests(self, query: str):
        self.__cur.execute("""%s""" % query)
        self.__con.commit()

    @select_error
    def get_sql_select_requests(self, select_request: str):
        self.__cur.execute("""%s""" % select_request)
        return self.__cur.fetchall()

    def send_table_content_to_user(self, table: str):
        try:
            self.__cur.execute("""SELECT * FROM '%s'""" % table)
        except Exception:
            return []
        else:
            return self.__cur.fetchall()
