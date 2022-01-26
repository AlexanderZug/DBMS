import sqlite3


class DBWorker:
    def __init__(self):
        self.__con = sqlite3.connect('/Users/Polzovatel/PycharmProjects/subd/dist/concerts.db')
        self.__cur = self.__con.cursor()

    def user_query(self, query: str):
        result = self.__cur.execute(query).fetchall()
        self.__con.commit()
        if not result: result = None
        return result

    def get_all_tabels(self):
        self.__cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
        return self.__cur.fetchall()

    def tabels_header(self):
        self.__cur.execute("PRAGMA table_info(concerts);")
        return self.__cur.fetchall()

    def get_sql_requests(self, query: list):
        pass

    def tabel_content_to_user(self):
        self.__cur.execute("""SELECT * FROM concerts;""")
        return self.__cur.fetchall()


DBWorker().tabels_header()
# class SQLWorker:
#     pass
#
#
# class WindowWorker:
#     pass
