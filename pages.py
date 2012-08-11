import web
import model
from globals import render
from datetime import datetime
import simplejson as json
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
		if i.author and i.email and i.comment: 
			# TODO validate email format, do it in html javascript.
			model.new_comment(post_id, i.author, i.comment, i.url, i.email, i.reply_notify_mail=='on')

			# TODO difference between seeother and redirect.
			web.seeother('/post/' + post_id)
		else:
			# TODO: show error message.
			return render.post(post_id)

class Upload(object):
	def GET(self, year, month, ):
		# TODO, do we need uploadinfo stores in database?
		u = model.get_uploadinfo(key)
		file_path = 'uploads/' + str(year) + '/' + str(month) + '/' + str(key) + '_' + u.filename 
		if os.path.isfile(file_path):
			f = open(file_path, 'r')
			content = f.read()
			f.close()
			return content
		else:
			web.notfound()
		
	def POST(self):
		# get the file content.
		i = web.input(FileData=None, FileName='', FileSize=0)

		if i.FileData and i.FileName and i.FileSize: 
			key = model.new_uploadinfo(i.FileName, i.FileSize)
			
			# save the file.
			y = datetime.now().year
			m = datetime.now().month
			year_dir = 'uploads/' + str(y)
			month_dir = year_dir + '/' + str(m)

			if not os.path.exists(year_dir):
				os.mkdir(year_dir)
			if not os.path.exists(month_dir):
				os.mkdir(month_dir)
			
			file_path = month_dir + '/' + str(key) + '_' + i.FileName
			
			try:
				f = open(file_path, 'wb')
				f.write(i.FileData)
				f.close()
				# return url.
				return json.dumps({'url': file_path})
			except:
				if os.path.isfile(file_path):
					os.remove(file_path)
				# how to set http status? see web.webapi
				web.badrequest()
			
