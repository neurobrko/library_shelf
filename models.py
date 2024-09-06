from config import db, ma


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    author = db.Column(db.String(64))
    isbn = db.Column(db.String(32), unique=True)
    pub_date = db.Column(db.DateTime)


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        load_instance = True
        sqla_session = db.session


book_schema = BookSchema()
books_schema = BookSchema(many=True)
