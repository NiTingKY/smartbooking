import requests
from flask import request
from extension import db
from src.models.chat import Chat

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
    # 获取 user_id（假设通过 cookie 传递）
    #user_id = request.cookies.get('user_id')
    user_id = request.cookies.get('user_id')
    if not user_id:
        return {
            "status": "error",
            "message": "用户未登录"
        }

    # 保存用户消息
    for msg in messages:
        if msg['role'] == 'user':
            chat = Chat(user_id=user_id, role=msg['role'], content=msg['content'])
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

        # 保存 AI 回复
        chat = Chat(user_id=user_id, role="assistant", content=reply)
        db.session.add(chat)
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
        return {
            "status": "error",
            "message": f"HTTP 错误: {http_err}"
        }
    except requests.exceptions.RequestException as req_err:
        return {
            "status": "error",
            "message": f"网络错误: {req_err}"
        }
    except KeyError:
        return {
            "status": "error",
            "message": "解析错误: 响应格式不正确"
        }