"""Module for running the FridayBot."""
import sys
import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='friday ', intents=intents)


@client.event
async def on_ready():
    """Signals the 'bot is ready' event."""

    print('Bot is ready.')


@client.event
async def on_member_join(member):
    """Announces that a member has joined the server."""

    target_channel = 'test'
    for channel in member.guild.channels:
        if str(channel) == target_channel:
            embed = discord.Embed(color=0x4a3d9a)
            embed.add_field(name="Welcome", value=f"{member.name} has joined {member.guild.name}", inline=False)
            await channel.send(embed=embed)
            break
    else:
        print(f'Could not find channel {target_channel}')


if __name__ == '__main__':
    try:
        token = os.environ['FRIDAY_TOKEN']
    except KeyError:
        print('[!] Missing FRIDAY_TOKEN environment variable.')
        sys.exit(1)
    else:
        client.run(token)
