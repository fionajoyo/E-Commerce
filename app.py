


#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@Author: Yangyan
@Time: 2022/4/8 
@FileName: app2.py
"""

from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import json
import config
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=config.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)

class brand_info(db.Model):
    __table__name="brand_info"
    brand_id=db.Column(db.String(255),primary_key=True,autoincrement=True,nullable=False)
    brand_name = db.Column(db.String(255),nullable=False)
    brand_salescount = db.Column(db.String(255), nullable=False)
    brand_state = db.Column(db.String(255), nullable=False)

class user_info(db.Model):
    __table__name="user_info"
    user_name=db.Column(db.String(255),nullable=False)
    user_id=db.Column(db.String(255),primary_key=True,nullable=False)
    password=db.Column(db.String(255),nullable=False)
    user_level=db.Column(db.String(255),nullable=False)


@app.route('/login',methods=['POST'])
def login():
    # print(request)
    u_name = request.form['username']
    # print(u_name)
    p_word = request.form['password']
    # print(p_word)
    state={
        "username":u_name,
        "state":""
    }
    user = user_info.query.filter_by(user_name=u_name, password=p_word).first()
    if user:
        state['state']="success"
        return json.dumps(state),200  # 登录成功
    else:
        state['state'] = "fail"
        return json.dumps(state),200 # 登录失败



@app.route('/register',methods=['POST'])
def register():
    print(request.form)
    u_name = request.form['username']
    print(u_name)
    p_word = request.form['password']
    u_id=request.form['id']
    user = user_info.query.filter_by(user_id=u_id).first()

    state={
        'user_id':u_id,
        'state':''
    }

    if user:
        state['state']='fail'
        return json.dumps(state),200
    else:
        temp = user_info(user_name=u_name,user_id=u_id, password=p_word,user_level='1')
        db.session.add(temp)
        db.session.commit()
        state['state'] = 'success'
        return json.dumps(state),200







@app.route('/test')
def test():
    user = user_info.query.filter_by(user_name="1", password="1").first()
    return 'hello'




if __name__ == '__main__':

    app.run(host='127.0.0.1',debug=True)