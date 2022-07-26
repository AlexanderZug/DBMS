from abc import ABC, abstractmethod
from typing import Union


class DBWorker(ABC):
    @abstractmethod
    def get_all_tables(self):
        pass

    @abstractmethod
    def get_tables_header(self, table: str):
        pass

    @abstractmethod
    def get_sql_requests(self, query: str):
        pass

    @abstractmethod
    def get_sql_select_requests(self, select_request: str):
        pass

    @abstractmethod
    def send_table_content_to_user(self, table: str):
        pass

    @abstractmethod
    def con(self):
        pass

    @abstractmethod
    def con(self, user_data: Union[tuple, str]):
        pass
