#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@Author: fionajoyo
@Time: 2022/8/21 
@FileName: wsgi.py
"""


from app import app
import logging

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
    app.run()