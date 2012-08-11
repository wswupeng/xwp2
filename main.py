#!/usr/bin/env python
from urls import *
import web

app = web.application(urls, globals())
if __name__ == '__main__':
	app.run()

