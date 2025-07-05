import discord
import asyncio

class DiscordClient:
    """
    DiscordClient wraps discord.py Client to provide async methods
    for interacting with Discord channels and messages.
    """

    def __init__(self, token: str):
        """
        Initialize the Discord client with the bot token.

        Args:
            token (str): Discord bot token for authentication.
        """
        self.token = token
        self.is_ready = asyncio.Event()

        # Enable all intents, including message content intent,
        # required for reading messages.
        intents = discord.Intents.all()

        # Create a discord.Client instance with the specified intents.
        self.client = discord.Client(intents=intents)

        @self.client.event
        async def on_ready():
            print("\n=== Discord Bot Status ===")
            print(f"✓ Bot logged in successfully as: {self.client.user}")
            print(f"\n=== Server Information ===")
            for guild in self.client.guilds:
                print(f"\nServer: {guild.name}")
                print("\nAvailable Channels:")
                text_channels = [ch for ch in guild.channels if str(ch.type) == 'text']
                voice_channels = [ch for ch in guild.channels if str(ch.type) == 'voice']
                
                if text_channels:
                    print("\nText Channels:")
                    for channel in text_channels:
                        print(f"  • {channel.name}")
                
                if voice_channels:
                    print("\nVoice Channels:")
                    for channel in voice_channels:
                        print(f"  • {channel.name}")
                
            print("\n=== Bot Ready for Commands ===\n")
            self.is_ready.set()

    async def start(self):
        """Start the Discord client and wait until ready."""
        print("\n=== Initializing Discord Bot ===")
        await self.client.start(self.token)

    async def close(self):
        """Close the Discord client connection."""
        print("\n=== Shutting down Discord Bot ===")
        await self.client.close()

    async def ensure_ready(self):
        """Wait until the client is ready before proceeding."""
        await self.is_ready.wait()

    async def get_channel_by_name(self, channel_name: str):
        """
        Get a channel by its name.

        Args:
            channel_name (str): Name of the Discord channel.

        Returns:
            discord.Channel: The channel object if found, None otherwise.
        """
        await self.ensure_ready()
        for guild in self.client.guilds:
            for channel in guild.channels:
                if channel.name == channel_name:
                    return channel
        return None

    async def send_message(self, channel_name: str, content: str):
        """
        Send a message to a specific Discord channel.

        Args:
            channel_name (str): Name of the Discord channel.
            content (str): Message content to send.

        Returns:
            discord.Message: The message object sent.
        """
        await self.ensure_ready()
        channel = await self.get_channel_by_name(channel_name)
        if not channel:
            print(f"Debug: Channel {channel_name} not found")
            print(f"Available channels: {[ch.name for ch in self.client.get_all_channels()]}")
            raise ValueError(f"Channel with name {channel_name} not found.")
        return await channel.send(content)

    async def get_messages(self, channel_name: str, limit: int = 50):
        """
        Retrieve message history from a channel.

        Args:
            channel_name (str): Name of the Discord channel.
            limit (int): Number of messages to retrieve (default 50).

        Returns:
            List[discord.Message]: List of message objects.
        """
        channel = await self.get_channel_by_name(channel_name)
        if not channel:
            raise ValueError(f"Channel with name {channel_name} not found.")
        return [msg async for msg in channel.history(limit=limit)]

    async def get_channel_info(self, channel_name: str):
        """
        Fetch metadata about a Discord channel.

        Args:
            channel_name (str): Name of the Discord channel.

        Returns:
            dict: Basic information about the channel.
        """
        channel = await self.get_channel_by_name(channel_name)
        if not channel:
            raise ValueError(f"Channel with name {channel_name} not found.")
        return {
            "id": channel.id,
            "name": channel.name,
            "type": str(channel.type)
        }

    async def search_messages(self, channel_name: str, query: str):
        """
        Search messages in a channel containing the query string.

        Args:
            channel_name (str): Name of the Discord channel.
            query (str): Text to search for within messages.

        Returns:
            List[discord.Message]: Messages containing the query.
        """
        channel = await self.get_channel_by_name(channel_name)
        if not channel:
            raise ValueError(f"Channel with name {channel_name} not found.")
        # Fetch last 100 messages and filter locally
        return [msg async for msg in channel.history(limit=100) if query in msg.content]

    async def moderate_content(self, channel_name: str, message_id: int):
        """
        Delete a specific message from a channel (moderation).

        Args:
            channel_name (str): Name of the Discord channel.
            message_id (int): ID of the message to delete.

        Returns:
            None
        """
        channel = await self.get_channel_by_name(channel_name)
        if not channel:
            raise ValueError(f"Channel with name {channel_name} not found.")
        message = await channel.fetch_message(message_id)
        await message.delete()
