import web 
import model
from globals import admin_render 

MESSAGE_NONE = 0 
MESSAGE_UPDATE_DONE = 1 
MESSAGE_NEED_TITLE_OR_CONTENT = 2
MESSAGE_NEW_POST_DONE = 3 

class Post(object):
	def GET(self):
		# get from QUERY_STRING
		i = web.input(post_id=None, message=MESSAGE_NONE)

		#TODO validate i.post_id.
		#TODO how to accept *args/**kargs in template?
		return admin_render.post(i.post_id, None, i.message)

	def POST(self): 
		# get from http post form data.
		# TODO categories
		i = web.input(post_id=None, title='', content='', slug='', tag='', categories='')

		if i.title and i.content:
			if i.post_id:
				# TODO check the result.
				model.update_post(i.post_id, i.title, i.content, i.slug, i.tag, i.categories)
				web.seeother("/admin/post?post_id=%d&message=%d" % (i.post_id, MESSAGE_UPDATE_DONE))
			else:
				# TODO check the result.
				insert_id = model.new_post(i.title, i.content, i.slug, i.tag)
				# TODO if insert_id /else:
				web.seeother("/admin/post?post_id=%d&message=%d" % (insert_id, MESSAGE_NEW_POST_DONE))
		else:
			return admin_render.post(i.post_id, i, MESSAGE_NEED_TITLE_OR_CONTENT)

