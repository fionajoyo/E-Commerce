#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@Author: fionajoyo
@Time: 2022/3/27 
@FileName: config.py
"""
from sqlalchemy import create_engine

HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'flask1'
#USERNAME = 'users'
USERNAME = 'root'
PASSWORD = '*'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

