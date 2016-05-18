from flask import Flask
from flask import abort
from flask import redirect

app = Flask(__name__)

@app.route('/')
def index():
	return '<h1>Hello World!</h1>'

#使用app.route修饰器，把修饰的函数注册为路由
#修饰器可以使用不同的方式修改函数的行为，惯常用法是使用修饰器把函数注册为事件的处理程序
@app.route('/user/<name>')
def sayHello(name):
	if name == 'baidu':
		return redirect('http://www.baidu.com')
	elif name == 'No':
		return abort(404)
	return '<h1>Hello,%s</h1>'%name

if __name__ == '__main__':
	app.run(debug=True)
