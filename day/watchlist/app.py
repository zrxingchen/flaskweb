from flask import Flask
app = Flask(__name__)

@app.route('/user/<name>')

def index(name):
    return "<h1>欢迎进入地狱 %s</h1>"%name