#!/usr/bin/env bash
/home/klee/python/bin/flask db upgrade --directory /home/klee/repo/klee_engine/application/migrations
/home/klee/python/bin/uwsgi --ini /home/klee/conf/uwsgi.ini
