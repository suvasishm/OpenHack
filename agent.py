import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import MessageRole, FilePurpose, FunctionTool, FileSearchTool, ToolSet
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Initialize the AI Project client
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_CONNECTION_STRING"],
    credential=DefaultAzureCredential()
)

# Create an agent using GPT-4o model
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="LouMalnati"
)
print(f"Created agent, ID: {agent.id}")

# Create a thread for the conversation
thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

# Start the interactive message loop
print("\nChat with your pizza ordering agent (type 'exit' or 'quit' to end):")
while True:
    # Get the user input
    user_input = input("You: ")

    # Break out of the loop
    if user_input.lower() in ["exit", "quit"]:
        break

    # Add a message to the thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER, 
        content=user_input
    )

    # Create and process an agent run
    run = project_client.agents.runs.create_and_process(
        thread_id=thread.id, 
        agent_id=agent.id
    )    

    # Fetch all messages from the thread
    messages = project_client.agents.messages.list(thread_id=thread.id)  
    first_message = next(iter(messages), None) 
    if first_message: 
        print("Agent:", next((item["text"]["value"] for item in first_message.content if item.get("type") == "text"), ""))


# clean up by deleting the agent
project_client.agents.delete_agent(agent.id)
print("Deleted agent")
