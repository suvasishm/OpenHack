# Contoso Pizza Ordering Agent

> **Disclaimer**: This project was developed as part of Microsoft Open Hack, an immersive and challenge-based learning experience. It serves as a hands-on demonstration of Azure AI capabilities and is intended for educational purposes.

This project implements an AI-powered pizza ordering agent for Contoso Pizza, built using Azure AI Projects and Model Context Protocol (MCP). The agent assists customers in finding store locations, placing orders, and managing their pizza delivery/pickup experience.

## Features

- Interactive chat-based interface
- Store location lookup and information retrieval
- Pizza order calculation and recommendations
- Integration with Contoso Pizza's MCP server
- Vector-based store information search
- Automated order processing

## Prerequisites

- Python 3.x
- Azure Account with proper credentials
- Required Python packages (listed in dependencies section)
- Environment variables properly configured

## Setup

1. Clone the repository
2. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install azure-ai-projects azure-identity azure-ai-agents python-dotenv
   ```

4. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your Azure Project connection string:
     ```
     PROJECT_CONNECTION_STRING=your_connection_string_here
     ```

## Project Structure

```
├── agent.py               # Main agent implementation
├── knowledge/            # Store information and data
│   └── contoso-stores_v1/  # Store location details
├── prompts/             # System prompts and instructions
│   └── system.prompt.md   # Agent system instructions
└── README.md            # Project documentation
```

## Features

### Store Information
- Location details
- Operating hours
- Available services
- Specialties and features

### Order Management
- Pizza size recommendations
- Customizable orders
- Delivery/pickup options
- Order tracking

### AI Capabilities
- Natural language understanding
- Context-aware conversations
- Smart recommendations
- Location-based services

## Functions

### calculate_simple_pizza_order
Calculates recommended pizza quantities based on group size:
- Input: Number of adults and children
- Output: Recommended number of pizzas and sizing explanation

## Usage

1. Start the agent:
   ```bash
   python agent.py
   ```

2. Interact with the agent through the chat interface:
   - Provide your name when asked
   - Select a store location
   - Place your order
   - Choose delivery or pickup
   - Confirm your order

3. To exit:
   - Type 'exit' or 'quit'
   - The agent will clean up resources automatically

## MCP Server Integration

The agent integrates with Contoso Pizza's MCP server for:
- Menu information
- Order processing
- Store data
- Inventory management

Available MCP tools:
- get_pizzas
- get_pizza_by_id
- get_toppings
- get_topping_by_id
- get_topping_categories
- get_orders
- get_order_by_id
- place_order
- delete_order_by_id

## Error Handling

The agent includes robust error handling for:
- Function execution failures
- MCP server communication issues
- Invalid input handling
- Connection problems

## Security

- Uses Azure DefaultAzureCredential for authentication
- Secure environment variable handling
- Protected MCP server communication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Insert appropriate license information]

## Support

For support, please contact [Insert contact information]