import discord
from discord.ext import commands
import os
import asyncio
import logging

# Setup proper logging
discord.utils.setup_logging(level=logging.INFO)
logger = logging.getLogger('discord')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Operational and logged in as {bot.user}")

async def main():
    async with bot:
        try:
            await bot.load_extension("cogs.craft_cog")
            logger.info("Successfully loaded extension: cogs.craft_cog")
        except Exception as e:
            logger.error(f"Failed to load extension cogs.craft_cog: {e}")

        token = os.environ.get("DISCORD_BOT_TOKEN")
        if token:
            await bot.start(token)
        else:
            logger.error("Deployment Failure: DISCORD_BOT_TOKEN environment variable is not set.")

if __name__ == "__main__":
    asyncio.run(main())
