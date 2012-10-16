import web, datetime
"""
	TODO:
	DB TRANSACTION, ROLLBACK!
	check input parameters, such as postid > 0.
	maybe it's not nessary to use excerpt here. 
	
	sql may fail, so try/except, return None if except.
	check database yizhixing.	
"""
db = web.database(dbn='mysql', db='blog2', user='root', pw='wpeng')
_option_cache = None

def _del_term_relationship(post_id, term_type):
	db.delete('term_relationship', where='post_id=$post_id and term_type=$term_type', vars=locals())

def _insert_term_relationship(post_id, term_array, term_type):
	if term_array:
		for c in term_array:
			db.insert('term_relationship', post_id=post_id, term_id=c, term_type=term_type)	
	else:
		# default tag or default category.
		if term_type == "post_category":
			term_id = 1
		elif term_type == "post_tag":
			term_id = 2
		db.insert('term_relationship', post_id=post_id, term_id=term_id, term_type=term_type)

def get_posts(limit=None, post_type='blog', order='posted_on DESC'):
	try:
		return db.select('posts', where='post_type=$post_type', order=order, limit=limit, vars=locals()).list()
	except:
		return None 

def get_post(post_id):
	try:
		return db.select('posts', where='id=$post_id', vars=locals())[0]
	except:
		return None

#TODO should we use kargs here?
def new_post(author_id, title, content, excerpt=None, 
			 slug=None, post_type='blog', comment_status='open', 
			 post_status='published', tags=None, categories=None):
	try:
		#TODO update GlobalInfo.
		post_id = db.insert('posts', author_id=author_id, title=title, 
						 			content=content, excerpt=excerpt, 
						 			slug=slug, post_type=post_type, 
						 			comment_status=comment_status,
						 			post_status=post_status, 
						 			posted_on=datetime.datetime.utcnow())

		_insert_term_relationship(post_id, tags, 'post_tag')
		_insert_term_relationship(post_id, categories, 'post_category')
		
		return post_id
	except:
		return None 

def update_post(post_id, **kargs):
	try:
		if 'tags' in kargs:
			tags = kargs.pop('tags')
			_del_term_relationship(post_id, 'post_tag')
			_insert_term_relationship(post_id, tags, 'post_tag')

		if 'categories' in kargs:
			categories = kargs.pop('categories')
			_del_term_relationship(post_id, 'post_category')
			_insert_term_relationship(post_id, categories, 'post_category')
			
		db.update('posts', where='id=$post_id', vars=locals(), **kargs)
		
		return True
	except:
		return False

def delete_post(post_id):
	try:
		db.delete('posts', where='id=$post_id', vars=locals())
		db.delete('comments', where='post_id=$post_id', vars=locals())

		_del_term_relationship(post_id, 'post_tag')
		_del_term_relationship(post_id, 'post_category')

		return True
	except:
		return False

def new_comment(post_id, author, author_ip, comment_agent, content, url=None, email=None, reply_notify_mail=False):
	try: 
		#TODO try update entry.commentCount.
		return db.insert('comments',
					post_id=post_id, author=author,
					author_ip=author_ip, comment_agent=comment_agent,							content=content, posted_on=datetime.datetime.utcnow(),
					url=url, email=email, reply_notify_mail=reply_notify_mail)
	except:
		return None 

def get_comments(post_id=None, limit=None, order='posted_on DESC'):
	if not post_id: 
		where_val = None
	else:
		where_val = 'post_id=$post_id'

	try:
		return db.select('comments', where=where_val, order=order, limit=limit, vars=locals()).list()
	except:
		return None 

#TODO this api can be implement in entry.commentcount
def get_comment_num(post_id=None):
	if not post_id: 
		where_val = None
	else:
		where_val = 'post_id=$post_id'

	x = db.select('comments', what='COUNT(*)', where=where_val, vars=locals())
	try:
		return x[0]['COUNT(*)']
	except:
		return None 

def get_category(id):
	try:
		return db.select('terms', where='id=$id', vars=locals())[0]
	except:
		return None

def get_post_categories(post_id):
	try:
		category_ids = db.select('term_relationship', what='term_id', where='post_id=$post_id and term_type="post_category"', vars=locals())

		return [get_category(c.term_id) for c in category_ids]
			
	except:
		return None

def get_all_categories():
	return db.select('terms', where='type="post_category"').list()

"""
#TODO its now not correct.
def get_category_tree():
	from tree import TreeNode
	root = TreeNode()
	for c in db.select('categories'):
		node = TreeNode(c)
		if c.parent_id == 0:
			root.add_child(node)
		else:
			for n in root:
				if n.value.id == c.parent_id: n.add_child(node)
"""	

"""parent_id=0 means no parent."""
def new_category(name, parent_id=0, description=''):
	try:
		return db.insert('terms', name=name, parent_id=parent_id, description=description, type='post_category')
	except:
		return None 

def update_category(id, **kargs):
	try:
		db.update('terms', where='id=$id', vars=locals(), **kargs)

		return True
	except:
		return False

def delete_category(id):
	if id == 1:
		#default category cannot be deleted.
		return False
	try:
		# TODO, optimize the sql.	
		# if the post just in it, put post into default
		# else delete the record between it.
		posts_in_category = db.select('term_relationship', where='term_id=$id and term_type="post_category"', vars=locals())
		r = []
		for p in posts_in_category:
			x = db.select('term_relationship', where='post_id=$p.post_id', what='COUNT(*)', vars=locals())[0]['COUNT(*)']

			if x == 1:
				r.append(p.post_id)
				
		for m in r:
			db.update('term_relationship', where='post_id=$m', vars=locals())
		db.delete('terms', where='id=$id', vars=locals())
		db.delete('term_relationship', where='term_id=$id and term_type="post_category"', vars=locals())
	except:
		return False

	return True

def get_option(name):
	if not _option_cache:
		db.select('options', where='is_custom=0', what='option_name,option_value')
		_option_cache = dict()
		for x in s:
			_option_cache.update(x)

	if name in _option_cache:
		return _option_cache[name]
	else:
		try:
			r = db.select('options', where='option_name=$name', vars=locals())[0].option_value
			_option_cache[name] = r

			return r
		except:
			return None

"""
def get_blogrolls(limit=None):
	return None


def new_uploadinfo(file_name, file_size):
	try:
		return db.insert('uploads', file_name=file_name, file_size=file_size)
	except:
		return None

def get_uploadinfo(key):
	try:
		return db.select('uploads', where='id=$key', vars=locals())[0]
	except:
		return None

#TODO USE OPTIONS table.
class GlobalInfo(object):
	def __init__(self):
		#read basic db info from db.
		#read from web.ctx.
		try:
			self.delegate = db.select('ginfo', where='id=1')[0]
		except:
			# the table now is empty.
			# if insert failed, we consider it as a bug, just complain. 
			db.insert('ginfo', baseurl=web.ctx.home, owner='xwp owner', version='0.1')

			self.delegate = db.select('ginfo', where='id=1')[0]
			
	def __getattr__(self, name):
		return getattr(self.g, name)
	
	def __setattr__(self, name, value):
		setattr(self.delegate, name, value)

g_info = GlobalInfo()
"""

