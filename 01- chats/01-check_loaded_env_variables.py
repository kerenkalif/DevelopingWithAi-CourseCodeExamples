import os
print(f"ANTHROPIC_API_KEY from system: {os.environ.get('ANTHROPIC_API_KEY')}")
print(f"OPENAI_API_KEY from system: {os.environ.get('OPENAI_API_KEY')}")
print(f"GOOGLE_API_KEY from system: {os.environ.get('GOOGLE_API_KEY')}")

for key, value in os.environ.items():
    print(f"{key}: {value}")