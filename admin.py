import web 
import model
from settings import admin_render 
from settings import render
from datetime import datetime
import simplejson as json
import md5
import random
import utils

MESSAGE_NONE = '' 
MESSAGE_UPDATE_DONE = 'update post done.'
MESSAGE_UPDATE_ERROR = 'update post error.'
MESSAGE_NEED_TITLE_OR_CONTENT = 'no title or content.'
MESSAGE_NEW_POST_DONE = 'new post done.'
MESSAGE_NEW_POST_ERROR = 'new post error.' 

salt = '&A102ad@#)'

"""
NewPost and EditPost share admin/post.html  
"""

class NewPost(object):
	def GET(self):
		return admin_render.post(None, None, MESSAGE_NONE)
	
	def POST(self): 
		i = web.input(author_id=None, title=None, 
					  content=None, excerpt=None, 
					  slug=None, post_type='blog', 
					  comment_status='open', post_status='published', 
					  tags=[], categories=[])
	
		#TODO author id	
		#TODO slug 
		if i.slug == '': i.slug = None
		i.author_id = 1
		if i.title and i.content: # and i.author_id:
			insert_id = model.new_post(i.author_id, i.title, 
									   i.content, i.excerpt,
									   i.slug, i.post_type, 
									   i.comment_status, i.post_status, 
									   i.tags, i.categories)
			if insert_id:
				raise web.seeother("/admin/edit-post?post_id=%d&message=%s" % (insert_id, MESSAGE_NEW_POST_DONE))
			else:
				return admin_render.post(None, i, MESSAGE_NEW_POST_ERROR)
		else:
			return admin_render.post(None, i, MESSAGE_NEED_TITLE_OR_CONTENT)

class EditPost(object):
	def GET(self):
		# get from QUERY_STRING
		i = web.input(post_id=None, message=MESSAGE_NONE)

		if not i.post_id: 
			raise web.seeother('/admin')

		#TODO validate i.post_id in html?
		#TODO how to accept *args/**kargs in template?
		return admin_render.post(int(i.post_id), None, i.message)
	
	def POST(self): 
		# get from http post form data.
		i = web.input(author_id=None, title=None, 
					  content=None, excerpt=None, 
					  slug=None, post_type='blog', 
					  comment_status='open', post_status='published', 
					  tags=[], categories=[])
		
		if not i.post_id:
			raise web.seeother('/admin')

		#TODO author id	
		#TODO slug 
		if i.slug == '': i.slug = None
		i.author_id = 1

		values = dict(i)
		values.pop('post_id')
		values.pop('submit')
	
		
		if model.update_post(int(i.post_id), **values):
			raise web.seeother("/admin/edit-post?post_id=%d&message=%s" % (int(i.post_id), MESSAGE_UPDATE_DONE))
		else:
			return admin_render.post(None, i, MESSAGE_UPDATE_ERROR)

#temporary disable it. 
"""
class Admin(object):
	def GET(self):
		utils.seeother_if_notadmin('/login')		

class Upload(object):
	def GET(self):
		return render.admin.upload()

	def POST(self):
		i = web.input(FileData=None, FileName='', FileSize=0)

		if i.FileData and i.FileName and i.FileSize: 
			key = model.new_uploadinfo(i.FileName, i.FileSize)
			
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

				return json.dumps({'url': file_path})
			except:
				if os.path.isfile(file_path):
					os.remove(file_path)

				# how to set http status? see web.webapi
				web.badrequest()

class Login(object):
	def GET(self):
		if utils.is_admin():
			raise web.seeother('/index')

		return render.admin.login()

	def POST(self):
		# get the md5-password from database by username
		# compare with the two password.
		# if ok, generate the session.
		i = web.input(username='', password='')

		if i.username == '' or i.password == '':
			return render.admin.login_error('password or username should not be null.')

		#TODO to implement.
		user = model.get_user(i.username) 
		if not user: 
			return render.admin.login_error('no such user.')
		
		pwd = i.password + salt
		md5_pwd = md5.new(pwd).hexdigest()
		if md5_pwd != user.password:
			return render.admin.login_error('password incorrect.')

		web.ctx.session.loggedin = 1
		# TODO: should use a more readable var. 
		web.ctx.session.user_id = 1

		raise web.seeother('/admin')
			
class Logout(object):
	def POST(self):
		utils.seeother_if_notadmin('/login')
		
		web.ctx.session.loggedin = 0
		web.ctx.session.user_id = 0

		raise web.seeother('/index')
"""		
