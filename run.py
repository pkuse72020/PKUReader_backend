# coding=UTF-8

from app import app, db
from app.ArticleSearch.searchengine import test

if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    app.run(host='0.0.0.0', debug=True, port = 5000)
