import asyncio
import os.path
import random
import youtube_dl
from math import floor

from _config import Configs

class MusicBot:
    def __init__(self, client=None, message=None, configs=None):
        self._autoplaylistName = configs.autoplaylistName
        self._volume = configs.volume
        self._pause = configs.pause

    '''----- Setters and Getters -----'''
    # Getters
    async def getVolume(self):
        return self._volume

    # Setters
    async def setVolume(self, newVolume):
        self._volume = newVolume


if __name__ == '__main__':
    testConfig = Configs()
    musicBot = MusicBot(None, None, testConfig)
    print(musicBot.getVolume())
