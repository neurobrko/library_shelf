from flask import abort, make_response
from config import db
from models import Book, book_schema, books_schema
from datetime import datetime


def list_all():
    books = Book.query.all()
    return books_schema.dump(books)


def insert_book(book):
    isbn = book.get("isbn")
    existing_book = Book.query.filter(Book.isbn == isbn).one_or_none()

    if existing_book is None:
        new_book = book_schema.load(book, session=db.session)
        db.session.add(new_book)
        db.session.commit()
        return book_schema.dump(new_book), 201
    else:
        existing_title = existing_book.title
        abort(
            406, f"Book with ISBN {isbn} already exists! It is named: {existing_title}."
        )


def list_by_title(title):
    books = Book.query.filter(Book.title == title)
    books_count = books.count()

    if books_count == 1:
        return books_schema.dump(books)[0]
    elif books_count > 1:
        return books_schema.dump(books)
    else:
        abort(404, f"There is no book on the shelf with title {title}.")


def list_by_isbn(isbn):
    book = Book.query.filter(Book.isbn == isbn).one_or_none()

    if book is not None:
        return book_schema.dump(book)
    else:
        abort(400, f"There si no book with ISBN {isbn}.")


def list_by_author(author):
    books = Book.query.filter(Book.author == author)
    books_count = books.count()

    if books_count == 1:
        return books_schema.dump(books)[0]
    elif books_count > 1:
        return books_schema.dump(books)
    else:
        abort(404, f"There is no book on the shelf by {author}.")


def update_book(isbn, book):
    existing_book = Book.query.filter(Book.isbn == isbn).one_or_none()

    if existing_book is not None:
        if "pub_date" in book.keys():
            book["pub_date"] = datetime.strptime(book["pub_date"], "%Y-%m-%d").date()
        db.session.query(Book).filter(Book.isbn == isbn).update(
            book, synchronize_session=False
        )
        db.session.commit()
    else:
        abort(404, f"There is no book with IDBN {isbn}.")


def delete_book(id):
    existing_book = Book.query.filter(Book.id == id).one_or_none()

    if existing_book is not None:
        existing_title = existing_book.title
        db.session.delete(existing_book)
        db.session.commit()
        return make_response(
            f"Book with title {existing_title} successfully deleted.", 200
        )
    else:
        abort(404, f"There is no book with ID {id}.")
