from flask import request, make_response, jsonify
from flask.views import MethodView
from src.services import aiServices
from src.models.chat import Chat
from src.models.item import Item
from extension import db
import datetime
import logging
import re

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AiApi(MethodView):
    
    def post(self):
        """
        处理 AI 对话请求，接收消息历史并返回 AI 回复。
        """
        if not request.is_json:
            return {
                "status": "error",
                "message": "请求体必须是有效的 JSON 格式"
            }, 400
        
        form = request.json
        messages = form.get('messages', [])
        
        if not messages:
            return {
                "status": "error",
                "message": "消息列表不能为空"
            }, 400
        
        for msg in messages:
            if not isinstance(msg, dict):
                return {
                    "status": "error",
                    "message": "消息必须是字典格式"
                }, 400
            if 'role' not in msg or 'content' not in msg:
                return {
                    "status": "error",
                    "message": "每条消息必须包含 'role' 和 'content' 字段"
                }, 400
            if msg['role'] not in ['user', 'assistant', 'system']:
                return {
                    "status": "error",
                    "message": "消息的 'role' 必须是 'user', 'assistant' 或 'system'"
                }, 400
        
        # 添加系统提示（如果没有）
        CURRENT_DATE = datetime.datetime.now
        if not any(msg.get('role') == 'system' for msg in messages):
            messages.insert(0, {
                "role": "system",
                "content": "你是一个友好的助手，回答问题时尽量简洁、准确，并用中文回复。当前日期是 {CURRENT_DATE.strftime('%Y-%m-%d %H:%M:%S')}。"
            })
        
        # 只发送最新用户消息（如果前端只发送最新消息，可以跳过此步骤）
        latest_message = [msg for msg in messages if msg['role'] == 'user'][-1] if any(msg['role'] == 'user' for msg in messages) else None
        if latest_message:
            # 构造只包含系统提示和最新用户消息的列表
            ai_messages = [messages[0]] if messages[0]['role'] == 'system' else []
            ai_messages.append(latest_message)
            result = aiServices.chat_with_ai(ai_messages)
        else:
            result = aiServices.chat_with_ai(messages)

        if result["status"] == "success":
            result["data"]["timestamp"] = datetime.datetime.now().isoformat()
        return make_response(jsonify(result), 200 if result["status"] == "success" else 500)
        
    
    def get(self):
        user_id = request.cookies.get('user_id')
        if not user_id:
            return jsonify({"status": "error", "message": "用户未登录"}), 400
        chats = db.session.query(Chat).filter_by(user_id=user_id).order_by(Chat.create_time.asc()).all()
        history = [{"role": chat.role, "content": chat.content, "create_time": chat.create_time.isoformat()} for chat in chats]
        return jsonify({"status": "success", "data": history})

    def process_history(self):
        if not request.is_json:
            return {
                "status": "error",
                "message": "请求体必须是有效的 JSON 格式"
            }, 400
        
        form = request.json
        user_id = request.cookies.get('user_id')
        task = form.get('task', 'summarize')
        messages = form.get('messages', [])

        if not user_id:
            return jsonify({"status": "error", "message": "用户未登录"}), 400

        if not messages:
            return jsonify({"status": "error", "message": "没有提供消息进行处理"}), 400

        # Validate the messages
        for msg in messages:
            if not isinstance(msg, dict):
                return {
                    "status": "error",
                    "message": "消息必须是字典格式"
                }, 400
            if 'role' not in msg or 'content' not in msg:
                return {
                    "status": "error",
                    "message": "每条消息必须包含 'role' 和 'content' 字段"
                }, 400
            if msg['role'] not in ['user', 'assistant']:
                return {
                    "status": "error",
                    "message": "消息的 'role' 必须是 'user' 或 'assistant'"
                }, 400

        # Get the current timestamp
        current_time = datetime.datetime.now()
        current_date_str = current_time.strftime("%Y年%m月%d日 %H:%M CST")

        # Parse financial data from messages and save to item table
        


        # Format messages as a string for inclusion in the prompt
        messages_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])

        # Prepare the prompt for the AI
        if task == "analyze":
            system_prompt = (
                "你是一个财务助手，请分析以下历史聊天记录，重点关注用户的消费模式、支出类别和可能的财务建议。"
                "同时，分析最近的饮食记录，判断是否有营养不良风险，并提供具体的营养建议（如增加水果、蔬菜等）以保持膳食均衡。"
                f"当前日期和时间是 {current_date_str}。\n" 
                f"以下是历史记录：\n{messages_str}"
            )
        else:  # Default to summarize for other tasks
            system_prompt = (
                "你是一个财务助手，请总结以下历史聊天记录，提取关键信息。"
                f"当前日期和时间是 {current_date_str}。\n"
                f"以下是历史记录：\n{messages_str}"
            )

        ai_messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        # Log the input to the AI for debugging
        logger.debug(f"AI Input: {ai_messages}")

        result = aiServices.chatai(ai_messages)
        
        # Log the AI's response for debugging
        logger.debug(f"AI Response: {result}")

        if result["status"] == "success":
            reply = result["data"].get("reply", "")
            if not reply:
                reply = "无法分析所选记录，请提供更多信息或选择其他记录。"
            result["data"]["reply"] = reply
            result["data"]["timestamp"] = datetime.datetime.now().isoformat()  # Add timestamp to AI response
        return make_response(jsonify(result), 200 if result["status"] == "success" else 500)