import os,sys

from flask import Flask,url_for,render_template,request,flash,redirect
from flask_sqlalchemy import SQLAlchemy
import click
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required,current_user



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

login_manager = LoginManager(app) #实例化拓展类
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

login_manager.login_view = 'login'
login_manager.login_message = '未登录'


# models  数据层

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
  
class Movie(db.Model):
     id = db.Column(db.Integer,primary_key=True)
     title = db.Column(db.String(60))
     year = db.Column(db.String(4))





# views 视图函数
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':

        if not current_user.is_authenticated:
            return redirect(url_for('index'))
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
@login_required
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
@login_required
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

# 生成管理员账户
@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('更新用户')
        user.username = username
        user.set_password(password)
    else:
        click.echo('创建用户')
        user = User(username=username, name='Dom')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('完成')

#登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('输入错误')
            return redirect(url_for('login'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('登录成功')
            return redirect(url_for('index'))

        flash('重新输入 username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')

# 登出
@app.route('/logout')
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))


# 设置
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('输入错误')
            return redirect(url_for('settings'))
        
        current_user.name = name
        
        db.session.commit()
        flash('设置name成功')
        return redirect(url_for('index'))

    return render_template('settings.html')


# 错误处理函数
@app.errorhandler(404)
def page_not_found(e):
    
    return render_template('404.html')





# 模板上下文处理函数
@app.context_processor
def common_user():
    user = User.query.first()
    return dict(user=user)



 