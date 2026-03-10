from flask import Flask
from flask_cors import CORS

from extension import db
from src.Api import itemApi, userApi, analysisApi, aiApi

app = Flask(__name__)
CORS().init_app(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost:3306/web-py-db?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.static_folder = 'static'
app.static_url_path = '/static' 
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'hello world'


item_api = itemApi.ItemApi.as_view('item_api')
app.add_url_rule('/items/add', view_func=item_api, methods=['POST'])
app.add_url_rule('/items/delete/<item_id>', view_func=item_api, methods=['DELETE'])
app.add_url_rule('/items/update/<item_id>', view_func=item_api, methods=['PUT'])
app.add_url_rule('/items/batch_add', view_func=item_api, methods=['POST'])
app.add_url_rule('/items/select/<user_id>', view_func=item_api, methods=['GET'])
app.add_url_rule('/items/select/selectByJson', view_func=item_api, methods=['POST'])

user_api = userApi.UserApi.as_view('user_api')
app.add_url_rule('/user/login', view_func=user_api, methods=['POST'])
app.add_url_rule('/user/register', view_func=user_api, methods=['POST'])
app.add_url_rule('/user/info/<uid>', view_func=user_api, methods=['GET'])

app.add_url_rule('/user/updata', view_func=user_api, methods=['POST', 'PUT'])

# 新增分析路由
analysis_api = analysisApi.AnalysisApi.as_view('analysis_api')
app.add_url_rule('/analysis/total', view_func=analysis_api, methods=['GET'])
app.add_url_rule('/analysis/monthly', view_func=analysis_api, methods=['GET'])
app.add_url_rule('/analysis/recent', view_func=analysis_api, methods=['GET'])


# 新增 AI 路由
ai_api = aiApi.AiApi.as_view('ai_api')
app.add_url_rule('/api/ai/chat', view_func=ai_api, methods=['POST'])
app.add_url_rule('/api/ai/chat/history', view_func=ai_api, methods=['GET'])
#app.add_url_rule('/api/ai/process_history', view_func=aiApi.process_history, methods=['POST'])
aiApi.AiApi.process_history = aiApi.AiApi.as_view('process_history')  # Correct reference to the class
app.add_url_rule('/api/ai/process_history', view_func=aiApi.AiApi.process_history, methods=['POST'])

if __name__ == '__main__':
    app.run()
