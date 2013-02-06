from flask import Flask, render_template, redirect, request, session
import mysql.connector
app = Flask(__name__)

from random import randint
class MyClass:
    i = 12345
    def f(self):
		z = randint(1,50)
		return z

@app.route('/devfest')
def devfest():
    return redirect('http://devfe.st/')

@app.route('/signin')
def devfest():
    return redirect('/signin.html')
	
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
        username = request.form['username']
        session['username'] = username
        return redirect('/')

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
