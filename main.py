#!/usr/bin/env python
from urls import *
import web

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('userinfo'), initializer={'user_id': 0, 'loggedin' : 0})

def session_hook():
	web.ctx.session = session

app.add_processor(web.loadhook(session_hook))

if __name__ == '__main__':
	app.run()

