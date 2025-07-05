import os
import asyncio
import warnings
import discord.utils
from dotenv import load_dotenv
from fastmcp import FastMCP
from mcp.client import stdio
from discord_client import DiscordClient

# Suppress all warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", module="discord.*")
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", message=".*'audioop' is deprecated.*")
discord.utils.setup_logging(level=40)  # Only show ERROR level logs

# Load environment variables from .env file (e.g., DISCORD_BOT_TOKEN)
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not DISCORD_TOKEN:
    raise EnvironmentError("DISCORD_BOT_TOKEN not found in environment variables.")

# Initialize the Discord client with the bot token
discord_client = DiscordClient(DISCORD_TOKEN)

# Create a FastMCP app instance
app = FastMCP("Discord MCP")

print("\n=== Starting Discord MCP Server ===\n")

# MCP tool to send a message to a Discord channel
@app.tool()
async def send_message(channel_name: str, content: str):
    """
    Send a message to a Discord channel.

    Args:
        channel_name (str): Name of the target channel.
        content (str): Message text to send.

    Returns:
        discord.Message: The sent message object.
    """
    return await discord_client.send_message(channel_name, content)


# MCP tool to get recent messages from a channel
@app.tool()
async def get_messages(channel_name: str, limit: int = 50):
    """
    Retrieve recent messages from a Discord channel.

    Args:
        channel_name (str): Name of the target channel.
        limit (int): Number of messages to retrieve (default 50).

    Returns:
        List[discord.Message]: List of message objects.
    """
    return await discord_client.get_messages(channel_name, limit)


# MCP tool to fetch channel metadata
@app.tool()
async def get_channel_info(channel_name: str):
    """
    Get metadata about a Discord channel.

    Args:
        channel_name (str): Name of the target channel.

    Returns:
        dict: Channel information.
    """
    return await discord_client.get_channel_info(channel_name)


# MCP tool to search messages in a channel by query string
@app.tool()
async def search_messages(channel_name: str, query: str):
    """
    Search messages in a Discord channel containing the given query.

    Args:
        channel_name (str): Name of the target channel.
        query (str): Text to search for.

    Returns:
        List[discord.Message]: Messages matching the query.
    """
    return await discord_client.search_messages(channel_name, query)


# MCP tool to delete a message (moderation)
@app.tool()
async def moderate_content(channel_name: str, message_id: int):
    """
    Delete a specific message in a Discord channel.

    Args:
        channel_name (str): Name of the target channel.
        message_id (int): ID of the message to delete.

    Returns:
        None
    """
    await discord_client.moderate_content(channel_name, message_id)


# async def main():
#     # Start Discord client as a background task
#     discord_task = asyncio.create_task(discord_client.start())
#     # Start MCP server (assuming app.run() is async, otherwise use asyncio.to_thread)
#     mcp_task = asyncio.create_task(app.run_async())  # If FastMCP supports async run
#     await asyncio.gather(discord_task, mcp_task)

async def main():
    try:
        discord_task = asyncio.create_task(discord_client.start())
        mcp_task = asyncio.create_task(app.run_async())
        await asyncio.gather(discord_task, mcp_task)
    except Exception as e:
        import traceback
        print("=== Exception in main ===")
        traceback.print_exc()
        raise


if __name__ == "__main__":
    asyncio.run(main())
