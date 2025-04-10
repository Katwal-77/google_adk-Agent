from agent import root_agent

def main():
    print("Weather and Time Agent")
    print("Type 'exit' to quit")
    print("Example queries:")
    print("- What's the weather in New York?")
    print("- What time is it in New York?")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break

        # Use the agent to generate a response
        response = root_agent.generate_content(user_input)
        print(f"\nAgent: {response.text}")

if __name__ == "__main__":
    main()
