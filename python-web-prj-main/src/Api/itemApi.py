import datetime
from flask import request, make_response, jsonify
from flask.views import MethodView

from src.models.item import Item
from src.services import itemServices


class ItemApi(MethodView):
    def get(self, user_id):
        if user_id is not None:
            data = itemServices.getByUserId(user_id)
            if data is None:
                return {
                   'status': 'error',
                   'message': '数据不存在'
                }
            return make_response(jsonify(data), 200)
            

    def post(self):
        form = request.json
        if request.path == '/items/add':
            item = Item()
            item.dollar = form.get('dollar')
            item.plat = form.get('plat')
            item.create_time = datetime.datetime.now()
            item.update_time = datetime.datetime.now()
            item.detail = form.get('detail')
            item.user_id = request.cookies.get('user_id')
            item.source = form.get('source')
            item.is_income = form.get('is_income')
            item.is_delete = 0
            result = itemServices.addItem(item)
            if result == 'success':
                return {
                   'status': 'success',
                   'message': '数据添加成功'
                }
            else:
                return {
                   'status': 'error',
                   'message': '数据添加失败'
                }
        elif request.path == '/items/batch_add':
            data = form.get('data')  # 提取 data 列表
            if data:
                reult = itemServices.addItems(data)
                if reult != 0:
                    return make_response(jsonify(reult), 200) 
                else:
                    return {
                       'status': 'error',
                       'message': '数据添加失败'
                    } # 将数据转换为 JSON 格式并创建响应对象
            else:
                return {
                    'status': 'error',
                    'message': '数据错误'
                }
        elif request.path == '/items/select/selectByJson':
            form = request.json
            result = itemServices.selectByJson(form)
            if result is not None:
                return make_response(jsonify(result), 200)  # 将数据转换为 JSON 格式并创建响应对象
            else:
                return {
                   'status': 'error',
                   'message': '数据错误'
                }
        else:
            return {
                'status': 'error',
                'message': '无效的请求路径'
            }


    def delete(self, item_id):
        result = itemServices.deleteByItemId(item_id)
        return make_response(jsonify(result), 200) 

    def put(self, item_id):
        form = request.json
        result = itemServices.updateByItemId(item_id, form)
        return make_response(jsonify(result), 200)  # 将数据转换为 JSON 格式并创建响应对象