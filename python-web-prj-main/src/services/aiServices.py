import requests
from flask import request
from extension import db
from src.models.chat import Chat
from src.models.item import Item
from src.services import itemServices
import datetime
import re
import logging

# 设置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# SiliconFlow API 配置
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = "Bearer sk-egezlbrjpmpxjkjxkckuncgoevfytiktiviodqhksxvacoyg"
MODEL = "Qwen/Qwen3-8B"
def chat_with_ai(messages):
    """
    与 SiliconFlow API 交互，发送消息并获取 AI 回复，同时保存对话到数据库。
    :param messages: 包含对话历史的列表
    :return: 字典，包含状态、消息和数据
    """
    user_id = request.cookies.get('user_id')
    if not user_id:
        return {
            "status": "error",
            "message": "用户未登录"
        }

    current_time = datetime.datetime.now()

    # 只处理最后一条用户消息
    user_message = None
    for msg in reversed(messages):  # 从后向前遍历，获取最新的用户消息
        if msg['role'] == 'user':
            user_message = msg
            break

    if user_message:
        content = user_message['content']
        # 检查是否已存在相同的聊天记录
        existing_chat = db.session.query(Chat).filter_by(
            user_id=user_id,
            role='user',
            content=content,
            create_time=current_time
        ).first()

        if not existing_chat:
            # 保存用户消息到 chat 表
            chat = Chat(user_id=user_id, role='user', content=content, create_time=current_time)
            db.session.add(chat)
            logger.debug(f"Saving user message: {content}")

            # 提取金额信息
            expense_match = re.search(r'(?:花了|花费了|花|买了|消费|花费|买|购买)(\d+\.?\d*)(?:块|元)?(.*)', content)
            income_match = re.search(r'(?:收入了|赚了|收了|收入|获得|得到|赚到|获得了)(\d+\.?\d*)(?:块|元)?(.*)', content)

            if expense_match or income_match:
                amount = float(expense_match.group(1) if expense_match else income_match.group(1))
                detail = (expense_match.group(2) if expense_match else income_match.group(2)).strip() or "未指定详情"
                is_income = 1 if income_match else 0
                logger.debug(f"Matched: amount={amount}, detail={detail}, is_income={is_income}")

                # 判断行为类别
                source = "未知"
                if expense_match:
                    if any(keyword in content for keyword in ["吃饭", "吃早饭", "吃午饭", "吃晚饭", "餐饮","吃"]):
                        source = "餐饮"
                    elif any(keyword in content for keyword in ["衣服", "购物", "买东西", "网购","买"]):
                        source = "购物"
                    elif any(keyword in content for keyword in ["房租", "水电", "物业","交钱"]):
                        source = "生活缴费"
                elif income_match:
                    if any(keyword in content for keyword in ["奖金", "工资", "薪资", "薪水"]):
                        source = "薪资"
                    elif "投资" in content:
                        source = "投资"

                # 确定交易时间
                transaction_time = current_time
                if "今天" in content:
                    transaction_time = current_time
                elif "昨天" in content:
                    transaction_time = current_time - datetime.timedelta(days=1)
                if "上午" in content:
                    transaction_time = transaction_time.replace(hour=9, minute=0, second=0)
                elif "晚上" in content:
                    transaction_time = transaction_time.replace(hour=19, minute=0, second=0)

                # 去重：检查是否已存在相同的记录
                existing_item = db.session.query(Item).filter_by(
                    user_id=user_id,
                    dollar=amount,
                    detail=detail,
                    create_time=transaction_time,
                    is_income=is_income
                ).first()

                if not existing_item:
                    item = Item(
                        dollar=amount,
                        plat="未知",
                        create_time=transaction_time,
                        update_time=current_time,
                        detail=detail,
                        user_id=user_id,
                        source=source,
                        is_delete=0,
                        is_income=is_income
                    )
                    logger.debug(f"Saving item: dollar={item.dollar}, source={item.source}")
                    itemServices.addItem(item)

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        usage = result["usage"]

        # 检查是否已存在相同的 AI 回复
        existing_chat = db.session.query(Chat).filter_by(
            user_id=user_id,
            role='assistant',
            content=reply,
            create_time=current_time
        ).first()

        if not existing_chat:
            # 保存 AI 回复到 chat 表
            chat = Chat(user_id=user_id, role="assistant", content=reply, create_time=current_time)
            db.session.add(chat)
            logger.debug(f"Saving AI reply: {reply}")

        # 提交数据库更改
        db.session.commit()

        return {
            "status": "success",
            "message": "请求成功",
            "data": {
                "reply": reply,
                "usage": usage
            }
        }
    except requests.exceptions.HTTPError as http_err:
        db.session.rollback()
        return {
            "status": "error",
            "message": f"HTTP 错误: {http_err}"
        }
    except requests.exceptions.RequestException as req_err:
        db.session.rollback()
        return {
            "status": "error",
            "message": f"网络错误: {req_err}"
        }
    except KeyError:
        db.session.rollback()
        return {
            "status": "error",
            "message": "解析错误: 响应格式不正确"
        }
def chatai(messages):
    
    """
    与 SiliconFlow API 交互，发送消息并获取 AI 回复，同时保存对话到数据库。
    :param messages: 包含对话历史的列表
    :return: 字典，包含状态、消息和数据
    """
    user_id = request.cookies.get('user_id')
    if not user_id:
        return {
            "status": "error",
            "message": "用户未登录"
        }

    current_time = datetime.datetime.now()

    # 只保存当前请求的对话到 chat 表（可选，视需求）
    for msg in messages:
        if msg['role'] == 'user':
            chat = Chat(user_id=user_id, role=msg['role'], content=msg['content'], create_time=current_time)
            db.session.add(chat)

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        usage = result["usage"]

        # 保存 AI 回复到 chat 表（可选，视需求）
        chat = Chat(user_id=user_id, role="assistant", content=reply, create_time=current_time)
        db.session.add(chat)


        return {
            "status": "success",
            "message": "请求成功",
            "data": {
                "reply": reply,
                "usage": usage
            }
        }
    except requests.exceptions.HTTPError as http_err:
        db.session.rollback()
        return {
            "status": "error",
            "message": f"HTTP 错误: {http_err}"
        }
    except requests.exceptions.RequestException as req_err:
        db.session.rollback()
        return {
            "status": "error",
            "message": f"网络错误: {req_err}"
        }
    except KeyError:
        db.session.rollback()
        return {
            "status": "error",
            "message": "解析错误: 响应格式不正确"
        }
    