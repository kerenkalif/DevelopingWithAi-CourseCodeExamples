from flask import Flask, request, jsonify, session
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Required for sessions
CORS(app, supports_credentials=True)  # Important: allow credentials for sessions

client = OpenAI()

@app.route('/set_role', methods=['POST'])
def set_role():
    data = request.json
    role_str = data.get('role', 'You are a helpful assistant.')
    role_str += " You are not allowed to answer anything that is not part of your profession."
    
    print(f"Session {session.sid if hasattr(session, 'sid') else 'new'} - The role: {role_str}")
    
    session['messages'] = [{"role": "system", "content": role_str}]
    
    resp = client.chat.completions.create(model="gpt-4", messages=session['messages'])
    return jsonify({"status": "success", "full_response": resp.to_json()})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    
    # Get this session's messages, or create default
    if 'messages' not in session:
        session['messages'] = [{"role": "system", "content": "You are a helpful assistant."}]
    
    messages = session['messages']
    messages.append({"role": "user", "content": user_input})
    
    resp = client.chat.completions.create(model="gpt-4", messages=messages)
    reply = resp.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    
    # Save back to session
    session['messages'] = messages
    
    print(f"Session - Tokens used: {resp.usage.prompt_tokens}")
    
    return jsonify({
        "reply": reply,
        "tokens_used": resp.usage.prompt_tokens
    })

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('messages', None)
    print("Session - Chat reset")
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
