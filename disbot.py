if __name__ == "__main__":
    exit()

import discord

from main import DISCORD_IDS, DISCORD_TOKEN


discord_bot = discord.Client()


@discord_bot.event
async def on_ready():
    channel = discord_bot.get_channel(DISCORD_IDS[1])
    await channel.send(send_text)
    exit()

discord_bot.run(DISCORD_TOKEN)