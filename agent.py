import os, time, json
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import MessageRole, FilePurpose, FunctionTool, FileSearchTool
from dotenv import load_dotenv
from typing import Dict, Any

def calculate_simple_pizza_order(adults: int, children: int = 0) -> Dict[str, Any]:
    """
    Calculate the number of large pizzas needed based on the number of adults and children.
    One large pizza serves 2 adults and 2 children.
    
    Args:
        adults (int): Number of adults
        children (int): Number of children (optional)
    
    Returns:
        dict: Dictionary containing the recommended number of pizzas and explanation
    """
    # Convert children to adult equivalents (1 child = 0.5 adult portions)
    total_adult_equivalents = adults + (children * 0.5)
    
    # Calculate pizzas needed (1 pizza serves 2 adult equivalents)
    pizzas_needed = max(1, round(total_adult_equivalents / 2))
    
    return {
        "pizzas_needed": pizzas_needed,
        "size": "large",
        "serves": {
            "adults": adults,
            "children": children
        },
        "explanation": f"For {adults} adults and {children} children, you need {pizzas_needed} large pizza(s). "
                      f"Each large pizza serves approximately 2 adults or 4 children."
    }


# Load environment variables
load_dotenv(override=True)

# Initialize the AI Project client
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_CONNECTION_STRING"],
    credential=DefaultAzureCredential(),
    mcp_endpoint="https://ca-pizza-mcp-dpp3dr2tbvkje.mangobeach-6a5c7f24.northeurope.azurecontainerapps.io/sse"
)

# Read the system prompt
with open('prompts/system.prompt.md', 'r') as file:
    system_prompt = file.read()

# Upload file and create vector store
file = project_client.agents.files.upload(file_path="./knowledge/contoso-stores_v1/contoso_pizza_chicago.md", purpose=FilePurpose.AGENTS)
vector_store = project_client.agents.vector_stores.create_and_poll(file_ids=[file.id], name="chicago_location_vectorstore")

# Create search tool
file_search = FileSearchTool(vector_store_ids=[vector_store.id])

# Define user functions
user_functions = {calculate_simple_pizza_order}
functions = FunctionTool(functions=user_functions)

# Delete existing agent if it exists
agent_name = "ContosoBot-Pizza-Agent-v1"

# Create a new agent using GPT-4o model with system prompt
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name=agent_name,
    instructions=system_prompt,
    tools=[*functions.definitions, *file_search.definitions],
    tool_resources=file_search.resources,
)
print(f"Created new agent: {agent_name} (ID: {agent.id})")

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
    print(f"Created message, ID: {message['id']}")

    run = project_client.agents.runs.create_and_process(
        thread_id=thread.id, 
        agent_id=agent.id
    )
    print(f"Created run, ID: {run.id}")

    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(1)
        run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)

        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []
            for tool_call in tool_calls:
                if tool_call.function.name == "calculate_simple_pizza_order":
                    args = json.loads(tool_call.function.arguments)
                    output = calculate_simple_pizza_order(**args)
                    tool_outputs.append({"tool_call_id": tool_call.id, "output": json.dumps(output)})
            project_client.agents.runs.submit_tool_outputs(thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs)

    print(f"Run completed with status: {run.status}")

    messages = project_client.agents.messages.list(thread_id=thread.id)  
    first_message = next(iter(messages), None) 
    if first_message: 
        print(next((item["text"]["value"] for item in first_message.content if item.get("type") == "text"), ""))

# clean up by deleting the agent
project_client.agents.vector_stores.delete(vector_store.id)
project_client.agents.files.delete(file_id=file.id)
project_client.agents.delete_agent(agent.id)
print("Deleted agent")
