from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI()
messages = []

@app.route('/set_role', methods=['POST'])
def set_role():
    global messages
    data = request.json
    role_str = data.get('role', 'You are a helpful assistant.')
    role_str += ". You are not allowed to answer anything that is not part of your professionalise"
    print("The role: " + role_str)
    messages = [{"role": "system", "content": role_str}]
    
    resp = client.chat.completions.create(model="gpt-4", messages=messages)
    return jsonify({"status": "success", "full_response": resp.to_json()})

@app.route('/chat', methods=['POST'])
def chat():
    global messages
    data = request.json
    user_input = data.get('message', '')
    
    messages.append({"role": "user", "content": user_input})
    resp = client.chat.completions.create(model="gpt-4", messages=messages)
    reply = resp.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    
    return jsonify({
        "reply": reply,
        "tokens_used": resp.usage.prompt_tokens
    })

@app.route('/reset', methods=['POST'])
def reset():
    global messages
    messages = []
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
