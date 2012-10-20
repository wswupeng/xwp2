#!/bin/sh

uwsgi -s :9000 -w wsgi_main -p 4
