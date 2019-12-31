#!/usr/bin/env bash

# 后台启动 redis
redis-server /usr/local/etc/redis.conf

## 激活虚拟环境
source activate CMDBPath
# 启动celery
celery -A celerytask worker -l info

# 启动django
python manage.py runserver


