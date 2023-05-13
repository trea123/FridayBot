"""Module for running the DiscordBot"""

import os
import sys
import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.reactions = True

client = commands.Bot(command_prefix="!", intents=intents)

# raw_template = open('graphics_template.csv', 'r')
# template = raw_template.read()


@client.event
async def on_ready():
    """Signals the 'bot is ready' event"""

    print("[*] Bot is ready")
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.event
async def on_member_join(member):
    """Announces that a member has joined the server"""

    target_channel = "join-leave"
    for channel in member.guild.channels:
        if str(channel) == target_channel:
            embed = discord.Embed(color=0x4a3d9a)
            embed.add_field(name="Welcome", value=f"{member.name} has joined {member.guild.name}", inline=False)
            await channel.send(embed=embed)
            break
    else:
        print(f"Could not find channel {target_channel}")


@client.event
async def on_member_remove(member):
    """Announces that a member has left the server"""

    target_channel = "join-leave"
    for channel in member.guild.channels:
        if str(channel) == target_channel:
            embed = discord.Embed(color=0x4a3d9a)
            embed.add_field(name="Goodbye", value=f"{member.name} left {member.guild.name}", inline=False)
            await channel.send(embed=embed)
            break
    else:
        print(f"Could not find channel {target_channel}")


@client.event
async def on_command_completion(ctx):
    target_channel = "mod-log"
    for channel in ctx.guild.channels:
        if str(channel) == target_channel:
            await channel.send(f"{ctx.author.name}, has used the command '{ctx.command.name}'")


@client.command()
async def ping(ctx):
    """Pings the latency between the bot and the server"""

    await ctx.send(f"time={round(client.latency * 1000, 1)} ms")


@client.command()
async def create_channel(ctx):
    """Creates a private channel only viewed by the creator of channel and owner of server"""
    channel_name = ctx.author.name
    await ctx.guild.create_text_channel(f"{channel_name}'s channel")
    await ctx.send(f"A new channel called {channel_name} was made")
    


@client.command()
async def create(ctx):
    while True:
        await ctx.guild.create_text_channel(f"test")


@client.command()
async def prune(ctx):
    guild = ctx.guild
    for channel in guild.channels:
        await channel.delete()
        await ctx.send('channel successfully deleted.')


@client.command()
async def give_member_list(ctx):
    """Displays a list of all members in the server"""

    member_list = "\n".join([member.name for member in ctx.guild.members])
    await ctx.send(f"Here is a list of all members in this server:\n{member_list}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prod", action="store_true", required=False,
        help="specify production lifecycle to automatically "
             "load bot token from system configuration"
    )
    args = parser.parse_args()

    if args.prod is True:
        prod_config = "/etc/DiscordBot/token.txt"
        with open(prod_config, "r") as file:
            token = file.read().strip()
    else:
        try:
            token = os.environ['BOT_TOKEN']
        except KeyError:
            print("[!] Missing BOT_TOKEN environment variable")
            sys.exit(1)

    client.run(token)
