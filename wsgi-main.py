#!/usr/bin/env python
from urls import *
import web

app = web.application(urls, globals())
application = app.wsgifunc()
session = web.session.Session(app, web.session.DiskStore('userinfo'), initializer={'user_id': 0, 'username' : 'default', 'loggedin' : 0})

def session_hook():
	web.ctx.session = session

app.add_processor(web.loadhook(session_hook))

if __name__ == '__main__':
#	web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
	app.run()

