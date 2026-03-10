import datetime
from flask import request, make_response, jsonify
from flask.views import MethodView

from extension import db
from src.models.item import Item
from src.services import analysisServices, itemServices  # 添加itemServices导入


class AnalysisApi(MethodView):
    def get(self):
        # 获取总收入或总支出
        user_id = request.cookies.get('user_id')
        if request.path == '/analysis/total':
            stat_type = request.args.get('type')
            if stat_type == 'income':
                total = analysisServices.getTotalIncome(user_id)
            elif stat_type == 'expense':
                total = analysisServices.getTotalExpense(user_id)
            else:
                return {'status': 'error', 'message': '无效的统计类型'}, 400
            
            return {
                'status': 'success',
                'total': float(total),
                'currency': 'CNY'  # 货币单位调整为人民币
            }

        # 按月度统计收入或支出
        if request.path == '/analysis/monthly':
            stat_type = request.args.get('type')
            if stat_type == 'monthly_income':
                monthly_data = analysisServices.getMonthlyIncome(user_id)  # 修正为analysisServices
            elif stat_type == 'monthly_expense':
                monthly_data = analysisServices.getMonthlyExpense(user_id)  # 修正为analysisServices
            else:
                return {'status': 'error', 'message': '无效的统计类型'}, 400
            return {
                    'status': 'success',
                    'data': monthly_data,
                    'currency': 'CNY'
                }

        # 获取最近五条账单
        if request.path == '/analysis/recent':
            limit = 5
            recent_items = analysisServices.getRecentItems(user_id, limit)
            return {
                'status': 'success',
                'data': recent_items,
                'currency': 'CNY'
            }
       