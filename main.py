#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''   HR System build   '''

from flask import Flask, render_template, url_for
from flask import redirect, request, session, make_response, flash
from functools import wraps
import sqlite3, os, xlsxSwissKnife

######## initializaton ########

app = Flask(__name__)
app.secret_key = 'DogLeeNation(2B||!2B)-->|'

######## global configuration ########

FOLDER = os.path.join(os.curdir, 'score-sheets')  # xlsx location
DATABASE = os.path.join(app.root_path, 'data.db')  # db loaction

######## functions ########

def getAll():
	with sqlite3.connect(DATABASE) as database:
		cursor = database.execute('select * from test')
		data = cursor.fetchall()
		return data

def getConditonal(column, conditon, require):
	with sqlite3.connect(DATABASE) as database:
		cursor = database.execute("select %s from test where %s = '%s'" % (column, conditon, require))
		data = cursor.fetchall()
		return data

def getAdmin(column, conditon, require):
	with sqlite3.connect(DATABASE) as database:
		cursor = database.execute("select %s from admin where %s = '%s'" % (column, conditon, require))
		data = cursor.fetchall()
		return data

def verify(id, passwd):
	with sqlite3.connect(DATABASE) as database:
		cursor = database.execute("select passwd from admin where id = '%s'" % id)
		correct = cursor.fetchone()
		if correct==None:  # wrong id
			flash("用户名或密码错误！")
			return 0
		else:  # correct
			if passwd==correct[0]:
				return 1
			else:  # wrong passwd
				flash("用户名或密码错误！")
				return 0

def login_verify(to_be_decorated):
	'''  check-in decorator  '''
	@wraps(to_be_decorated)
	def decorated(*args, **kwargs):
		if 'id' not in session:
			flash("请登录！")
			return redirect(url_for('login'))
		return to_be_decorated(*args, **kwargs)
	return decorated

def updatePerson(id):
	with sqlite3.connect(DATABASE) as database:
		database.execute("update test set name = '%s', gender = '%s', qq = '%s', tel = '%s', wchat = '%s', emg = '%s', school = '%s', class = '%s', apart = '%s', depart = '%s', grp = '%s', occup = '%s', dateofjoin = '%s' where id = '%s'" % (request.form['name'], request.form['gender'], request.form['qq'], request.form['tel'], request.form['wchat'], request.form['emg'], request.form['school'], request.form['class'], request.form['apart'], request.form['depart'], request.form['group'], request.form['occup'], request.form['dateofjoin'], id))
		database.commit()

def updateIssue(idx):
	with sqlite3.connect(DATABASE) as database:
		database.execute("update issue set title = '%s', body = '%s' where idx = '%s'" % (request.form['title'], request.form['body'], idx))
		database.commit()

def grepPerson(column, require):
	with sqlite3.connect(DATABASE) as database:
		cursor = database.execute("select * from test where %s GLOB '*%s*'" % (column, require))
		data = cursor.fetchall()
		return data

def grepIssue(column, require):
	with sqlite3.connect(DATABASE) as database:
		if column == 'idx':
			cursor = database.execute("select * from issue where idx = %s" % require)
			return cursor.fetchall()
		else:
			if column == 'name':
				cursor = database.execute("select id from test where name = '%s'" % require)
				id = cursor.fetchone()[0]
			elif column == 'id':
				id = require
			cursor = database.execute("select * from issue where id = '%s'" % id)
			data = cursor.fetchall()
			return data

def addPerson():
	with sqlite3.connect(DATABASE) as database:
		database.execute("insert into test (id,name,gender,qq,tel,wchat,emg,school,class,apart,depart,grp,occup,dateofjoin) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (request.form['id'], request.form['name'], request.form['gender'], request.form['qq'], request.form['tel'], request.form['wchat'], request.form['emg'], request.form['school'], request.form['class'], request.form['apart'], request.form['depart'], request.form['group'], request.form['occup'], request.form['dateofjoin']))
		database.commit()

def addIssue():
	with sqlite3.connect(DATABASE) as database:
		database.execute("insert into issue (id,title,body) values ('%s','%s','%s')" % (request.form['id'],request.form['title'],request.form['body']))
		database.commit()

######## route ########

@app.route('/')
def index():
	# a useless port
	return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html');
	elif request.method == 'POST':
		session['id'] = request.form['id']
		session['passwd'] = request.form['passwd']
		if verify(session['id'], session['passwd']):
			return redirect(url_for('personal'))
		return redirect(url_for('logout'))

@app.route('/personal/', methods=['GET', 'POST'])
@login_verify
def personal():
	if request.method == 'GET':
		database = getAdmin('id','id',session['id'])
		return render_template('personal_base.html', database = database)
	elif request.method == 'POST':
		filename = request.form['title'] + ' - ' + request.form['date'] + '.xlsx'
		session['filename'] = filename
		if xlsxSwissKnife.newFile(request.form['title'], request.form['depart'], date=request.form['date']):
			return redirect(url_for('score'))
		else:
			flash("创建表格失败！")
			return redirect(url_for('personal'))

@app.route('/logout/')
def logout():
	if 'id' in session:
		session.pop('id', None)
		# the following lines are wierd
		session.pop('passwd', None)
		session.pop('filename', None)
	return redirect(url_for('index'))

@app.route('/update/<id>', methods=['GET', 'POST'])
@login_verify
def update(id):
	'''  update for personale info  '''
	if request.method == 'GET':
		print(id)
		return render_template('info_update.html', database=getConditonal('*','id',id),id=id)
	elif request.method == 'POST':
		updatePerson(id)
		return redirect(url_for('personal'))

@app.route('/search_person/', methods=['GET', 'POST'])
@login_verify
def search_person():
	if request.method == 'POST':
		return render_template('search_person.html', result=grepPerson(request.form['direction'],request.form['content']))
	elif request.method == 'GET':
		return render_template('search_person.html', result=grepPerson('id','苟'))

@app.route('/entry_person/', methods=['GET', 'POST'])
@login_verify
def entryPerson():
	if request.method == 'POST':
		addPerson()
		print("addPerson() called")
		return redirect(url_for('personal'))
	elif request.method == 'GET':
		return render_template('info_entry.html')

@app.route('/entry_issue/', methods=['GET', 'POST'])
@login_verify
def entryIssue():
	if request.method == 'POST':
		addIssue()
		print("addIssue() called")
		return redirect(url_for('personal'))
	elif request.method == 'GET':
		return render_template('issue_entry.html')

@app.route('/search_issue/', methods=['GET', 'POST'])
@login_verify
def search_issue():
	if request.method == 'POST':
		return render_template('search_issue.html', result=grepIssue(request.form['direction'], request.form['content']))
	elif request.method == 'GET':
		return render_template('search_issue.html', result=grepIssue('id', '苟'))

@app.route('/update_issue/<idx>', methods=['GET', 'POST'])
@login_verify
def alter(idx):
	''' alter for issue '''
	if request.method == 'GET':
		print(id)
		return render_template('issue_update.html', database=grepIssue('idx',idx))
	elif request.method == 'POST':
		updateIssue(idx)
		return redirect(url_for('personal'))

@app.route('/score_page/')
@login_verify
def score():
	if 'filename' not in session:
		return redirect(url_for('personal'))
	else:
		data = xlsxSwissKnife.read(session['filename'])
		print(data)
		return render_template('score-entry.html', data=data)


######## run ########

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)
