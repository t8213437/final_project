#!/usr/bin/env python3

import os, pprint, sqlite3
from collections import namedtuple

def open_database(path='msg.db'):
	new = not os.path.exists(path)
	db = sqlite3.connect(path)
	if new:
		c = db.cursor()
		c.execute('CREATE TABLE information (id INTEGER PRIMARY KEY,'
				  ' form_user TEXT, to_user TEXT, memo TEXT, Picid INTEGER)')
		add_msg(db, 'brandon', 'psf', 'hello world!!', '-1')
		add_msg(db, 'brandon', 'liz', 'How aer you~', '-1')
		add_msg(db, 'sam', 'brandon', 'Hi!!Hi!!', '-1')
		db.commit()
	return db

def add_msg(db, form_user, to_user, memo, picid):
	db.cursor().execute('INSERT INTO information (form_user, to_user, memo, picid)'
						' VALUES (?, ?, ?, ?)', (form_user, to_user, memo, picid))

def get_msg(db, account):
	c = db.cursor()
	c.execute('SELECT * FROM information WHERE form_user = ? or to_user = ?'
			  ' ORDER BY id', (account, account))
	Row = namedtuple('Row', [tup[0] for tup in c.description])
	return [Row(*row) for row in c.fetchall()]

if __name__ == '__main__':
	db = open_database()
	pprint.pprint(get_msg(db, 'brandon'))
