import requests

# 🔧 הגדרות Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"  # for weaker pc can use he model 'phi3'


def extract_root_cause(error: Exception) -> str:
    msg = str(error)

    if "Connection refused" in msg or "Failed to establish" in msg:
        return "❌ Ollama is not running. Please start Ollama."

    if "timeout" in msg.lower():
        return "⚠️ The local model is taking too long to respond."

    return "⚠️ Local model error."


def safe_generate(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

        if response.status_code != 200:
            return {"ok": False, "error": f"⚠️ HTTP Error {response.status_code}"}

        data = response.json()
        return {"ok": True, "data": data["response"]}

    except Exception as e:
        return {"ok": False, "error": extract_root_cause(e)}


def generate_question(topic):
    generate_question_prompt = f"""
Create a LeetCode-style coding question in Python about: {topic}.

The question should include:
- Clear problem description
- Function signature
- Example input/output
- Constraints

Do NOT include the solution.
"""

    result = safe_generate(generate_question_prompt)

    if not result["ok"]:
        print("⚠️ Error:", result["error"])
        exit()

    return result["data"]


def evaluate_solution(question, student_code):
    ask_for_review_prompt = f"""
You are a senior Python code reviewer helping a student.

Here is the coding question:
{question}

Here is the student's solution:
{student_code}

Give high-quality feedback:
- Is the approach correct?
- Time complexity
- Strengths
- What should be improved
- Give hints WITHOUT giving full solution
"""

    return safe_generate(ask_for_review_prompt)


# 🧪 שימוש
topic = input("Enter topic: ")

question = generate_question(topic)

print("\n--- Question ---\n")
print(question)

print("\nWrite your solution (end with END):")

lines = []
while True:
    line = input()
    if line.strip() == "END":
        break
    lines.append(line)

student_code = "\n".join(lines)

feedback = evaluate_solution(question, student_code)

print("\n--- Feedback ---\n")

if feedback["ok"]:
    print(feedback["data"])
else:
    print(feedback["error"])