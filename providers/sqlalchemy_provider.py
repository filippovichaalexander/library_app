from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import sessionmaker, Session

# from db_logic.models import Base, Author, Book, Genre, BookGenre
# from providers.data_provider_interface import DataProvider

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from providers.data_provider_interface import DataProvider
from db_logic.models import Base, Author, Genre, Book, BookGenre  # Ensure models are defined

# SERVER_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres'
# DATABASE_URI = f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

SERVER_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres'
DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


class SqlAlchemyProvider(DataProvider):
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = None

    @classmethod
    def connect(cls):
        if not cls.session:
            cls.session = cls.Session()
        return cls.session

    @staticmethod
    def create_database_if_not_exists():
        engine = create_engine(SERVER_URI, isolation_level="AUTOCOMMIT")
        conn = engine.connect()
        result = conn.execute(text(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'"))

        if not result.fetchone():
            print(f"Creating DB {DB_NAME}")
            conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
            print(f"DB {DB_NAME} created successfully")
        else:
            print(f"DB {DB_NAME} already exists")
        conn.close()

    @staticmethod
    def create_tables_if_not_exists():
        Base.metadata.create_all(SqlAlchemyProvider.engine)

    @staticmethod
    def add_author(name):
        session = SqlAlchemyProvider.connect()
        author = Author(author_name=name)
        session.add(author)
        session.commit()
        return author.author_id

    @staticmethod
    def add_book(title, publication_year, author_id):
        session = SqlAlchemyProvider.connect()
        book = Book(title=title, publication_year=publication_year, author_id=author_id)
        session.add(book)
        session.commit()
        return book.book_id

    @staticmethod
    def add_genre(genre_name):
        session = SqlAlchemyProvider.connect()
        genre = Genre(genre_name=genre_name)
        session.add(genre)
        session.commit()
        return genre.genre_id

    @staticmethod
    def add_book_genre(book_id, genre_id):
        session = SqlAlchemyProvider.connect()
        book_genre = BookGenre(book_id=book_id, genre_id=genre_id)
        session.add(book_genre)
        session.commit()
        return book_genre.book_id, book_genre.genre_id

    @staticmethod
    def get_books_by_genre(genre_name):
        session = SqlAlchemyProvider.connect()
        books = session.query(Book).join(BookGenre).join(Genre).filter(Genre.genre_name.ilike(f"%{genre_name}%")).all()
        for book in books:
            print(f"Book Title: {book.title}")

    @staticmethod
    def get_books_by_author_and_year(author_name):
        session = SqlAlchemyProvider.connect()
        # Use an exact match to query books
        books = session.query(Book).join(Author).filter(Author.author_name == author_name).order_by(
            Book.publication_year).all()
        return [(book.title, book.publication_year) for book in books]

    @staticmethod
    def get_genre_count():
        session = SqlAlchemyProvider.connect()
        results = session.query(Genre.genre_name, func.count(BookGenre.book_id)).outerjoin(BookGenre).group_by(
            Genre.genre_name).all()
        return results