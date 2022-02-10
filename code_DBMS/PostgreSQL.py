import psycopg2
from psycopg2 import errors
from abstract_method import DBWorker
from decorators import sql_error_handler_postgres, postgres_init_massages
from config import host_name, user_name, password, db_name
from loguru import logger

logger.add('logs/debug.log', level='DEBUG', format='{time} {level} {message}', rotation='300 MB', compression='zip')


class DBPostgreSQL(DBWorker):
    @postgres_init_massages
    def __init__(self):
        self.__con = psycopg2.connect(database=db_name, user=user_name, password=password, host=host_name)
        self.__con.autocommit = True
        self.__cur = self.__con.cursor()

    @logger.catch
    def get_all_tables(self):
        self.__cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema='public'""")
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
