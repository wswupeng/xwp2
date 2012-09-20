
urls = (
	'/', 'pages.Index',
	'/post/(\d+)', 'pages.Post',
	# TODO what does '\d+', \w+ means?
	#'/upload/(\d+)/(\d+)/(\w+)', 'pages.Upload'
	'/admin/upload', 'admin.Upload',
	'/admin/edit-post', 'admin.EditPost',
	'/admin/new-post', 'admin.NewPost',
	'/admin', 'admin.NewPost'
	# '/admin/config', 'admin.Config'
)
