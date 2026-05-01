from google import genai
from google.genai.errors import ClientError

client = genai.Client()
model="gemini-2.5-flash"

def extract_root_cause(error: Exception) -> str:
    msg = str(error)

    if "RESOURCE_EXHAUSTED" in msg or "quota" in msg.lower():
        if "limit: 0" in msg:
            return "⚠️ No available quota for this Gemini model in the current project."
        return "⚠️ Gemini API quota exceeded. Please wait or check billing/quota settings."

    if "API key" in msg or "permission" in msg.lower() or "PERMISSION_DENIED" in msg:
        return "❌ Invalid API key or missing API permissions."

    if "NOT_FOUND" in msg or "not found" in msg.lower():
        return "❌ The selected model is not available for this account or API version."

    if "UNAUTHENTICATED" in msg or "authentication" in msg.lower():
        return "❌ Authentication failed."

    return "⚠️ API request failed."

def safe_generate(prompt):
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        return {"ok": True, "data": response.text}

    except ClientError as e:
        return {"ok": False, "error": extract_root_cause(e)}

    except Exception:
        return {"ok": False, "error": "⚠️ Unexpected error occurred."}


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

    question = result["data"]
    return question

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