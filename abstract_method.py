from abc import ABC, abstractmethod


class DBWorker(ABC):

    @abstractmethod
    def get_all_tables(self):
        pass

    @abstractmethod
    def get_tables_header(self):
        pass

    @abstractmethod
    def get_sql_requests(self):
        pass

    @abstractmethod
    def get_sql_select_requests(self):
        pass

    @abstractmethod
    def send_table_content_to_user(self):
        pass
