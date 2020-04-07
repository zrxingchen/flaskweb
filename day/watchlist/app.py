import os,sys

from flask import Flask,url_for,render_template,request,flash,redirect
from flask_sqlalchemy import SQLAlchemy
import click
from werkzeug.security import generate_password_hash,check_password_hash

WIN = sys.platform.startswith('win')
if WIN:
    prefix = "sqlite:///"
else:
    prefix = "sqlite:////"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '1903_dev'

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
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        # 获取表单得数据
        title = request.form.get('title')
        year = request.form.get('year')
        #  验证数据  year长度不能超过4 title 长度不能超过60
        if not title or not year or len(year)>4 or  len(title)>60:
            flash('输入错误')
            return redirect(url_for('index'))
        # 将数据保存到数据库
        movie = Movie(title=title,year=year)   # 创建记录
        db.session.add(movie)
        db.session.commit()
        flash('创建成功')
        return redirect(url_for('index'))

    movies = Movie.query.all()  # 读取所有得电影记录
    return render_template('index.html',movies=movies)




# 编辑视图函数
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('输入错误')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('修改成功')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


# 编辑删除视图函数
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


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




# 错误处理函数
@app.errorhandler(404)
def page_not_found(e):
    
    return render_template('404.html')





# 模板上下文处理函数
@app.context_processor
def common_user():
    user = User.query.first()
    return dict(user=user)



 