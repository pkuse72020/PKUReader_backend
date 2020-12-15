# coding=UTF-8

from app import app, db
from app.ArticleSearch.searchengine import test

if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    # 测试端口修改为8000
    app.run(host='0.0.0.0', debug=True, port = 8000)