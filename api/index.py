from flask import Flask, jsonify
import os
import json
from flask_cors import CORS  # 导入CORS模块

app = Flask(__name__)
CORS(app)  # 启用CORS支持，允许所有域名跨域访问

# 计数器存储路径 (Vercel 临时存储)
COUNTER_FILE = "/tmp/counters.json"

def load_counters():
    """加载计数器数据"""
    if not os.path.exists(COUNTER_FILE):
        return {}
    with open(COUNTER_FILE, 'r') as f:
        return json.load(f)

def save_counters(counters):
    """保存计数器数据"""
    with open(COUNTER_FILE, 'w') as f:
        json.dump(counters, f)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def count_visit(path):
    """处理所有路径请求"""
    # 规范化路径 (移除首尾斜杠)
    path = path.strip('/') or 'root'
    
    counters = load_counters()
    
    # 增加计数器
    counters[path] = counters.get(path, 0) + 1
    
    save_counters(counters)
    
    return jsonify({
        'path': f'/{path}' if path != 'root' else '/',
        'count': counters[path]
    })

if __name__ == '__main__':
    app.run()
else:
    # Vercel 需要命名为 application 的 WSGI 对象
    application = app
