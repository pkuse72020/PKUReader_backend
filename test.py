# main.py
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'hello world'

def main():
    app.run(host='0.0.0.0',port=5001,debug=True)

if __name__ == '__main__':
    main()
