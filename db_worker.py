import sqlite3


class DBWorker:
    def __init__(self):
        self.__con = sqlite3.connect('dist/concerts.db')
        self.__cur = self.__con.cursor()

    def user_query(self, query: str):
        result = self.__cur.execute(query).fetchall()
        self.__con.commit()
        if not result: result = None
        return result

    def get_all_tabels(self):
        self.__cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
        return self.__cur.fetchall()

    def tabels_header(self, table: str):
        self.__cur.execute("PRAGMA table_info('%s');" % table)
        return self.__cur.fetchall()

    def get_sql_requests(self, query: list):
        pass

    def tabel_content_to_user(self, table: str):
        try:
            self.__cur.execute("""SELECT * FROM '%s'""" % table)
        except Exception:
            return []
        else:
            return self.__cur.fetchall()
