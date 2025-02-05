from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama
import os

# 清除代理设置，防止代理服务器干扰连接
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''

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
        response = ollama.chat(model='llama3.2:latest', messages=[
            {
                'role': 'user',
                'content': data['text']
            }
        ])
        
        ai_text = response['message']['content']
        
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

@app.route('/api/test-ollama', methods=['GET'])
def test_ollama():
    try:
        response = ollama.chat(model='llama3.2:latest', messages=[
            {
                'role': 'user',
                'content': 'Say hello!'
            }
        ])
        return jsonify({"status": "success", "response": response})
    except Exception as e:
        print(f"Test error details: {str(e)}")  # 添加测试错误日志
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True) 