# -*- coding:utf-8 -*-


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 配置数据库信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/Flask_test01'
# 是否追踪数据库的修改，会极大的消耗数据库的性能,一般不开启追踪：Flase
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 创建链接数据库对象
db = SQLAlchemy(app)


class Role(db.Model):
    # 自定义表名为：roles
    __tablename__ = 'roles'

    """角色：1.一个角色可以有有多个用户"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    us = db.relationship('User', backref='role')


class User(db.Model):
    # 自定义表名为：users
    __tablename__ = 'users'

    """用户：多，一个角色可以有多个用户"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64))
    pswd = db.Column(db.String(64))
    # 指定外检约束：一对多，关系字段定义在多的哪一方
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User: %s-%s-%s-%s>' % (self.name, self.email, self.pswd, self.role_id)


@app.route('/index')
def index():
    return 'index'


if __name__ == '__main__':
    # 删除继承自db.Model的类映射的数据库的表
    db.drop_all()
    # 会把继承来自db.Model映射到数据库的表
    db.create_all()

    # 准备角色数据
    ro1 = Role(name='admin')
    db.session.add(ro1)
    db.session.commit()
    # 再次插入一条数据
    ro2 = Role(name='user')
    db.session.add(ro2)
    db.session.commit()

    us1 = User(name='wang', email='wang@163.com', pswd='123456', role_id=ro1.id)
    us2 = User(name='zhang', email='zhang@189.com', pswd='201512', role_id=ro2.id)
    us3 = User(name='chen', email='chen@126.com', pswd='987654', role_id=ro2.id)
    us4 = User(name='zhou', email='zhou@163.com', pswd='456789', role_id=ro1.id)
    db.session.add_all([us1, us2, us3, us4])
    db.session.commit()

    app.run(debug=True)
