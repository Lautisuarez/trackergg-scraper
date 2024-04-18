from utils.config import settings as s
import discord
from discord.ext import commands

def main():
    COGS = ["services.discord.pingCog", "services.discord.scraper"]

    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix=">", intents=intents)

    @client.event
    async def on_ready():
        for cog in COGS:
            try:
                print(f"Loading cog {cog}")
                await client.load_extension(cog)
                print(f"Loaded cog {cog}")
            except Exception as e:
                print(f"Error loading cog {cog}: {e}")
        print("Bot is ready...")

    client.run(s.DS_TOKEN)

if __name__ == "__main__":
    main()