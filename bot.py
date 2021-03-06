"""Module for running the DiscordBot"""
import sys
import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=">", intents=intents)


@client.event
async def on_ready():
    """Signals the 'bot is ready' event"""

    print("[*] Bot is ready")


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


@client.command()
async def ping(ctx):
    """Pings the latency between the bot and the server"""

    await ctx.send(f"time={round(client.latency * 1000, 1)} ms")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prod", action="store_true", required=False,
        help="specify production lifecycle to automatically "\
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
