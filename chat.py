#!/usr/bin/env python3

import msg
import ssl
from flask import Flask, redirect, request, url_for
from jinja2 import Environment, PackageLoader

user = {}
user['marry'] = '123456'
user['john'] = 'qwerty'
user['brandon'] = 'atigdng'
user['sam'] = 'xyzzy'

app = Flask(__name__)
get = Environment(loader=PackageLoader(__name__, '')).get_template

@app.route('/login', methods=['GET', 'POST'])
def login():
	username = request.form.get('username', '')
	password = request.form.get('password', '')
	if request.method == 'POST':
		if user[username] == password:
			response = redirect(url_for('index'))
			response.set_cookie('username', username)
			return response
	return get('login.html').render(username=username)

@app.route('/logout')
def logout():
	response = redirect(url_for('login'))
	response.set_cookie('username', '')
	return response

@app.route('/register', methods=['GET', 'POST'])
def register():
	username = request.form.get('username', '')
	password = request.form.get('password', '')
	if request.method == 'POST':
		if username not in user:
			user[username] = password
			response = redirect(url_for('index', flash='Register successful'))
			response.set_cookie('username', username)
			return response
	return get('register.html').render(username=username)

@app.route('/')
def index():
	username = request.cookies.get('username')
	if not username:
		return redirect(url_for('login'))
	information = msg.get_msg(msg.open_database(), username)
	return get('index.html').render(information=information, username=username,flash_messages=request.args.getlist('flash'))

@app.route('/chatwho', methods=['GET', 'POST'])
def chatwho():
	username = request.cookies.get('username')
	if not username:
		return redirect(url_for('login'))
	account = request.form.get('account', '').strip()
	complaint = None
	if request.method == 'POST':
		if account:
			response = redirect(url_for('send_msg'))
			response.set_cookie('account', account)
			return response
	return get('chatwho.html').render(complaint=complaint, account=account)

@app.route('/send_msg', methods=['GET', 'POST'])
def send_msg():
	username = request.cookies.get('username')
	if not username:
		return redirect(url_for('login'))
	account = request.cookies.get('account')
	if not account:
		return redirect(url_for('chatwho'))
	information = msg.get_msg(msg.open_database(), username)
	memo = request.form.get('memo', '').strip()
	picid = request.form.get('picid', '').strip()
	complaint = None
	if request.method == 'POST':
		if (memo or picid):
			db = msg.open_database()
			msg.add_msg(db, username, account, memo, picid)
			db.commit()
			return redirect(url_for('send_msg'))
	return get('send_msg.html').render(information=information, complaint=complaint, account=account, memo=memo, username=username)

if __name__ == '__main__':
	context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
	context.load_cert_chain('server.crt', 'server.key')
	app.run(host='127.0.0.1',port=12345, debug = True, ssl_context=context)
