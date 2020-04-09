from watchlist import db,app
from flask_login import login_user,logout_user,login_required,current_user
from flask import Flask,url_for,render_template,request,flash,redirect
from watchlist.models import User,Movie


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

