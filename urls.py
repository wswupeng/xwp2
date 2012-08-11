urls = (
	'/', 'pages.Index',
	'/post/(\d+)', 'pages.Post',
	# TODO what does '\d+', \w+ means?
	'/upload/(\d+)/(\d+)/(\w+)', 'pages.Upload'
	'/admin/post', 'admin.Post'
	# '/admin/config', 'admin.Config'
)
