import web 
import model
from settings import admin_render 
from settings import render
from datetime import datetime
import simplejson as json
import md5
import random
import utils
import os

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
				raise web.seeother("/admin/edit-post/%d?message=%s" % (insert_id, MESSAGE_NEW_POST_DONE))
			else:
				return admin_render.post(None, i, MESSAGE_NEW_POST_ERROR)
		else:
			return admin_render.post(None, i, MESSAGE_NEED_TITLE_OR_CONTENT)

class EditPost(object):
	def GET(self, post_id):
		# get from QUERY_STRING
		i = web.input(message=MESSAGE_NONE)

		#TODO validate post_id in html?
		#TODO how to accept *args/**kargs in template?
		return admin_render.post(post_id, None, i.message)
	
	def POST(self, post_id): 
		# get from http post form data.
		i = web.input(author_id=None, title=None, 
					  content=None, excerpt=None, 
					  slug=None, post_type='blog', 
					  comment_status='open', post_status='published', 
					  tags=[], categories=[])
		
		#TODO author id	
		#TODO slug 
		if i.slug == '': i.slug = None
		i.author_id = 1

		values = dict(i)
		values.pop('submit')
	
		
		if model.update_post(post_id, **values):
			raise web.seeother("/admin/edit-post/%d?message=%s" % (post_id, MESSAGE_UPDATE_DONE))
		else:
			return admin_render.post(post_id, i, MESSAGE_UPDATE_ERROR)

class Admin(object):
	def GET(self):
		# utils.seeother_if_notadmin('/login')		
		raise web.seeother('/admin/setup')

class Upload(object):
	def GET(self):
		return render.admin.upload()

	#TODO chdir file dir.
	def POST(self):
		i = web.input(FileData=None, FileName=None, FileSize=None)

		if i.FileData and i.FileName and i.FileSize: 
			key = str(random.random())[2:] + str(random.random())[2:] + str(random.random())[2:]

			y = datetime.now().year
			m = datetime.now().month
			year_dir = 'static/uploads/' + str(y)
			month_dir = year_dir + '/' + str(m)

			if not os.path.exists(year_dir):
				os.mkdir(year_dir)
			if not os.path.exists(month_dir):
				os.mkdir(month_dir)
			
			file_path = month_dir + '/' + key + '_' + i.FileName
			
			try:
				f = open(file_path, 'wb')
				f.write(i.FileData)
				f.close()

				return json.dumps({'url': '/' + file_path})
			except:
				if os.path.isfile(file_path):
					os.remove(file_path)

				# how to set http status? see web.webapi
				web.badrequest()
		else:
			print i.FileData == {} or i.FileData == None, i.FileName, i.FileSize

class Login(object):
	def GET(self):
		if utils.is_admin():
			raise web.seeother('/')

		return render.admin.login(None)

	def POST(self):
		# get the md5-password from database by username
		# compare with the two password.
		# if ok, generate the session.
		i = web.input(username='', password='')

		if i.username == '' or i.password == '':
			return render.admin.login('password or username should not be null.')

		#TODO to implement.
		user = model.get_user(i.username) 
		if not user: 
			return render.admin.login('no such user.')
		
		pwd = i.password + salt
		md5_pwd = md5.new(pwd).hexdigest()
		if md5_pwd != user.password:
			return render.admin.login('password incorrect.')

		web.ctx.session.loggedin = 1
		# TODO: should use a more readable var. 
		web.ctx.session.user_id = user.id
		web.ctx.session.username = user.name

		raise web.seeother('/admin')
			
class Logout(object):
	def GET(self):
		utils.seeother_if_notadmin('/login')
		
		web.ctx.session.loggedin = 0
		web.ctx.session.user_id = 0

		raise web.seeother('/')

class NewCategory(object):
	def GET(object):
		return admin_render.category(None, None, None)

	def POST(object):
		i = web.input(name=None, parent_id=0, description='')
		
		if i.name:
			cid = model.new_category(name=i.name, 
							  parent_id=i.parent_id, 
							  description=i.description)
		if cid:
			web.seeother('/admin/edit-category/%d?message="new category done."', cid)
		else:
			return admin_render.category(None, i, 'new category error.')

class EditCategory(object):
	def GET(self, cid):
		i = web.input(message=None)
		return admin_render.category(cid, None, None)

	def POST(self, cid):
		i = web.input(name='', description='', parent_id=0)

		if not i.name:
			return admin_render.category(cid, i, 'name must be provided.')
		elif model.update_category(name=i.name, description=i.description, parent_id=i.parent_id):
			return admin_render.category(cid, i, 'category update ok.')

class Setup(object):
	def GET(self):
		i = web.input(message=None)
		return admin_render.setup(i.message)
	
	def POST(self):
		i = web.input()

		d = dict(i)
		# TODO, should we initial the options in init?
		if model.update_options(**d):
			raise web.seeother('/admin/setup?message=update setup done.')
		else:	
			raise web.seeother('/admin/setup?message=update setup failed.')

class AdminPosts(object):
	def GET(self):
		i = web.input(message=None)

		return admin_render.admin_posts(i.message)

	def POST(self):
		i = web.input(del_post_array=[])

		for pid in i.del_post_array:
			if not model.delete_post(pid):
				raise web.seeother('/admin/admin-posts?message=delete post failed.')

		raise web.seeother('/admin/admin-posts?message=delete post done.')

# maybe here we need check code, it's dangerous to delete anything.
class AdminCategories(object):
	def GET(self):
		i = web.input(message=None)

		return admin_render.admin_categories(i.message)
	
	def POST(self):
		i = web.input(del_category_array=[])

		for cid in i.del_category_array:
			if not model.delete_category(cid):
				raise web.seeother('/admin/admin-categories?message=delete category failed.')
		
		raise web.seeother('/admin/admin-categories/?message=delete category done.')

class UserAdmin(object):
	def GET(self):
		return render.admin.user_admin()
	
	def POST(self):
		# not implemented.
		pass	

class CommentAdmin(object):
	def GET(self):
		return render.admin.comment_admin()
	
	def POST(self):
		pass

class PageAdmin(object):
	def GET(self):
		return render.admin.page_admin()
	
	def POST(self):
		i = web.input(del_page_array=[])

		# page is 'page' post_type post.
		for pid in del_page_array:
			if not model.delete_post(pid):
				pass

		raise web.seeother("/admin/page-admin")

class LinkAdmin(object):
	def GET(self):
		return render.admin.link_admin()
	
	def POST(self):
		pass
	
