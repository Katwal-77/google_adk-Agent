from agent import root_agent

# Print the type and available methods/attributes
print(f"Agent type: {type(root_agent)}")
print("\nAvailable methods and attributes:")
for attr in dir(root_agent):
    if not attr.startswith('_'):  # Skip private/internal attributes
        print(f"- {attr}")

# Try to get help on the agent
print("\nHelp on agent:")
try:
    help(root_agent)
except Exception as e:
    print(f"Error getting help: {e}")
