from Multi_agent_tool.agent import root_agent

# Start a conversation with the agent
response = root_agent.start_chat()
print("Agent started. Type 'exit' to quit.")

while True:
    user_input = input("> ")
    if user_input.lower() == 'exit':
        break
    
    response = root_agent.send_message(user_input)
    print(response.text)
