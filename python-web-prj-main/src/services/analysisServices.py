import json
import datetime
from flask import request

from src.models.item import Item
from extension import db



# 获取总收入
def getTotalIncome(user_id):
    from sqlalchemy import func
    total = db.session.query(func.sum(Item.dollar)).filter(
        Item.user_id == user_id,
        Item.is_income == 1,
        Item.is_delete == 0
    ).scalar()
    return total if total else 0

# 获取总支出
def getTotalExpense(user_id):
    from sqlalchemy import func
    total = db.session.query(func.sum(Item.dollar)).filter(
        Item.user_id == user_id,
        Item.is_income == 0, 
        Item.is_delete == 0
    ).scalar()
    return total if total else 0

# 按月度统计收入
def getMonthlyIncome(user_id):
    from sqlalchemy import extract, func
    from src.models.item import Item
    
    monthly_data = db.session.query(
        extract('year', Item.create_time).label('year'),
        extract('month', Item.create_time).label('month'),
        func.sum(Item.dollar).label('total')
    ).filter(
        Item.user_id == user_id,
        Item.is_income == 1
    ).group_by('year', 'month').all()

    return [{
        "year": int(year),
        "month": int(month),
        "total": float(total) if total else 0.0
    } for year, month, total in monthly_data]


# 按月度统计收入
def getMonthlyExpense(user_id):
    from sqlalchemy import extract, func
    from src.models.item import Item
    
    monthly_data = db.session.query(
        extract('year', Item.create_time).label('year'),
        extract('month', Item.create_time).label('month'),
        func.sum(Item.dollar).label('total')
    ).filter(
        Item.user_id == user_id,
        Item.is_income == 0,  # 修改为支出条件
        Item.is_delete == 0
    ).group_by('year', 'month').all()

    return [{
        "year": int(year),
        "month": int(month),
        "total": float(total) if total else 0.0
    } for year, month, total in monthly_data]


def getRecentItems(user_id, limit=5):
    from src.models.item import Item
    
    items = Item.query.filter(
        Item.user_id == user_id,
        Item.is_delete == 0
    ).order_by(Item.create_time.desc()).limit(limit).all()

    return [item.to_dict() for item in items]
