import os

import discord
import dotenv

from locallib import BotWorkerTask
from locallib import Config
from locallib import DatabaseAdapter
from locallib import ShikiClient

dotenv.load_dotenv()
client = discord.Client()

ADMIN_DISCORD_ID = os.getenv('ADMIN_DISCORD_ID')
DB_ADAPTER = DatabaseAdapter()
SHIKI_CLIENT = ShikiClient()
CFG = Config(DB_ADAPTER, client)
BOT_WORKER = BotWorkerTask(CFG, client, SHIKI_CLIENT)


@client.event
async def on_ready():
    global DB_ADAPTER
    global CFG
    try:
        DB_ADAPTER.connect()
        CFG.load()
        if CFG.status != discord.Status.online:
            await client.change_presence(status=discord.Status.online)
        if CFG.activity.type != discord.ActivityType.unknown:
            await client.change_presence(activity=CFG.activity)
    except Exception as e:
        print('Error during initialization')
        print(e)
        await client.close()
        print('Bot not started')
    print('Bot ready')


@client.event
async def on_message(message: discord.Message):
    global CFG
    try:
        if message.author == client.user:
            return
        # region jokes
        if message.content.strip() in CFG.jokes and len(CFG.jokes) > 0:
            await message.channel.send(CFG.jokes[message.content.strip()],
                                       reference=message)
            return
        # endregion jokes
        if message.content.startswith(CFG.prefix):
            print(message.author, message.channel.id, message.content)
            args = message.content[len(CFG.prefix):].split()
            if args[0] == 'help':
                await command_help(message)
            elif args[0] == 'config':
                await command_config(message, args)
            elif args[0] == 'usechannel':
                await command_usechannel(message)
            elif args[0] == 'worker':
                await command_worker(message, args)
            elif args[0] == 'github':
                await command_github(message)
    except Exception as e:
        print(e)


# region commands

async def command_worker(message: discord.Message, args: list[str]):
    global BOT_WORKER
    if len(args) > 1:
        if args[1] == 'start':
            BOT_WORKER.start()
        elif args[1] == 'stop':
            BOT_WORKER.stop()
    await message.channel.send("Worker running" if BOT_WORKER.is_running()
                               else "Worker stopped", reference=message)


async def command_help(message: discord.Message):
    response = """
`config`: show config
`config users <add/remove> <usernames>`: add or remove users
`config users clear`: truncate users
`config interval <time in seconds>`: interval between requests
`config prefix <prefix>`: command prefix
`config status <online/invisible/idle/dnd>`: set bot status
`config activity <playing/streaming/listening/watching> <text>`: set bot activity
`config activity clear`: remove bot activity
`config jokes add "<message>" "<reaction>"`: add joke
`config jokes remove <jokes>`: remove jokes (jokes must be quoted)
`config jokes clear`: remove all jokes
`usechannel`: use this channel for notifications
`worker`: get worker status
`worker <start/stop>`: start/stop worker
`github`: get link to the source code
    """
    await message.channel.send(response, reference=message)


async def command_config(message: discord.Message, args: list[str]):
    global CFG
    global BOT_WORKER
    if len(args) > 1:
        if args[1] == 'users' and len(args) > 2:
            if args[2] == 'add':
                CFG.add_users(args[3:])
            elif args[2] == 'clear':
                CFG.truncate_users()
            elif args[2] == 'remove':
                CFG.delete_users(args[3:])
        elif args[1] == 'jokes' and len(args) > 2:
            if args[2] == 'add' and len(args) > 4:
                substrings = message.content.split('"')
                if len(substrings) < 4:
                    return
                mess = substrings[1]
                react = substrings[3]
                if mess and react:
                    CFG.add_joke(mess, react)
            elif args[2] == 'clear':
                CFG.truncate_jokes()
            elif args[2] == 'remove':
                substrings = message.content.split('"')

                CFG.delete_jokes(substrings[1::2])
        elif args[1] == 'status' and len(args) == 3:
            try:
                status = discord.Status(args[2])
                if status != discord.Status.online:
                    CFG.activity = discord.Activity()
                await client.change_presence(status=status)
                CFG.status = status
            except ValueError as e:
                pass
        elif args[1] == 'interval' and len(args) == 3:
            try:
                interval = int(args[2])
                if BOT_WORKER.is_running():
                    BOT_WORKER.restart()
                CFG.long_pooling_interval = interval
            except ValueError as e:
                pass
        elif args[1] == 'prefix' and len(args) == 3:
            CFG.prefix = args[2]
        elif args[1] == 'activity':
            if len(args) == 3:
                activity = discord.Activity()
                await client.change_presence(activity=activity)
                CFG.activity = activity
            elif len(args) > 3:
                activity_text = ' '.join(args[3:])
                activity_type = discord.ActivityType.unknown
                if args[2] == 'playing':
                    activity_type = discord.ActivityType.playing
                elif args[2] == 'streaming':
                    activity_type = discord.ActivityType.streaming
                elif args[2] == 'listening':
                    activity_type = discord.ActivityType.listening
                elif args[2] == 'watching':
                    activity_type = discord.ActivityType.watching
                activity = discord.Activity()
                if activity_type != discord.ActivityType.unknown:
                    activity = discord.Activity(name=activity_text,
                                                type=activity_type)
                    CFG.status = discord.Status.online
                await client.change_presence(activity=activity)
                CFG.activity = activity
    await message.channel.send(str(CFG), reference=message)


async def command_usechannel(message: discord.Message):
    await message.channel.send("Okay. This channel", reference=message)
    CFG.message_channel = message.channel


async def command_github(message: discord.Message):
    url = 'https://github.com/thisUsernameIsAlredyTaken/ShikimoriDiscordBot'
    await message.channel.send(url, reference=message)

# endregion commands


client.run(os.getenv('DISCORD_BOT_TOKEN'))
