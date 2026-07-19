import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Operational and logged in as {bot.user}")

async def main():
    async with bot:
        await bot.load_extension("cogs.craft_cog")
        token = os.environ.get("DISCORD_BOT_TOKEN")
        if token:
            await bot.start(token)
        else:
            print("Deployment Failure: DISCORD_BOT_TOKEN environment variable is not set.")

if __name__ == "__main__":
    asyncio.run(main())
