import psycopg2
from psycopg2 import errors
from code_DBMS.abstract_method import DBWorker
from code_DBMS.decorator import sql_error_handler_postgres, select_error_postgres, postgres_init_massages
from code_DBMS.config import host_name, user_name, password, db_name
from loguru import logger

logger.add('logs/debug.log', level='DEBUG', format='{time} {level} {message}', rotation='300 MB', compression='zip')


class DBPostgreSQL(DBWorker):
    @postgres_init_massages
    def __init__(self):
        self.con = psycopg2.connect(database=db_name, user=user_name, password=password, host=host_name,
                                    port="5432")
        self.con.autocommit = True
        self.cur = self.con.cursor()

    @logger.catch
    def get_all_tables(self):
        self.cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema='public'""")
        return self.cur.fetchall()

    @logger.catch
    def get_tables_header(self, table: str):
        try:
            self.cur.execute("""SELECT * FROM %s LIMIT 1""" % table)
        except psycopg2.errors.SyntaxError:
            return []
        return self.cur.description

    @logger.catch
    @sql_error_handler_postgres
    def get_sql_requests(self, query: str):
        self.cur.execute("""%s""" % query)

    @logger.catch
    @select_error_postgres
    def get_sql_select_requests(self, select_request: str):
        self.cur.execute("""%s""" % select_request)
        return self.cur.fetchall()

    @logger.catch
    def send_table_content_to_user(self, table: str):
        try:
            self.cur.execute("""SELECT * FROM %s""" % table)
        except psycopg2.errors.SyntaxError:
            return []
        else:
            return self.cur.fetchall()