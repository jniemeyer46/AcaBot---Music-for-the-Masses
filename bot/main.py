# General Imports
from discord import Client, opus
import asyncio
import itertools
import threading
import random
import time
import youtube_dl

# Local File Imports
from _musicbot import MusicBot
from _configs import Configs

''' SETUP REQUIRED FOR THE BOT '''
# Discord Client Connection
discordClient = Client()
# Configs
configs = Configs()


@discordClient.event
async def on_ready():
    print('%s has logged into the dicord channel' % discordClient.user.name)


@discordClient.event
async def on_message(message):
    if message.content.startswith(configs.commandPrefix):
        message.content = message.content.lower()
        msg = message.content[1:].split(' ')

        '''----- Owner Commands -----'''
        if msg[0] in configs.OwnerCommands and str(message.author.id) == configs.ownerID:
            # shutdown the bot and clear the chat from all bot requests and responses
            if msg[0] == 'shutdown':
                await acaBot.shutdown(message)

        '''----- Trusted User Commands -----'''
        if msg[0] in configs.TrustedCommands and str(message.author.top_role) in configs.rolePermissions:
            if msg[0] == 'deletenp':
                pass
            elif msg[0] == 'disconnect':
                await acaBot.disconnect(message)
            elif msg[0] == 'pause':
                pass
            elif msg[0] == 'playlist':
                await acaBot.playlist(message)
            elif msg[0] == 'store':
                await acaBot.store(message)
            elif msg[0] == 'summon':
                await acaBot.summon(message)
            elif msg[0] == 'volume':
                await acaBot.setVolume(message)

        '''----- General Commands -----'''
        if msg[0] in configs.GeneralCommands:
            # Clean the discord chat of all previous bot requests and responses
            if msg[0] == 'clean':
                await acaBot.cleanChat(message)
            elif msg[0] == 'test':
                await acaBot._voice.disconnect()


if __name__ == '__main__':
    ''' BOT STARTS HERE '''
    acaBot = MusicBot(discordClient, configs)

    discordClient.run(configs.botToken)
