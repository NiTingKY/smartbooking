import json
import datetime
from flask import request

from src.models.item import Item
from extension import db

def addItem(item: Item):
    db.session.add(item)
    db.session.commit()
    return 'success'


def addItems(data:json):
    items = []  
    user_id = request.cookies.get('user_id')  
    if user_id is None: 
        return 'error'
    for item_data in data:  # 遍历 data 列表中的每个字典
        item = Item()  # 创建一个新的 Item 对象
        item.dollar = item_data.get('dollar')
        item.plat = item_data.get('plat')
        item.create_time = datetime.datetime.now()
        item.update_time = datetime.datetime.now()
        item.detail = item_data.get('detail')
        item.user_id = user_id
        item.source = item_data.get('source')
        item.is_income = item_data.get('is_income')
        item.is_delete = 0
        items.append(item)  # 将 Item 对象添加到 items 列表中
    db.session.add_all(items)  # 使用 add_all 方法一次性添加所有 Item 对象到数据库会话中
    db.session.commit()
    return len(items)  # 返回添加的 Item 对象数量

def getByUserId(user_id):
    items = Item.query.filter_by(user_id=user_id).all()  # 使用 filter_by 方法过滤出指定 user_id 的所有 Item 对象
    items_dict = [item.to_dict() for item in items]  # 将 Item 对象转换为字典列表
    return items_dict  

def updateByItemId(item_id, form):
    item = Item.query.get(item_id)  # 使用 get 方法获取指定 item_id 的 Item 对象
    if item is None:  # 如果没有找到对应的 Item 对象，则返回错误信息
        return 'error';
    item.dollar = form.get('dollar', item.dollar)
    item.plat = form.get('plat', item.plat)
    item.detail = form.get('detail', item.detail)
    item.source = form.get('source', item.source)
    item.is_income = form.get('is_income', item.is_income)
    item.update_time = datetime.datetime.now()
    db.session.commit()  
    return 'success'

def selectByJson(form): # 从 form 字典中获取 user_id 字段的值
    print(form)
    start_date = form.get('start_date')  # 从 form 字典中获取 start_date 字段的值
    end_date = form.get('end_date')  # 从 form 字典中获取 end_date 字段的值
    is_income = form.get('is_income')  # 从 form 字典中获取 is_income 字段的值
    plat = form.get('plat')  # 从 form 字典中获取 plat 字段的值
    source = form.get('source')  # 从 form 字典中获取 source 字段的值
    detail = form.get('detail')  # 从 form 字典中获取 detail 字段的值
    user_id = request.cookies.get('user_id')  # 从 request 对象的 cookies 属性中获取 user_id 字段的值
    if user_id is None:  # 如果没有找到对应的 Item 对象，则返回错误信息
        return 'error';
    
    query = Item.query.filter(Item.user_id == user_id)
    print("user_id {}".format( query.count()))
    if start_date is not None and start_date!= '':
        query = query.filter(Item.create_time > (start_date))
        print("start date {}".format(query.count))
    if end_date is not None and end_date!= '':
        query = query.filter(Item.create_time < (end_date))
        print("end date {}".format(query.count()))
    if is_income is not None and is_income != '':
        query = query.filter(Item.is_income == is_income)
        print("is_income".format(query.count()))
    if plat is not None and plat != '':
        query = query.filter(Item.plat == plat)
        print("plat {}".format(query.count()))
    if source is not None and source!= '':  
        query = query.filter(Item.source == source)
        print("source {}".format(query.count()))
    if detail is not None and detail!= '':  
        query = query.filter(Item.detail.like('%' + detail + '%'))
        print("detail {}".format(query.count()))
    items = query.all() 
    items_dict = [item.to_dict() for item in items]  # 将 Item 对象转换为字典列表
    return items_dict


def deleteByItemId(item_id):
    item = Item.query.filter_by(uid=item_id).first()  # 使用 get 方法获取指定 item_id 的 Item 对象，使用 first() 方法获取第一个匹配的结果，而不是一个列表 o  
    if item is None:  # 如果没有找到对应的 Item 对象，则返回错误信息
        return 'error';
    item.is_delete = 1
    item.update_time = datetime.datetime.now()
    db.session.commit()  # 提交数据库会话，将更新保存到数据库中
    return 'success' 
