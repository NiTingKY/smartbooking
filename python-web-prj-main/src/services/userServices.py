from flask import jsonify
from datetime import datetime
from src.models.user import User
from extension import db


def userLogin(account, password):
    user = User.query.filter_by(account=account).first()
    if user is None:
        return {
            'status': 'error',
            'message': '用户名不存在'
        }
    if user.password != password:
        return {
           'status': 'error',
           'message': '密码错误'
        }
    else:
        return {
            'status': 'success',
            'message': '登录成功',
            'user': user.to_dict()
        }


def userRegister(user:User):
    user_s = User.query.filter_by(account=user.account).first()
    if user_s is not None:
        return {
           'status': 'error',
           'message': '账号已存在'
        }
    db.session.add(user)
    db.session.commit()
    return {
        'status': 'success',
        'message': '注册成功',
        'user': user.to_dict()
    }

def getByUid(uid):
    user = User.query.filter_by(uid=uid).first()
    return user

def userUpdate(user: User, form_data):
    if 'name' in form_data:
        user.name = form_data['name']
    if 'password' in form_data:
        user.password = form_data['password'] 
    if 'phone' in form_data:
        user.phone = form_data['phone']
    if 'mail' in form_data:
        user.mail = form_data['mail']
    if 'sex' in form_data:
        user.sex = form_data['sex']
    if 'birth' in form_data:
        user.birth = form_data['birth']

    db.session.commit()
    return {
        'status': 'success',
        'message': '信息更新成功',
        'user': user.to_dict()
    }
