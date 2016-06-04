#!/usr/bin/python3

from flask import Flask,render_template,session,url_for,flash,redirect
from flask.ext.wtf import Form
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager
from flask.ext.moment import Moment
from flask.ext.mongoengine import MongoEngine
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from datetime import datetime,timedelta


class NameForm(Form):
	name = StringField('your name?',validators=[Required()])
	passwd = StringField('your passwd?',validators=[Required()])
	submit = SubmitField('Submit')


#创建Flask对象app，Flask类的构造函数只有一个必须指定的参数，即程序主模块或包的名字.在大多数程序中，Python的__name__变量就是所需要的值
app = Flask(__name__)
#设置密钥,Flask-WTF使用这个密钥生成加密令牌，再用令牌验证请求中表单数据的真伪
app.config['SECRET_KEY'] = 'qlsuxalee'
#设置session的有效时间
app.permanent_session_lifetime = timedelta(minutes=5)
#添加mongodb的配置
app.config['MONGODB_SETTINGS'] = {
	'db': 'TestDb',
	'host': '115.159.161.107',
	'port':27017,
	'username':'root',
	'password':'liu123456'
}
bootstrap = Bootstrap(app)#插件初始化
manager = Manager(app)#命令行解释器
momen = Moment(app)
db = MongoEngine(app)

#设置调试模式
app.debug = True

class User(db.Document):
	#定义mongodb的数据库类型
	username = db.StringField(required=True)
	#username = db.StringField(required=True,unique=True)
	passwd = db.StringField(required=True)

@app.route('/index')
def index():
	name = session.get('username')
	return render_template('index.html',name=name,current_time=datetime.utcnow())
		
#注册界面
@app.route('/signup',methods=['GET','POST'])
def signup():
	name = None
	nameForm = NameForm()
	#先判断session是否存在之
	if session.get('username'):
		#已经登录过的,返回到主界面
		return redirect(url_for('index'))
		# return render_template('index.html',name=session.get('username'),current_time=datetime.utcnow())
	else:
		#nameForm.validate_on_submit()方法，提交表单后，
		#如果数据被所有验证函数接受，那么nameForm.validate_on_submit()方法返回True，
		#否则返回False
	
		#没有登录过的
		if nameForm.validate_on_submit():
			userName = nameForm.name.data#获取表格输入
			userPasswd = nameForm.passwd.data
			user = User(username=userName,passwd=userPasswd)
			#将填空置空
			nameForm.name.data = ''
			nameForm.passwd.data = ''
			# if first:
			# first = True
			if User.objects(username=userName):
				#判断该用户名是否被注册了
				flash("This username has exitted!")
			else:
				#如果还没有注册
				if user.save():
					print(user.save())
					#设置seesion，记录登陆状态
					session['username'] = userName
					#数据库存储成功的话
					return redirect(url_for('index'))
					# return render_template('index.html',name=userName,current_time=datetime.utcnow())
				else:
					flash("Input Error")
		return render_template('signup.html',form=nameForm,current_time=datetime.utcnow())

@app.route('/logout')
def logout():
	#判断是否登陆过
	if not session.get('username'):
		flash("你还没有登陆")
		return redirect(url_for('index'))
	else:
		session.pop('username',None)
		return redirect(url_for('index'))

@app.route('/user/<name>')
def user(name):
	#默认在templates文件夹中寻找模板
	return render_template('user.html',user=name)

#游戏介绍界面
@app.route('/introduction')
def page():
	return render_template('introduction.html')

#404 page
@app.errorhandler(404)
def page_no_found(e):
	return render_template('404.html')


if __name__ == '__main__':
	app.run()
	#manager.run()#可以在命令行中传入参数并接收，即可以解析命令行参数


