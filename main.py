from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SECRET_KEY']='2333' # 密码
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:A15446546ab@localhost:3306/test'
    # 协议：mysql+pymysql
    # 用户名：root
    # 密码：2333
    # IP地址：localhost
    # 端口：3306
    # 数据库名：runoob #这里的数据库需要提前建好
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db=SQLAlchemy(app)
app.debug=True

# 新建表Role
class Role(db.Model):
    __tablename__='roles' # 表名
    id=db.Column(db.Integer, primary_key=True) # id字段，int类型，主键
    name=db.Column(db.String(64), unique=True) # name字段，字符串类型，唯一
    users=db.relationship('User', backref='role', lazy='dynamic') # 外键关系，动态更新

    def __repr__(self): # 相当于toString
        return '<Role %r>' %self.name

# 新建表User
class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(64), unique=True, index=True) #索引
    role_id=db.Column(db.Integer, db.ForeignKey('roles.id')) # 外键

    def __repr__(self):
        return '<User %r>' %self.username

if __name__=='__main__':
    db.drop_all() # 删除存在表
    db.create_all() # 创建这两个表
    app.run()