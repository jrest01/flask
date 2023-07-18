from flask import Flask



app = Flask(__name__)


@app.route('/flask')
def hello():
    return "Platzi, hellow from Flask"
