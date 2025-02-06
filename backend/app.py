from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI, OpenAIError
import ollama
import os

# 清除代理设置，防止代理服务器干扰连接
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''

client = OpenAI(api_key="sk-d321c3b960284c11b3961629980ce184", base_url="https://api.deepseek.com")


app = Flask(__name__)
CORS(app)

# Store messages in memory (replace with a database in production)
messages = []

@app.route('/api/messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

@app.route('/api/messages', methods=['POST'])
def send_message():
    data = request.json
    user_message = {
        'id': len(messages) + 1,
        'text': data['text'],
        'sender': 'user'
    }
    messages.append(user_message)
    
    # Call Ollama using Python library
    try:
        # Get response from Ollama
        response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": user_message['text']},
        ],
        stream=False
    )
        
        ai_text = response.choices[0].message.content
        
        ai_message = {
            'id': len(messages) + 1,
            'text': ai_text,
            'sender': 'ai'
        }
    except Exception as e:
        print(f"Error details: {str(e)}")  # 添加详细错误日志
        ai_message = {
            'id': len(messages) + 1,
            'text': f"Error: Could not connect to Ollama. Please ensure it's running. Error: {str(e)}",
            'sender': 'ai'
        }
    
    messages.append(ai_message)
    return jsonify([user_message, ai_message])


if __name__ == '__main__':
    app.run(debug=True) 