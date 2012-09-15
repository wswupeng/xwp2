import web

def is_admin():
	if web.ctx.session.loggedin == 1:
		return True
	else:
		return False

def seeother_if_notadmin(url):
	if not is_admin():
		raise web.seeother(url)





