#!/bin/sh

uwsgi -s :9000 -w wsgi-main -p 4
