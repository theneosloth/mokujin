#!/usr/bin/env python3
import configurator
import datetime
import logging
import os
import sys

sys.path.insert(1, (os.path.dirname(os.path.dirname(__file__))))
from functools import reduce
from discord.ext import commands
from src import tkfinder
from src.resources import const, embed
from github import Github

base_path = os.path.dirname(__file__)
config = configurator.Configurator(os.path.abspath(os.path.join(base_path, "resources", "config.json")))
prefix = '§'
description = 'The premier Tekken 7 Frame bot, made by Baikonur#4927, continued by Tib#1303'
bot = commands.Bot(command_prefix=prefix, description=description)

# Set logger to log errors
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

logfile_directory = os.path.abspath(os.path.join(base_path, "..", "log"))
logfile_path = logfile_directory + "\\logfile.log"

# Create logfile if not exists
if not os.path.exists(logfile_directory):
    os.makedirs(logfile_directory)

if not os.path.isfile(logfile_path):
    open(logfile_path, "w")

file_handler = logging.FileHandler(logfile_path)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

discord_token = config.read_config()['DISCORD_TOKEN']
feedback_channel_id = config.read_config()['FEEDBACK_CHANNEL_ID']
github_token = config.read_config()['GITHUB_TOKEN']
gh = Github(login_or_token=github_token)

blacklist = ["mirosu#4151"]
emoji_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']


@bot.event
async def on_ready():
    print(datetime.datetime.utcnow().isoformat())
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


def get_latest_commits_messages(numbers: int):
    commits = gh.get_user().get_repo("mokujin").get_commits()
    message = ""
    for i in range(0, numbers, 1):
        new_date = datetime.datetime.strptime(str(commits[i].commit.committer.date), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        message += f'{commits[i].commit.message} on {new_date}\n'
    return message


def get_move_type(original_move: str):
    for k in const.MOVE_TYPES.keys():
        if original_move in const.MOVE_TYPES[k]:
            return k


def do_sum(x1, x2):
    return x1 + "\n" + x2

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.author.id == bot.user.id and user.id != bot.user.id and reaction.count < 3:
        item_index = emoji_list.index(reaction.emoji)
        content = reaction.message.embeds[0].description.replace('\n', '\\n').split("\\n")
        character_name = embed.get_character_name_from_content(content)
        character = tkfinder.get_character_detail(character_name)
        move_list = embed.get_moves_from_content(content)
        move = move_list[item_index]

        result = display_moves_by_input(character, move)
        await reaction.message.channel.send(embed=result)


@bot.event
async def on_message(message):
    """This has the main functionality of the bot. It has a lot of
    things that would be better suited elsewhere but I don't know
    if I'm going to change it."""
    try:
        channel = message.channel
        if str(message.author) in blacklist:
            return

        if message.content == '!server-list':

            serverlist = list(map(lambda x: x.name, bot.guilds))

            serverlist.sort()
            step = 60
            for begin in range(0, len(serverlist), step):
                end = begin + step
                if end > len(serverlist):
                    end = len(serverlist)
                servers = reduce(do_sum, serverlist[begin:end])
                await channel.send(servers)
            msg = "Number of servers in: " + str(len(serverlist))
            await channel.send(msg)

        elif message.content == '!last-updates':
            try:
                messages = get_latest_commits_messages(5)
                print(messages)
                result = embed.success_embed(messages)
            except Exception as e:
                result = embed.error_embed(e)
            await channel.send(embed=result)

        elif message.content.startswith("!auto-delete"):

            if message.author.permissions_in(channel).manage_messages:
                duration = message.content.split(' ', 1)[1]
                if duration.isdigit() or duration == "-1":
                    config.save_auto_delete_duration(channel.id, duration)
                    result = embed.success_embed("Saved")
                else:
                    result = embed.error_embed("Duration needs to be a number in seconds")
            else:
                result = embed.error_embed("You need the permission <manage_messages> to do that")

            await channel.send(embed=result)

        elif message.content.startswith('!clear-messages'):
            # delete x of the bot last messages
            number = int(message.content.split(' ', 1)[1])
            messages = []
            async for m in channel.history(limit=100):
                if m.author == bot.user:
                    messages.append(m)

            to_delete = [message]
            for i in range(number):
                to_delete.append(messages[i])

            await channel.delete_messages(to_delete)

        elif message.content == '!help':
            await channel.send(embed=embed.help_embed())

        elif message.content.startswith('?feedback'):
            user_message = message.content.split(' ', 1)[1]
            server_name = str(message.channel.guild)
            try:
                feedback_channel = bot.get_channel(feedback_channel_id)
                user_message = user_message.replace("\n", "")
                feedback_message = "{}  ;  {} ;   {};\n".format(str(message.author), server_name, user_message)
                await feedback_channel.send(feedback_message)
                result = embed.success_embed("Feedback sent")
            except Exception as e:
                result = embed.error_embed("Feedback couldn't be sent caused by: " + e)

            await channel.send(embed=result)

        elif message.content.startswith('!') and len(message.content[1:].split(' ', 1)) > 1:

            delete_after = config.get_auto_delete_duration(channel.id)
            user_message_list = message.content[1:].split(' ', 1)

            original_name = user_message_list[0].lower()
            original_move = user_message_list[1]

            character_name = tkfinder.correct_character_name(original_name)

            if character_name is not None:
                character = tkfinder.get_character_detail(character_name)
                move_type = get_move_type(original_move.lower())

                if move_type:
                    result = display_moves_by_type(character, move_type)
                else:
                    result = display_moves_by_input(character, original_move)
            else:
                result = embed.error_embed(f'Character {original_name} does not exist.')
                delete_after = 5

            bot_message = await channel.send(embed=result, delete_after=delete_after)
            if embed.MOVE_NOT_FOUND_TITLE == bot_message.embeds[0].title:
                for emoji in emoji_list:
                    await bot_message.add_reaction(emoji)

        await bot.process_commands(message)
    except Exception as e:
        error_msg = f'Message: {message.content}. Error: {e}'
        print(error_msg)
        logger.error(error_msg)

def display_moves_by_type(character, move_type):
    move_list = tkfinder.get_by_move_type(character, move_type)
    result = object
    if len(move_list) < 1:
        result = embed.error_embed(
            'No ' + move_type.lower() + ' for ' + character['proper_name'])
    elif len(move_list) == 1:
        character_move = tkfinder.get_move(character, move_list[0])
        result = embed.move_embed(character, character_move)
    elif len(move_list) > 1:
        result = embed.move_list_embed(character, move_list, move_type)
    return result


def display_moves_by_input(character, original_move):
    character_move = tkfinder.get_move(character, original_move)
    character_name = character["name"]
    if character_move is not None:
        result = embed.move_embed(character, character_move)
    else:
        generic_move = tkfinder.get_generic_move(original_move)
        if generic_move is not None:
            generic_character = tkfinder.get_character_detail("generic")
            result = embed.move_embed(generic_character, generic_move)
        else:
            similar_moves = tkfinder.get_similar_moves(original_move, character_name)
            result = embed.similar_moves_embed(similar_moves, character_name)

    return result


bot.run(discord_token)
