#coding=utf-8
from flask import Flask,render_template
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
import os
import click
from flask import request,url_for,redirect,flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_required, current_user



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'
db = SQLAlchemy(app)

login_manager = LoginManager(app) #实例化扩展类
#login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id)) #用ID作为user模型的主键查询对应的用户
    return user


@app.route('/home')
def hello():
    return '<h1>Hello aliao </h1><img src="http://helloflask.com/totoro.gif">'
@app.route('/user/<name>')
def user_page(name):
    return 'hello %s visiter' % name + '<h1>look </h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='axw'))
    print(url_for('user_page', name='test'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))
    return 'Test page'

name = 'axw'
files = [
    {'title': 'member', 'year': 'service_customer'},
    {'title': 'home', 'year': 'gateway_hippo'},
    {'title': 'event', 'year': 'bannerservice'},
    {'title': 'pages', 'year': 'picasso'}
]

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.route('/list')
def index():
    return render_template('index.html', name=name, files=files)

@app.route('/')
def db_index():
    #user = User.query.first() #使用context_processor后不需要在函数中再定义
    files = FilesList.query.all()
    #return render_template('index.html',user=user,files=files)
    return render_template('index_new.html', files=files) #用新的index_new页面（套用模板base.html方式）

@app.route('/new', methods=['GET', 'POST'])
def new_index():
    if request.method == 'POST':
        #if not current_user.is_authenticated:
            #return redirect(url_for('new_index'))
        #获取表单
        title = request.form.get('title') #传入表单对应输入字段的name值
        year = request.form.get('year')
        #验证数据
        if not title or not year or len(year) > 4 or len(title) > 15:
            flash('invalid input') #显示错误提示
            return redirect(url_for('new_index')) #重定向回首页
        #保存表单数据到数据库
        file = FilesList(title=title, year=year) #创建记录
        db.session.add(file)
        db.session.commit()
        flash('item created')
        return redirect(url_for('new_index'))
    user = User.query.first()
    files = FilesList.query.all()
    return render_template('index_new.html',user=user,files=files)

@app.route('/settings', methods=['GET', 'POST'])
#@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input')
            return redirect(url_for('settings'))
        current_user.name = name

        db.session.commit()
        flash('settings update')
        return redirect(url_for('new_index'))
    return render_template('settings.html')


@app.route('/files/edit/<int:file_id>', methods=['GET','POST'])
#@login_required #登陆保护
def edit(file_id):
    file = FilesList.query.get_or_404(file_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 15:
            flash('invalid input')
            return redirect(url_for('edit', file_id=file_id))

        file.title = title
        file.year = year

        db.session.commit()
        flash('Item update')
        return redirect(url_for('new_index'))
    return render_template('edit.html',files=file)

@app.route('/files/delete/<int:file_id>', methods= ['POST'])
#@login_required #登陆保护
def delete(file_id):
    file = FilesList.query.get_or_404(file_id)
    db.session.delete(file)
    db.session.commit()
    flash('item deleted')
    return redirect(url_for('new_index'))

@app.errorhandler(404)
def page_not_found(e):
    #user = User.query.first()
    #return render_template('404.html',user=user),404
    return render_template('404.html'), 404

@app.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input')
            return redirect(url_for('login'))

        user = User.query.first()
        if username == user.username and user.validate_password(password):
            #login_user(user)
            current_user.name = username
            flash('login success')
            return redirect(url_for('new_index'))

        flash('Invalid username or password')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bye')
    return redirect(url_for('new_index'))


#创建数据库模型
class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20)) #用户名
    password_hash = db.Column(db.String(128)) #密码散列值
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash,password)



class FilesList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.cli.command() #命令
@click.option('--drop', is_flag=True, help='Create after drop.') #设置选项
def initdb(drop):
    '''Initialize the database'''
    if drop:
        db.drop_all()

    db.create_all()
    click.echo('Initialized database') #输出提示信息


@app.cli.command()
def forge():
    '''Generate fake data'''
    db.create_all()

    name = 'axw'
    files = [
        {'title':'test3','year':'3'},
        {'title': 'test4', 'year': '4'},
        {'title': 'test5', 'year': '5'},
        {'title': 'test6', 'year': '6'}
    ]

    user = User(name=name)
    db.session.add(user)

    for f in files:
        file = FilesList(title=f['title'],year=f['year'])
        db.session.add(file)

    db.session.commit()
    click.echo('Done!')

@app.cli.command()
@click.option('--username', prompt=True, help='the username used to login')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='the password used to login')
def admin(username, password):
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('updating user')
        user.username = username
        user.set_password(password)

    else:
        click.echo('creating user')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done!')
