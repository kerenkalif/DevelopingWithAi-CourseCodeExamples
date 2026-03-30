from flask import Flask, request, jsonify
from flask_cors import CORS
from secret_key import open_ai_key
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=open_ai_key)

# Dictionary to store conversations per user
conversations = {}

@app.route('/set_role', methods=['POST'])
def set_role():
    data = request.json
    user_id = data.get('user_id')
    role_str = data.get('role', 'You are a helpful assistant.')
    role_str += " You are not allowed to answer anything that is not part of your profession."
    
    print(f"User {user_id} - The role: {role_str}")
    
    conversations[user_id] = [{"role": "system", "content": role_str}]
    
    resp = client.chat.completions.create(model="gpt-4", messages=conversations[user_id])
    return jsonify({"status": "success", "full_response": resp.to_json()})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get('user_id')
    user_input = data.get('message', '')
    
    # Get this user's messages, or create empty list
    if user_id not in conversations:
        conversations[user_id] = [{"role": "system", "content": "You are a helpful assistant."}]
    
    messages = conversations[user_id]
    messages.append({"role": "user", "content": user_input})
    
    resp = client.chat.completions.create(model="gpt-4", messages=messages)
    reply = resp.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    
    print(f"User {user_id} - Tokens used: {resp.usage.prompt_tokens}")
    
    return jsonify({
        "reply": reply,
        "tokens_used": resp.usage.prompt_tokens
    })

@app.route('/reset', methods=['POST'])
def reset():
    data = request.json
    user_id = data.get('user_id')
    
    if user_id in conversations:
        del conversations[user_id]
    
    print(f"User {user_id} - Chat reset")
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
