from flask import Flask, render_template, redirect, request, session
import mysql.connector
app = Flask(__name__)

DB_NAME = 'self'
cnx = mysql.connector.connect(
		user='root',
		password='go away plz',
		host='localhost',
		database='self',
		buffered=True)



from random import randint
class MyClass:
    i = 12345
    def f(self):
		z = randint(1,50)
		return z

@app.route('/devfest')
def devfest():
    return redirect('http://devfe.st/')
	
@app.route('/about')
def devfest():
    return redirect('/about.html')

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', name = session['username'])
    return redirect('/login')

@app.route('/index')
def home():
    if 'username' in session:
        return render_template('index.html', name = session['username'])
    return redirect('/login')
	
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
	cursor = cnx.cursor()
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
				cursor.close()
				return redirect('/')
			else:
				cursor.close()
				print "Wrong password"
				return redirect('/login')
	cursor.close()
	print "Username not found"
	return redirect('/login')

@app.route('/stats')
def stats():
	x = MyClass()
	#return render_template('stats.html', name = session['username'])
	return render_template('stats.html', name = x.f())
		
@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect('/login')

@app.route('/signup')
def signup():
	if request.method == 'GET':
		return render_template('signup.html')
#	elif request.method == 'POST':


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'l34GE0q1l1U+4D8c4S/1Yg=='
    app.run()

cnx.close()

