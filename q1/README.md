# Discord MCP Integration

A powerful integration between Discord and MCP (Mission Control Protocol) that enables programmatic control and interaction with Discord channels through MCP tools.

## Overview

This project implements a Discord bot that exposes various Discord functionalities through MCP tools, allowing for seamless interaction with Discord channels and messages through a standardized interface.

## Prerequisites

- Python 3.8 or higher
- Discord Bot Token
- Discord Developer Application with proper intents enabled
- FastMCP library

## Installation

1. Clone the repository
2. Create a virtual environment (recommended)
3. Install dependencies:
   - Using pip: `pip install -r requirements.txt`
   - Using uv: `uv pip install -r requirements.txt`

## Configuration

1. Create a `.env` file in the project root
2. Add your Discord bot token:
   ```
   DISCORD_BOT_TOKEN=your_token_here
   ```

## Running the Application

There are two ways to run the application:

1. **Recommended Method**:
   ```
   python main.py
   ```
   This method provides full functionality with both Discord and MCP services.

2. **Alternative Method (MCP-focused)**:
   ```
   uv run --with fastmcp fastmcp run main.py
   ```
   Note: This method may have limitations with Discord integration.

## Available MCP Tools

The integration provides the following MCP tools for Discord interaction:

1. **send_message**
   - Purpose: Send messages to specific Discord channels
   - Parameters:
     - channel_name: Target channel name
     - content: Message text to send

2. **get_messages**
   - Purpose: Retrieve recent messages from a channel
   - Parameters:
     - channel_name: Target channel name
     - limit: Number of messages to retrieve (default: 50)

3. **get_channel_info**
   - Purpose: Fetch metadata about a Discord channel
   - Parameters:
     - channel_name: Target channel name

4. **search_messages**
   - Purpose: Search for messages containing specific text
   - Parameters:
     - channel_name: Target channel name
     - query: Text to search for

5. **moderate_content**
   - Purpose: Delete specific messages (moderation)
   - Parameters:
     - channel_name: Target channel name
     - message_id: ID of the message to delete

## Features

- Real-time Discord integration
- Asynchronous operation
- Comprehensive channel management
- Message history retrieval
- Content moderation capabilities
- Search functionality
- Channel metadata access

## Project Structure

- `main.py`: Entry point and MCP tool definitions
- `discord_client.py`: Discord client implementation
- `requirements.txt`: Project dependencies
- `pyproject.toml`: Project configuration
- `.env`: Environment variables (not tracked in git)

## Error Handling

The application includes robust error handling for:
- Channel not found scenarios
- Authentication failures
- Message deletion errors
- Invalid channel names
- Connection issues

## Best Practices

1. Always use environment variables for sensitive data
2. Ensure proper Discord bot permissions
3. Handle rate limits appropriately
4. Monitor bot status through console output
5. Check channel names carefully before operations

## Limitations

- Message search is limited to the last 100 messages
- Channel operations require exact channel name matches
- Bot requires appropriate Discord permissions
- Some features may be limited by Discord API restrictions

## Troubleshooting

Common issues and solutions:

1. Bot Not Connecting:
   - Verify bot token in .env file
   - Check Discord Developer Portal settings
   - Ensure proper intents are enabled

2. Channel Not Found:
   - Verify exact channel names
   - Check bot's server access
   - Ensure proper capitalization

3. Permission Issues:
   - Review bot's role permissions
   - Check channel-specific permissions
   - Verify bot's position in role hierarchy

## Support

For issues and feature requests, please create an issue in the repository.

## Security Considerations

- Never commit .env files
- Regularly rotate bot tokens
- Implement proper permission checks
- Monitor bot activity
- Restrict moderation commands appropriately

## License

[Specify your license here]
