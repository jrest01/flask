from flask import Flask

app = Flask(__name__)


@app.route('/flask')
def hello():
    return "Hellow World from Flask"