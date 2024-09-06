from flask import render_template
import config

from models import Book

app = config.connex_app
app.add_api(config.basedir / "books.yaml")


@app.route("/")
def home():
    books = Book.query.all()
    return render_template("home.html", books=books)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
