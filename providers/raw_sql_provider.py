import psycopg2

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from db_logic.raw_sql_queries import CREATE_TABLE_QUERIES, INSERT_AUTHOR, INSERT_GENRE, INSERT_BOOK, INSERT_BOOK_GENRE, \
    SELECT_BOOKS_BY_GENRE, SELECT_BOOKS_BY_AUTHOR_AND_YEAR, SELECT_GENRES_WITH_BOOK_COUNT
from providers.data_provider_interface import DataProvider

SERVER_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres'
DATABASE_URI = f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

class RawSqlProvider(DataProvider):
    connection = None

    @classmethod
    def connect(cls):
        if not cls.connection or cls.connection.closed:
            cls.connection = psycopg2.connect((DATABASE_URI))

        return cls.connection

    # creating DB
    @staticmethod
    def create_database_if_not_exists():
        conn = psycopg2.connect((SERVER_URI))
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"select 1 from pg_catalog.pg_database where datname = '{DB_NAME}'")
        if cur.fetchone() is None:
            print(f"creating DB {DB_NAME}")
            cur.execute(f"create database {DB_NAME}")
            print(f"DB {DB_NAME} created successfully")
        else:
            print(f"DB {DB_NAME} already exists")

        cur.close()
        conn.close()

    @staticmethod
    def create_tables_if_not_exists():
        with RawSqlProvider.connect() as conn:
            with conn.cursor() as cur:
                for q in CREATE_TABLE_QUERIES:
                    cur.execute(q)
                print('tables created succesfully')

    @staticmethod
    def add_author(name):
        with RawSqlProvider.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(INSERT_AUTHOR, (name,))
                return cur.fetchone()[0]

    @staticmethod
    def add_book(*args):
        title, publication_year, author_id = args
        with RawSqlProvider.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(INSERT_BOOK, (title, publication_year, author_id))
                return cur.fetchone()[0]

    @staticmethod
    def add_genre(genre_name):
        with RawSqlProvider.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(INSERT_GENRE, (genre_name,))
                return cur.fetchone()[0]

    @staticmethod
    def add_book_genre(book_id, genre_id):
        with RawSqlProvider.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(INSERT_BOOK_GENRE, (book_id, genre_id))
                return cur.fetchone()

    @staticmethod
    def get_books_by_genre(genre_name):
        with RawSqlProvider.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(SELECT_BOOKS_BY_GENRE, (f"%{genre_name}%",))
                books = cur.fetchall()
                return books

    @staticmethod
    def get_books_by_author_and_year(author_name):
        with RawSqlProvider.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(SELECT_BOOKS_BY_AUTHOR_AND_YEAR, (f"%{author_name}%",))
                books = cur.fetchall()
                return books

    @staticmethod
    def get_genre_count():
        with RawSqlProvider.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(SELECT_GENRES_WITH_BOOK_COUNT)
                results = cur.fetchall()
                return results