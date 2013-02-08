from flask import Flask, render_template, redirect, request, session, Markup
import mysql.connector
import HTML
app = Flask(__name__)

cnx = mysql.connector.connect(
		user='root',
		password='go away plz',
		host='localhost',
		database='self',
		buffered=True)


cursor = cnx.cursor()

signInError = 'false'

from random import randint
class MyClass:
    i = 12345
    def f(self):
		z = randint(1,50)
		return z

@app.route('/devfest')
def devfest():
    return redirect('http://devfe.st/')
	
@app.route('/signup')
def signup():
	return render_template('signup.html')
	
@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/signin')
def signin():
    if 'username' in session:
        return render_template('dashboard.html', name = session['username'])
    if request.method == 'GET':
        return render_template('signin.html', error = signInError)
    elif request.method == 'POST':
        username = request.form['username']
	password = request.form['password']
	query = "SELECT user_name, user_password FROM user"
	cursor.execute(query)
	found = False
	for(user_name, user_password) in cursor:
		if username == user_name:
			found = True
			if password == user_password:
				session['username'] = username
				return redirect('/')
			else:
				print "Wrong password"
				return redirect('/signin')
	print "Username not found"
	return redirect('/signin')

@app.route('/')
def index():
    if 'username' in session:
       # return render_template('dashboard.html', name = session['username'])
       return redirect('/dashboard')
    return redirect('/login')

@app.route('/index')
def home():
    if 'username' in session:
        return render_template('dashboard.html', name = session['username'])
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
	password = request.form['password']
	query = "SELECT user_name, user_password FROM user"
	cursor.execute(query)
	found = False
	for(user_name, user_password) in cursor:
		if username == user_name:
			found = True
			if password == user_password:
				session['username'] = username
				signInError = 'display:none'
				return redirect('/')
			else:
				print "Wrong password"
				signInError = 'false'
				return redirect('/signin')
	print "Username not found"
	return redirect('/signin')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
	if request.method == 'GET':
		query = "SELECT user_id FROM user WHERE user_name=\"%s\"" % session['username']
		cursor.execute(query)
		for(user_id) in cursor:
			query = "SELECT * FROM tasks where user_id=%d" % user_id[0]
			cursor.execute(query)
			count = 0
			t = HTML.Table(header_row=['Task Title', 'Task Description'])
			for (user_id, task_title, task_description) in cursor:
				if count==3 or not task_title or not task_description:
					break;
				count=count+1
				t.rows.append([task_title, task_description])
			html = str(t)
			value = Markup(html)

		query = "SELECT user_id FROM user WHERE user_name=\"%s\"" % session['username']
		cursor.execute(query)
		for(user_id) in cursor:
			query = "SELECT * FROM rewards WHERE user_id=%d" % user_id[0]
			cursor.execute(query)
			count = 0
			t2 = HTML.Table(header_row=['Reward Title', 'Reward Description'])
			for (user_id, reward_title, reward_description) in cursor:
				if count==3 or not reward_title or not reward_description:
					break;
				count=count+1
				t2.rows.append([reward_title, reward_description])
			html2 = str(t2)
			value2 = Markup(html2)
		return render_template('dashboard.html', name=session['username'], mytaskstable=value, myrewardstable=value2)

@app.route('/reporttask', methods=['GET','POST'])
def reporttask():
	if request.method=='POST':
		task_title = request.form['task_title']
		task_description = request.form['task_description']
		if not task_title or not task_description:
			return redirect('/')
		query = "SELECT user_id FROM user WHERE user_name=\"%s\"" % session['username']
		cursor.execute(query)
		for(user_id) in cursor:
			query = "INSERT INTO tasks (user_id, task_title, task_description) VALUES (%d, \"%s\", \"%s\")" % (user_id[0], task_title, task_description)
			cursor.execute(query)
		cnx.commit()
		
        return redirect('/dashboard')
	

@app.route('/reportreward', methods=['GET','POST'])
def reportreward():
	if request.method=='POST':
		reward_title = request.form['reward_title']
		reward_description = request.form['reward_description']
		if not reward_title or not reward_description:
			return redirect('/')
		query = "SELECT user_id FROM user WHERE user_name=\"%s\"" % session['username']
		cursor.execute(query)
		for(user_id) in cursor:
			query = "INSERT INTO rewards (user_id, reward_title, reward_description) VALUES (%d, \"%s\", \"%s\")" % (user_id[0], reward_title, reward_description)
			cursor.execute(query)
		cnx.commit()
        return render_template('dashboard.html', name = session['username'])

# @app.route('/viewtask')
# def viewtask():
	#Code to view the tasks page here. 
#	if request.method == 'GET':
		
		

@app.route('/stats')
def stats():
	x = MyClass()
	#return render_template('stats.html', name = session['username'])
	return render_template('stats.html', name = x.f())
		
@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect('/login')

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'l34GE0q1l1U+4D8c4S/1Yg=='
    app.run()

cursor.close()
cnx.close()
