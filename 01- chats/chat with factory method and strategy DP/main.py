from llm_factory import LLMClientFactory

def main():
    available = ", ".join(LLMClientFactory._registry.keys())
    print(f"Available providers: {available}")
    provider = input("Choose a provider: ").strip()

    try:
        strategy = LLMClientFactory.create(provider)
    except ValueError as e:
        print(e)
        return  

    role_str = input("What role do you want to give the AI? ")
    strategy.set_system_role(role_str)

    print(f"\nChat started with {provider}. Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            break

        response = strategy.send_message(user_input)
        print(f"AI: {response.reply}")
        print(f"[Input tokens: {response.input_tokens} | Output tokens: {response.output_tokens}]\n")


if __name__ == "__main__":
    main()
