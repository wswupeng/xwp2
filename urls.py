
urls = (
	'/', 'pages.Index',
	'/post/(\d+)', 'pages.Post',
	# TODO what does '\d+', \w+ means?
	#'/upload/(\d+)/(\d+)/(\w+)', 'pages.Upload'
	'/admin/upload', 'admin.Upload',
	'/admin/edit-post/(\d+)', 'admin.EditPost',
	'/admin/new-post', 'admin.NewPost',
	'/admin', 'admin.Admin',
	'/admin/edit-category/(\d+)', 'admin.EditCategory',
	'/admin/new-category', 'admin.NewCategory'

	# '/admin/config', 'admin.Config'
)
