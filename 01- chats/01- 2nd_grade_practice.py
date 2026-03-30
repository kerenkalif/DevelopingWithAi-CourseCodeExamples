from secret_key import antropic_key
from anthropic import Anthropic

client = Anthropic(api_key=antropic_key)

with open("role_2nd_grade_math_teacher.txt", "r", encoding="utf-8") as f:
    role_str = f.read()

messages = []

while True:
    messages.append({
        "role": "user",
        "content": (
            "Give exactly ONE NEW long addition or subtraction exercise for a 2nd grade student. "
            "It must be different from all previous exercises in this conversation. "
            "Show only the exercise. "
            "Do not add explanations."
        )
    })

    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=messages,
        system=role_str
    )

    reply = resp.content[0].text.strip()
    messages.append({"role": "assistant", "content": reply})
    print(reply)

    user_input = input("Enter your answer: ").strip()

    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye")
        break

    if not user_input:
        print("Please enter an answer.")
        continue

    messages.append({
        "role": "user",
        "content": f"The student's answer is: {user_input}. Check if it is correct and give feedback."
    })

    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=messages,
        system=role_str
    )

    reply = resp.content[0].text.strip()
    messages.append({"role": "assistant", "content": reply})
    print(f"Kalifi Teacher says:\n{reply}")