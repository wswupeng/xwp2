import web
import model
from settings import render
import os

class Index(object):
	def GET(self):
		return render.index()

class Post(object):
	def GET(self, post_id):
		# TODO validate post through api, or validate in render? use try catch.	
		return render.post(post_id)
	
	def POST(self, post_id):
		i = web.input(author='', email='', url=None, comment='', reply_notify_mail=None)

		# TODO validate email format, and also do it in html javascript.
		if i.author and i.email and i.comment: 
			model.new_comment(post_id, i.author, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'], i.comment, i.url, i.email, i.reply_notify_mail=='on')

			# TODO difference between seeother and redirect.
			raise web.seeother('/post/' + post_id)
		else:
			# TODO: show error message.
			return render.post(post_id)

"""
#temporary disable it.
class Upload(object): 
	def GET(self, year, month, key):
		u = model.get_uploadinfo(key)

		if not u:
			raise web.notfound()

		file_path = 'uploads/' + str(year) + '/' + str(month) + '/' + str(key) + '_' + u.file_name 

		if os.path.isfile(file_path):
			f = open(file_path, 'r')
			content = f.read()
			f.close()
			return content
		else:
			raise web.notfound()

class Feed(object):
	def GET(self):
		return render.rss()
"""


