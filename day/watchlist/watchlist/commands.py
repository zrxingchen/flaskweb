from watchlist import db,app
import click
from watchlist.models import User,Movie



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
