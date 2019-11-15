# General Imports
from discord import Client, opus
import asyncio
import itertools
import threading
import random
import time

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
        msg = message.content.lower()
        msg = msg[1:].split(' ')

        '''----- Owner Commands -----'''
        if msg[0] in configs.OwnerCommands and str(message.author.id) == configs.ownerID:
            # Restart the bot and clear the chat from all bot requests and responses
            if msg[0] == 'restart':
                await acaBot.restart()
            # shutdown the bot and clear the chat from all bot requests and responses
            if msg[0] == 'shutdown':
                pass

        '''----- Trusted User Commands -----'''
        if msg[0] in configs.TrustedCommands and str(message.author.top_role) in configs.rolePermissions:
            pass

        '''----- General Commands -----'''
        if msg[0] in configs.GeneralCommands:
            # Clean the discord chat of all previous bot requests and responses
            if msg[0] == 'clean':
                await acaBot.cleanChat(message)


if __name__ == '__main__':
    ''' BOT STARTS HERE '''

    while configs.restartFlag is True:
        acaBot = MusicBot(discordClient, configs)

        discordClient.run(configs.botToken)
