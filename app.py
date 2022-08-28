


#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@Author: Yangyan
@Time: 2022/4/8 
@FileName: app2.py
"""

from flask import Flask, render_template, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
import json
import config
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import functools
import datetime

def create_token(api_user):
    '''
    生成token
    :param api_user:用户id
    :return: token
    '''

    # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    # 第二个参数是有效期(秒)
    s = Serializer(config.SECRET_KEY, expires_in=3600)
    # 接收用户id转换与编码
    token = s.dumps({"id": api_user}).decode("ascii")
    return token


def verify_token(token):
    '''
    校验token
    :param token:
    :return: 用户信息 or None
    '''

    # 参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(config.SECRET_KEY)
    try:
        # 转换为字典
        data = s.loads(token)
    except Exception:
        return None
    # 拿到转换后的数据，根据模型类去数据库查询用户信息
    user = user_info.query.filter_by(user_id=data["id"]).first()
    return user

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

class com_info(db.Model):
    __table__name='com_info'
    com_id=db.Column(db.String(255),nullable=False,primary_key=True)
    com_title=db.Column(db.String(255),nullable=False)
    com_class=db.Column(db.String(255),nullable=False)
    com_price=db.Column(db.String(255),nullable=False)
    user_id=db.Column(db.String(255),nullable=False)
    brand_id=db.Column(db.String(255),nullable=False)
    com_discount=db.Column(db.String(255),nullable=False)
    com_state=db.Column(db.String(255),nullable=False)


@app.route('/login',methods=['POST'])
def login():
    # print(request)
    u_id = request.form['userid']
    # print(u_name)
    p_word = request.form['password']

    if u_id and p_word:


        user = user_info.query.filter_by(user_id=u_id, password=p_word).first()
        if user:
            token = create_token(u_id)

            return jsonify(code=0,msg='success',data=token)
        else:
            return jsonify(code=1000,msg='登录失败') # 登录失败
    else:
        return jsonify(code=400,msg='bad request')


def login_required(view_func):
    @functools.wraps(view_func)
    def verify_token(*args, **kwargs):
        try:
            # 在请求头上拿到token
            token = request.form["token"]
        except Exception:

            return jsonify(code=1001, msg='缺少参数token')

        s = Serializer(config.SECRET_KEY)
        try:
            s.loads(token)
        except Exception:
            return jsonify(code=1002, msg="登录已过期")

        return view_func(*args, **kwargs)

    return verify_token


@app.route('/register',methods=['POST'])
def register():
    print(request.form)
    u_name = request.form['username']
    print(u_name)
    p_word = request.form['password']
    u_id=request.form['id']
    user = user_info.query.filter_by(user_id=u_id).first()

    if user:

        return jsonify(code=1005,msg='用户已经存在')
    else:
        try:
            temp = user_info(user_name=u_name,user_id=u_id, password=p_word,user_level='1')
            db.session.add(temp)
            db.session.commit()
            return jsonify(code=0,msg='注册成功')
        except Exception as e:
            db.session.rollback()   #回滚
            raise e


@app.route('/addbrand',methods=['POST'])
@login_required
def addbrand():
    #Post params:
    # token
    # brandid
    # brandname
    token=request.form['token']
    user=verify_token(token)
    if user:
        print(user.user_level)
        if user.user_level!='2':
            return jsonify(code=1004,msg='用户权限不足')
        b_id = request.form['brandid']
        print(b_id)
        b_name = request.form['brandname']
        brand = brand_info.query.filter_by(brand_id=b_id).first()
        state = {
            'brand_id': b_id,
            'state': ''
        }
        if brand:
            return jsonify(code=1006,msg='品牌id已经存在')
        else:
            try:
                temp = brand_info(brand_id=b_id,brand_name=b_name,brand_salescount='0',brand_state='0')
                db.session.add(temp)
                db.session.commit()
                return jsonify(code=0,msg='添加品牌成功')

            except Exception as e:
                db.session.rollback()
                raise e
    else:
        return jsonify(code=1003,msg="先登录再进行操作")

@app.route('/delbrand',methods=['POST'])
@login_required
def delbrand():
    #Post params：
    # token
    # brandid
    token = request.form['token']
    user = verify_token(token)
    if user:
        print(user.user_level)
        if user.user_level != '2':
            return jsonify(code=1004, msg='用户权限不足')
        b_id = request.form['brandid']
        try:
            brand_info.query.filter_by(brand_id=b_id).delete()
            db.session.commit()
            return jsonify(code=0,msg='删除成功')
        except Exception as e:
            db.session.rollback()
            return jsonify(code=1008,msg='品牌删除失败')
            raise e

@app.route('/addcom',methods=['POST'])
@login_required
def addcom():
    token=request.form['token']

    user = verify_token(token)
    if user:
        print(user.user_level)
        if user.user_level == '0':
            return jsonify(code=1004, msg='用户权限不足')
        c_id=request.form['comid']

        c_title=request.form['comtitle']
        c_class=request.form['comclass']
        c_price=request.form['comprice']
        u_id=user.user_id
        b_id=request.form['brandid']
        c_discount=request.form['discount']
        c_state='0'
        print(c_id,c_title,c_class,c_price,u_id,b_id,c_discount,c_state)

        try:
            com=com_info.query.filter_by(com_id=c_id).first()
            if com:
                return jsonify(code=1009,msg='商品已经存在')
            temp = com_info(com_id=c_id, com_title=c_title, com_class=c_class, com_price=c_price, user_id=u_id,
                            brand_id=b_id, com_discount=c_discount, com_state=c_state)
            db.session.add(temp)
            db.session.commit()
            return jsonify(code=0,msg='添加商品成功')
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify(code=1007,msg='上传商品失败')



@app.route('/delcom',methods=['POST'])
@login_required
def delcom():
    #Post params：
    # token
    # comid
    token = request.form['token']
    user = verify_token(token)
    if user:
        print(user.user_level)
        if user.user_level == '0':
            return jsonify(code=1004, msg='用户权限不足')
        c_id = request.form['comid']
        try:
            com_info.query.filter_by(com_id=c_id).delete()
            db.session.commit()
            return jsonify(code=0,msg='商品删除成功')
        except Exception as e:
            db.session.rollback()
            return jsonify(code=1010,msg='商品删除失败')
            raise e







@app.route('/test')
def test():
    user = user_info.query.filter_by(user_name="1", password="1").first()
    return 'hello'




if __name__ == '__main__':

    app.run(host='127.0.0.1',debug=True)