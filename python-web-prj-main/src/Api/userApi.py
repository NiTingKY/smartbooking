from datetime import datetime
from flask import request, make_response
from flask.views import MethodView
from extension import db
from src.models.user import User
from src.services import userServices


class UserApi(MethodView):
    def get(self, uid):
        if uid is not None:
            user = userServices.getByUid(uid)
            if user is None:
                return {
                    'status': 'error',
                    'message': '用户不存在'
                }
            return {
                'status': 'success',
                'result': user.to_dict()
            }

    def post(self):
        form = request.json
        print(form)
        if request.path == '/user/login':
            account = form.get('account')
            password = form.get('password')
            result = userServices.userLogin(account, password)
            if result.get('status') == 'success':
                response = make_response(result)
                response.set_cookie('user_id', str(result.get('user').get('uid')), 
                path='/',
                secure=True,        # 必须设置为True
                samesite='None',    # 需要HTTPS支持
                httponly=False
            )
                return response
            return {
               'status':'error',
               'message': '用户名或密码错误'
            }
        if request.path == '/user/register':
            user = User(
                name=form.get('name'),
                account=form.get('account'),
                password=form.get('password'),
                phone=form.get('phone'),
                mail=form.get('mail'),
                sex=form.get('sex'),
            )
            user.valid = 1
            user.birth = datetime.strptime(
                form.get('birth'), 
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            user.photo_adr = 'http://localhost:5000/static/photo.png'
            result = userServices.userRegister(user)
            return make_response(result)

        if request.path == '/user/updata':
            user_id = request.cookies.get('user_id')  # 添加user_id获取
            user = User.query.get(user_id)
            if not user:
                return {
                    'status': 'error',
                    'message': '用户不存在'
                }, 404
            form_data = request.json
            print(form_data)
            form_data['birth'] = datetime.strptime(
                form_data.get('birth'), 
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            result = userServices.userUpdate(user, form_data)
            return make_response(result)




    def delete(self, user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据删除成功'
        }

    def put(self, user_id):
        user: User = User.query.get(user_id)
        user.photo_adr = request.json.get('photo_adr')  # 新增头像路径映射
        db.session.commit()
        return {
            'status': 'success',
            'message': '头像更新成功',
            'photo_adr': user.photo_adr
        }
        user.uid = request.json.get('uid')
        user.account = request.json.get('account')
        user.name = request.json.get('name')
        user.password = request.json.get('password')
        user.phone = request.json.get('phone')
        user.mail = request.json.get('mail')
        user.sex = request.json.get('sex')
        user.birth = request.json.get('birth')
        user.valid = request.json.get('valid')
        user.photo_adr = request.json.get('photo_adr')
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据修改成功'
        }
