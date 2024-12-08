from abc import  ABC, abstractmethod

class DataProvider(ABC):
    connection = None

    @classmethod
    @abstractmethod
    def connect(cls):
        pass

    # creating DB
    @staticmethod
    @abstractmethod
    def create_database_if_not_exists():
        pass

    @staticmethod
    @abstractmethod
    def create_tables_if_not_exists():
        pass

    @staticmethod
    @abstractmethod
    def add_author(name):
        pass

    @staticmethod
    @abstractmethod
    def add_book(*args):
        pass

    @staticmethod
    def add_genre(genre_name):
        pass

    @staticmethod
    @abstractmethod
    def add_book_genre(book_id, genre_id):
        pass

    @staticmethod
    @abstractmethod
    def get_books_by_genre(genre_name):
        pass

    @staticmethod
    @abstractmethod
    def get_books_by_author_and_year(author_name):
        pass

    @staticmethod
    @abstractmethod
    def get_genre_count():
        pass