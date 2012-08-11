import web, datetime
"""
	TODO:
	try/except, check every sql operation.
	return True or False or None.
	check input parameters, such as postid > 0.
"""

db = web.database(dbn='mysql', db='blog2', user='root', pw='wpeng')

def get_posts(limit=-1, order='posted_on DESC', excerpt=False):
	#TODO excerpt 
	if limit == -1:
		limit_val = None
	else:
		limit_val = limit

	return db.select('entries', order=order, limit=limit_val)

def get_post(entry_id, excerpt=False):
	try:
		#TODO what if select return none?
		return db.select('entries', where='id=$entry_id', vars=locals())[0]
	except:
		return None

# TODO tag, categories.
# return insert post id.
def new_post(title, content, slug='', tag='', categories=''):
	try:
		return db.insert('entries', title=title, content=content, posted_on=datetime.datetime.utcnow(), slug=slug, tag='')
	except:
		return None 

#TODO tag, categories.
def update_post(entry_id, title, content, slug, tag, categories):
	try:
		db.update('entries', where='id=$entry_id', vars=locals(), title=title, content=content, slug=slug, tag='')
		return True
	except:
		return False

def delete_post(entry_id):
	try:
		db.delete('entries', where='id=$entry_id', vars=locals())
		db.delete('comments', where='entry_id=$entry_id', vars=locals())
		return True
	except:
		return False

def new_comment(entry_id, author, content, url='', email='', reply_notify_mail=False):
	try: 
		db.insert('comments', entry_id=entry_id, author=author,
					content=content, posted_on=datetime.datetime.utcnow(),
					url=url, email=email, reply_notify_mail=reply_notify_mail)
		return True
	except:
		return False


def get_comments(entry_id=-1, limit=-1, order='posted_on DESC'):
	if entry_id == -1: 
		where_val = None
	else:
		where_val = 'entry_id=$entry_id'
	if limit == -1:
		limit_val = None
	else:
		limit_val = limit

	return db.select('comments', where=where_val, order=order, limit=limit_val, vars=locals())

def get_comment_num(entry_id=-1):
	if entry_id == -1: 
		where_val = None
	else:
		where_val = 'entry_id=$entry_id'

	# TODO: what if result None?
	x = db.select('comments', what='COUNT(*)', where=where_val, vars=locals())
	return x[0]['COUNT(*)']

def get_blogrolls(limit=-1):
	return None

def get_post_categories(entry_id):
	try:
		c = db.select('entries', what='categories', where='id=$entry_id', vars=locals())[0]
	except:
		return None

	if c.categories:
		category_list = c.categories.split(',')	
		return map(lambda x: get_category(int(x)), category_list)
	else:
		return None

def get_category(category_id):
	try:
		return db.select('categories', where='id=$category_id', vars=locals())[0]
	except:
		return None

def get_all_categories():
	return db.select('categories')
