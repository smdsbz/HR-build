#!/usr/bin/python3
# -*- coding: utf-8 -*-

'   HR System build  ---- by smdsbz   '

from flask import Flask, render_template, url_for
from flask import redirect, request, session, make_response, flash
import sqlite3, os

app = Flask(__name__)
app.secret_key = 'DogLeeNation(2B||!2B)-->|'

######## functions ########

def getAll():
	database = sqlite3.connect(os.path.join(app.root_path, 'data.db'))
	cursor = database.execute('select * from test')
	data = cursor.fetchall()
	database.close()
	return data

def getConditonal(column, conditon, require):
	#print('getConditional(%s,%s,%s) called' % (column,conditon,require))
	database = sqlite3.connect(os.path.join(app.root_path, 'data.db'))
	cursor = database.execute("select %s from test where %s = '%s'" % (column, conditon, require))
	data = cursor.fetchall()
	#print(data)
	database.close()
	return data

def getAdmin(column, conditon, require):
	#print('getConditional(%s,%s,%s) called' % (column,conditon,require))
	database = sqlite3.connect(os.path.join(app.root_path, 'data.db'))
	cursor = database.execute("select %s from admin where %s = '%s'" % (column, conditon, require))
	data = cursor.fetchall()
	#print(data)
	database.close()
	return data

def verify(id, passwd):
	database = sqlite3.connect(os.path.join(app.root_path, 'data.db'))
	cursor = database.execute("select passwd from admin where id = '%s'" % id)
	correct = cursor.fetchone()
	database.close()
	#print(correct[0])
	if passwd == correct[0]:
		return 1
	else:
		session.pop('id', None)
		return 0

def updatePerson(id):
	database = sqlite3.connect(os.path.join(app.root_path, 'data.db'))
	database.execute("update test set name = '%s', gender = '%s', qq = '%s', tel = '%s', wchat = '%s', emg = '%s', school = '%s', class = '%s', apart = '%s', depart = '%s', grp = '%s', occup = '%s', dateofjoin = '%s' where id = '%s'" % (request.form['name'], request.form['gender'], request.form['qq'], request.form['tel'], request.form['wchat'], request.form['emg'], request.form['school'], request.form['class'], request.form['apart'], request.form['depart'], request.form['group'], request.form['occup'], request.form['dateofjoin'], id))
	database.commit()
	database.close()

def updateIssue(idx):
	database = sqlite3.connect(os.path.join(app.root_path, 'data.db'))
	database.execute("update issue set title = '%s', body = '%s' where idx = '%s'" % (request.form['title'], request.form['body'], idx))
	database.commit()
	database.close()

def grepPerson(column, require):
	#print('grepPerson(%s,%s) called' % (column,require))
	database = sqlite3.connect(os.path.join(app.root_path, 'data.db'))
	cursor = database.execute("select * from test where %s GLOB '*%s*'" % (column, require))
	data = cursor.fetchall()
	database.close()
	print(data)
	return data

def grepIssue(column, require):
	database = sqlite3.connect(os.path.join(app.root_path, 'data.db'))
	cursor = database.execute("select * from issue where %s = '%s'" % (column, require))
	data = cursor.fetchall()
	database.close()
	print(data)
	return data

def addPerson():
	database = sqlite3.connect(os.path.join(app.root_path, 'data.db'))
	try:
		database.execute("insert into test (id,name,gender,qq,tel,wchat,emg,school,class,apart,depart,grp,occup,dateofjoin) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (request.form['id'], request.form['name'], request.form['gender'], request.form['qq'], request.form['tel'], request.form['wchat'], request.form['emg'], request.form['school'], request.form['class'], request.form['apart'], request.form['depart'], request.form['group'], request.form['occup'], request.form['dateofjoin']))
	except:
		# issue: execute() fail when NULL exist in request.form
		print("addPerson() failed!")
	database.commit()
	database.close()

def addIssue():
	database = sqlite3.connect(os.path.join(app.root_path,'data.db'))
	try:
		database.execute("insert into issue (id,title,body) values ('%s','%s','%s')" % (request.form['id'],request.form['title'],request.form['body']))
	except:
		print((request.form['id'], request.form['title'], request.form['body']))
	database.commit()
	database.close()

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
		try:
			if verify(session['id'], session['passwd']):
				return redirect(url_for('personal'))
			else:
				# only one is None
				print("not TypeError")
				flash("用户名或密码错误！")
				return render_template('login.html')
		except TypeError:
			# both are None
			print("TypeError")
			flash("用户名或密码错误！")
			return render_template('login.html')

@app.route('/personal/')
def personal():
	try:
		session['id']
		database = getAdmin('id','id',session['id'])
		return render_template('personal_base.html', database = database)
	except KeyError:
		print("TypeError")
		flash("请登录")
		return redirect(url_for('login'))

@app.route('/logout/')
def logout():
	if 'id' in session:
		session.pop('id', None)
	return redirect(url_for('index'))

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
	# update for personale info
	try:
		session['id']
		if request.method == 'GET':
			print(id)
			return render_template('info_update.html', database=getConditonal('*','id',id),id=id)
		elif request.method == 'POST':
			updatePerson(id)
			return redirect(url_for('personal'))
	except KeyError:
		flash("请登录！")
		return redirect(url_for('login'))

@app.route('/search_person/', methods=['GET', 'POST'])
def search_person():
	try:
		session['id']
		if request.method == 'POST':
			return render_template('search_person.html', result=grepPerson(request.form['direction'],request.form['content']))
		elif request.method == 'GET':
			return render_template('search_person.html', result=grepPerson('id','苟'))
	except KeyError:
		flash("请登录!")
		return redirect(url_for('login'))

@app.route('/entry_person/', methods=['GET', 'POST'])
def entryPerson():
	try:
		session['id']
		if request.method == 'POST':
			addPerson()
			print("addPerson() called")
			return redirect(url_for('personal'))
		elif request.method == 'GET':
			return render_template('info_entry.html')
	except KeyError:
		flash("请登录！")
		return redirect(url_for('login'))

@app.route('/entry_issue/', methods=['GET', 'POST'])
def entryIssue():
	try:
		session['id']
		if request.method == 'POST':
			addIssue()
			print("addIssue() called")
			return redirect(url_for('personal'))
		elif request.method == 'GET':
			return render_template('issue_entry.html')
	except KeyError:
		flash("请登录！")
		return redirect(url_for('login'))

@app.route('/search_issue/', methods=['GET', 'POST'])
def search_issue():
	try:
		session['id']
		if request.method == 'POST':
			# fxxk the same-name issue!!!
			if request.form['direction'] == 'name':
				id_listed = getConditonal('id','name',request.form['content'])
			else:
				id_listed = request.form['content']
			print(id_listed)
			result = grepIssue('id',id_listed[0][0])
			if result == []:
				result = [(id_listed[0][0],"无搜索结果",""),]
			return render_template('search_issue.html', name=getConditonal('name','id',id_listed[0][0])[0][0], result=result)
		elif request.method == 'GET':
			return render_template('search_issue.html', name="姓名", result=[("#!","编号","标题","内容"),])
	except IndexError:
			return render_template('search_issue.html', name="姓名", result=[("编号","标题","内容"),])
	except KeyError:
		flash("请登录!")
		return redirect(url_for('login'))

@app.route('/update_issue/<idx>', methods=['GET', 'POST'])
def alter(idx):
	# alter for issue
	try:
		session['id']
		if request.method == 'GET':
			print(id)
			return render_template('issue_update.html', database=grepIssue('idx',idx))
		elif request.method == 'POST':
			updateIssue(idx)
			return redirect(url_for('personal'))
	except KeyError:
		flash("请登录！")
		return redirect(url_for('login'))


######## main ########

if __name__ == '__main__':
	# host = "0.0.0.0"  -->  mobile support!
	app.run(host="0.0.0.0", debug=True)
