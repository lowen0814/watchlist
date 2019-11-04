from flask import Flask,render_template
from flask import url_for
app = Flask(__name__)
@app.route('/home')
def hello():
    return '<h1>Hello aliao </h1><img src="http://helloflask.com/totoro.gif">'
@app.route('/user/<name>')
def user_page(name):
    return 'hello %s visiter' % name + '<h1>look </h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page',name='axw'))
    print(url_for('user_page',name='test'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for',num=2))
    return 'Test page'

name = 'axw'
movies = [
    {'title': '会员', 'year': 'service_customer'},
    {'title': '首页', 'year': 'gateway_hippo'},
    {'title': '场次', 'year': 'bannerservice'},
    {'title': '测试', 'year': 'test'}
]

@app.route('/list')
def index():
    return render_template('index.html', name=name, movies=movies)