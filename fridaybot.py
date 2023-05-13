"""Module for running the DiscordBot"""
import json
import logging
import os
import sys
import discord
from discord.ext import commands

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s [%(levelname)s] (%(name)s) %(message)s",
                    handlers=[logging.FileHandler("debug.log", mode="a"),
                              logging.StreamHandler(sys.stdout)])

project_path = os.path.abspath(__file__)
project_service = project_path.split(os.path.sep)[-1].split(".")[0]
project_dir = os.path.dirname(project_path)
project_name = project_dir.split(os.path.sep)[-1]

logger = logging.getLogger(project_service)

PROD_FILE = f"/etc/{project_name}/token.txt"
DEV_FILE = f"{project_dir}/.token.txt"

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.reactions = True

client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    """Signals the "bot is ready" event"""

    logger.info("Bot is ready")
    logger.info(f"Logged in as {client.user} (ID: {client.user.id})")
    logger.info("-" * 60)


@client.event
async def on_member_join(member):
    """Announces that a member has joined the server"""

    target_channel = "join-leave"
    for channel in member.guild.channels:
        if str(channel) == target_channel:
            embed = discord.Embed(color=0x4a3d9a)
            embed.add_field(name="Welcome", value=f"{member.name} has joined {member.guild.name}", inline=False)
            logger.info(f"Member {member.name!r} has joined the server.")
            await channel.send(embed=embed)
            break
    else:
        logger.info(f"Could not find channel {target_channel!r}")


@client.event
async def on_member_remove(member):
    """Announces that a member has left the server"""

    target_channel = "join-leave"
    for channel in member.guild.channels:
        if str(channel) == target_channel:
            embed = discord.Embed(color=0x4a3d9a)
            embed.add_field(name="Goodbye", value=f"{member.name} left {member.guild.name}", inline=False)
            logger.info(f"Member {member.name!r} has left the server.")
            await channel.send(embed=embed)
            break
    else:
        logger.info(f"Could not find channel {target_channel}")


@client.event
async def on_command_completion(ctx):
    target_channel = "mod-log"
    for channel in ctx.guild.channels:
        if str(channel) == target_channel:
            message = f"User: {ctx.author.name!r} has used the command {ctx.command.name!r}"
            logger.info(message)
            await channel.send(message)


@client.command()
async def ping(ctx):
    """Pings the latency between the bot and the server"""

    message = f"Time: {round(client.latency * 1000, 1)} ms"
    logger.info(message)
    await ctx.send(message)


@client.command()
async def create_channel(ctx):
    """Creates a private channel only viewed by the creator of channel and owner of server"""
    channel_name = ctx.author.name

    message = f"Creating new channel {channel_name!r}"
    logger.info(message)
    await ctx.guild.create_text_channel(channel_name)

    message = message.replace("Creating", "Created")
    logger.info(message)
    await ctx.send(message)


@client.command()
async def prune(ctx):
    guild = ctx.guild
    for channel in guild.channels:
        pre_message = f"Attempting to delete {channel!r}"
        logger.debug(pre_message)
        await channel.delete()

        post_message = f"Channel {channel} successfully deleted."
        logger.info(post_message)
        await ctx.send(post_message)


@client.command()
async def give_member_list(ctx):
    """Displays a list of all members in the server"""

    member_names = [member.name for member in ctx.guild.members]
    logger.debug(f"Member list: {member_names}")

    member_names_string = "\n".join(member_names)
    header_message = "Here is a list of all members in this server:"
    message = "\n".join([header_message, member_names_string])
    await ctx.send(message)


def load_token_file(prod: bool = False) -> str:
    """Load the appropriate token from file, based on lifecycle."""

    token_file = PROD_FILE if args.prod else DEV_FILE

    try:
        with open(token_file, "r") as file:
            token = file.read().strip()
    except FileNotFoundError as error:
        logger.error(f"Token file must exist at path {token_file!r}")
        raise error
    except FileNotFoundError as error:
        logger.error("You do not have permission to read "
                     f"token file at path {token_file!r}")
        raise error
    else:
        logger.info("Successfully loaded authentication token.")
        return token


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--prod",
                        action="store_true",
                        required=False,
                        help="specify production lifecycle to automatically"
                             " load bot token from system configuration")
    args = parser.parse_args()

    token = load_token_file(prod=args.prod)

    client.run(token)

