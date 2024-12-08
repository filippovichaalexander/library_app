from providers.raw_sql_provider import RawSqlProvider
from providers.sqlalchemy_provider import SqlAlchemyProvider

from ui_logic.console_ui import ConsoleDbApp


def main():
    # print('starting console app')
    # RawSqlProvider.create_database_if_not_exists()
    # RawSqlProvider.create_tables_if_not_exists()
    #
    # author_name = input('Please enter author name:')
    # author_id = RawSqlProvider.add_author(author_name)
    # print(f'author {author_name} created with id: {author_id}')
    #
    # title, publication_year, author_id = input('Please enter title, publication_year, author_id:').split(',')
    # book_id = RawSqlProvider.add_book(title, publication_year, author_id)
    # print(f'Book {title} created with id: {book_id}')
    #
    # genre_name = input('Please enter book genre:')
    # genre_id = RawSqlProvider.add_genre(genre_name)
    # print(f'Genre {genre_name} was created with id: {genre_id}')
    #
    # book_id, genre_id = input('Please enter book_id, genre_id:').split(',')
    # created_book_id, created_genre_id = RawSqlProvider.add_book_genre(book_id, genre_id)
    # print(f'Book id with {created_book_id} was added to genre id: {created_genre_id}')
    #
    # genre_name = input('Please enter book genre:')
    # RawSqlProvider.get_books_by_genre(genre_name)
    #
    # author_name = input('Please enter book author:')
    # RawSqlProvider.get_books_by_author_and_year(author_name)
    #
    # RawSqlProvider.get_genre_count()


    app = ConsoleDbApp(RawSqlProvider, SqlAlchemyProvider)
    app.start_app()


if __name__ == '__main__':
    main()