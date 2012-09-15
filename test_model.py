import model
"""
now its just in smoke test level.
"""

if __name__ == '__main__':
	#clear data
	for i in range(1,100):
		model.delete_post(i)
	for j in range(3, 100):
		model.delete_category(j)

	post_id = model.new_post(1, 'title', 'content', None, None, 'blog', 'open', 'published', None, None)
	assert(post_id)
	
	post = model.get_post(post_id)

	assert(post.author_id == 1 and post.title == 'title' and post.content == 'content' and post.excerpt== None and post.slug == None and post.post_type=='blog' and post.comment_status=='open' and post.post_status=='published')

	c = model.get_post_categories(post_id)
	assert(len(c) == 1 and c[0].name == 'uncategorized' and c[0].parent_id == 0 and c[0].id == 1 and c[0].description == '' and c[0].type=='post_category')
	
	# test tag. TODO.
	assert(model.update_post(post_id, author_id=2, title='new title', content='new content', comment_status='close', post_status='saved'))
	
	post = model.get_post(post_id)
	assert(post.author_id == 2 and post.title == 'new title' and post.content == 'new content' and post.excerpt== None and post.slug == None and post.post_type=='blog' and post.comment_status=='close' and post.post_status=='saved')
	
	assert(model.update_post(post_id, author_id=1, title='title', content='content', comment_status='open', post_status='published'))

	another_post_id = model.new_post(1, 'title', 'content', None, None, 'blog', 'open', 'published', None, None)
	assert(another_post_id)
	
	posts = model.get_posts()
	assert(len(posts)==2) 

	for post in posts:
		assert(post and post.author_id == 1 and post.title == 'title' and post.content == 'content' and post.excerpt== None and post.slug == None and post.post_type=='blog' and post.comment_status=='open' and post.post_status=='published')
	
	model.delete_post(post_id)
	model.delete_post(another_post_id)
	posts = model.get_posts()
	assert(not posts)
	
	post_id = model.new_post(1, 'title', 'content', None, None, 'blog', 'open', 'published', None, None)
	assert(post_id)

	for i in range(0, 10):
		author = 'author %d' %i
		content = 'comment %d' %i
		model.new_comment(post_id, author, '192.168.1.1', 'firefox 4.0', content)

	comments = model.get_comments()
	assert(comments and len(comments) == 10 and model.get_comment_num(post_id) == 10)

	ci = 9 
	for c in comments:
		assert(c.post_id == post_id and c.author == 'author %d' %ci and c.author_ip == '192.168.1.1' and c.comment_agent == 'firefox 4.0' and c.content == 'comment %d' %ci and c.url == None and c.email == None and c.reply_notify_mail == False)
		ci -= 1

	############start test category, now there is only default category.
	cid1 = model.new_category('category 1', 0, 'description 1')

	categories = model.get_all_categories()

	assert(len(categories) == 2 and cid1 > 0)

	for c in categories:
		if cid1 == c.id:
			assert(c.name == 'category 1' and c.parent_id == 0 and c.description == 'description 1')
	
	assert(model.update_category(cid1, name='new category 1', description='new description 1', parent_id=1))
	
	c1 = model.get_category(cid1)
	assert (c1.name == 'new category 1' and c1.parent_id == 1 and c1.description == 'new description 1')
	
	assert(model.delete_category(cid1))
	assert(len(model.get_all_categories()) == 1)

	
