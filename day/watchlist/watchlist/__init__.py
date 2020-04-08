import os,sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
WIN = sys.platform.startswith('win')

if WIN:
    prefix = "sqlite:///"
else:
    prefix = "sqlite:////"

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path),'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '1903_dev'


db = SQLAlchemy(app)

login_manager = LoginManager(app) #实例化拓展类
@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user

login_manager.login_view = 'login'
login_manager.login_message = '未登录'



# 模板上下文处理函数
@app.context_processor
def common_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)


from watchlist import views, errors ,commands