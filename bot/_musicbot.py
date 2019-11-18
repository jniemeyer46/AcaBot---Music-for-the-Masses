import asyncio
import os.path
import random
import youtube_dl
from math import floor

from _configs import Configs


class MusicBot:
    def __init__(self, client=None, configs=None):
        self._autoplaylistName = configs.autoplaylistName
        self._volume = configs.volume
        self._pause = configs.pauseFlag
        self._client = client
        self._configs = configs

    '''----- Setters and Getters -----'''
    # Getters
    async def getVolume(self):
        return self._volume

    # Setters
    async def setVolume(self, newVolume):
        self._volume = newVolume

    '''----- Functionality -----'''
    # Owner Commands
    async def restart():
        pass

    async def shutdown():
        pass

    # Trusted Commands
    async def deleteNP():
        pass

    async def disconnect():
        pass

    async def pause():
        pass

    async def playlist():
        pass

    async def store():
        pass

    async def summon():
        pass

    # General Commands
    def deleteMessageCheck(self, message):
        return message.content.startswith(self._configs.commandPrefix) or message.author.id == self._client.user.id

    async def cleanChat(self, message):
        deleted = await message.channel.purge(limit=200, check=self.deleteMessageCheck)

    async def help():
        pass

    async def nowPlaying():
        pass

    async def play():
        pass

    async def showQueue():
        pass

    async def skip():
        pass
