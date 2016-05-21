from flask import Flask,render_template,session,url_for,flash
from flask.ext.wtf import Form
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager
from flask.ext.moment import Moment
from flask.ext.mongoengine import MongoEngine
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from datetime import datetime


class NameForm(Form):
	name = StringField('your name?',validators=[Required()])
	passwd = StringField('your passwd?',validators=[Required()])
	submit = SubmitField('Submit')


#创建Flask对象app，Flask类的构造函数只有一个必须指定的参数，即程序主模块或包的名字。在大多数程序中，Python的__name__变量就是所需要的值
app = Flask(__name__)
#设置密钥,Flask-WTF使用这个密钥生成加密令牌，再用令牌验证请求中表单数据的真伪
app.config['SECRET_KEY'] = 'qlsuxalee'
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

@app.route('/',methods=['GET','POST'])
def index():
	name = None
	nameForm = NameForm()
	#session.set('name') = ben
	#nameForm.validate_on_submit()方法，提交表单后，
	#如果数据鞥被所有验证函数接受，那么nameForm.validate_on_submit()方法返回True，
	#否则返回False
	
	#先判断session是否存在之
	if session.get('name'):
		if nameForm.validate_on_submit():
			newName = nameForm.name.data#获取表格输入
			if newName == session.get('name'):
				session['name'] = nameForm.name.data
				nameForm.name.data = ''
				return redirect(url_for('index'))#重定向
			else:
				flash("Input Error")
	else:
		#设置session值
		#session.set('name') = benq
		print(session.get('name'))
		return render_template('index.html',form=nameForm,name=session.get('name'),current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
	#默认在templates文件夹中寻找模板
	return render_template('user.html',user=name)

@app.route('/page')
def page():
	return render_template('page.html')

#404 page
@app.errorhandler(404)
def page_no_found(e):
	return render_template('404.html')


if __name__ == '__main__':
	#app.run(debug=True)
	manager.run()#可以在命令行中传入参数并接收，即可以解析命令行参数


