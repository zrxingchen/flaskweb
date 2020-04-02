from flask import Flask,url_for,render_template
app = Flask(__name__)

@app.route('/')
def index():
    name = "Dom"
    movies = [
        {'title':"大赢家","year":"2020"},
        {'title':"主女","year":"2020"},
        {'title':"狗女","year":"2020"},
        {'title':"猫女","year":"2020"},
        {'title':"厕所","year":"2020"},
        {'title':"时间","year":"1333"},
        {'title':"三你那","year":"1666"},
        {'title':"帝霸","year":"1522"},
        {'title':"至尊","year":"1000"},
    ]

    return render_template('index.html',name=name,movies=movies)

    