import os,sys

from flask import Flask,url_for,render_template
from flask_sqlalchemy import SQLAlchemy
import click

WIN = sys.platform.startswith('win')
if WIN:
    prefix = "sqlite:///"
else:
    prefix = "sqlite:////"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# models  数据层
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
     id = db.Column(db.Integer,primary_key=True)
     title = db.Column(db.String(60))
     year = db.Column(db.String(4))






# views 视图函数
@app.route('/')
def index():
   
    user = User.query.first()
    movies = Movie.query.all()


    return render_template('index.html',user=user,movies=movies)

# 自定义命令
@app.cli.command()  # 注册命令
@click.option('--drop',is_flag=True,help='先删除在创建')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('初始化数据')


# 向空数据库插入数据
@app.cli.command()
def forge():
    name = "Dom"
    movies = [
        {'title':"大赢家","year":"2020"},
        {'title':"主2","year":"2020"},
        {'title':"12","year":"2020"},
        {'title':"猫3","year":"2020"},
        {'title':"99所","year":"2020"},
        {'title':"时间","year":"1333"},
        {'title':"三你那","year":"1666"},
        {'title':"帝霸","year":"1522"},
        {'title':"至尊","year":"1000"},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo("导入数据完成")



@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html',user=user)





