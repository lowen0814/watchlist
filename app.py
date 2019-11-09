#coding=utf-8
from flask import Flask,render_template
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
import os
import click
from flask import request,url_for,redirect,flash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'
db = SQLAlchemy(app)
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
        #获取表单
        title = request.form.get('title') #传入表单对应输入字段的name值
        year = request.form.get('year')
        #验证数据
        if not title or not year or len(year) > 4 or len(title) > 15:
            flash('invalid input') #显示错误提示
            return redirect(url_for('db_index')) #重定向回首页
        #保存表单数据到数据库
        file = FilesList(title=title, year=year) #创建记录
        db.session.add(file)
        db.session.commit()
        flash('item created')
        return redirect(url_for('new_index'))
    user = User.query.first()
    files = FilesList.query.all()
    return render_template('index_new.html',user=user,files=files)

@app.route('/files/edit/<int:file_id>', methods=['GET','POST'])
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



#创建数据库模型
class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


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
