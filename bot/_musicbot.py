import asyncio
import os.path
import random
import time
import youtube_dl
from math import floor

from _configs import Configs


class MusicBot:
    _player = None
    _voice = None

    # Queues
    coolDownQueue = []
    playQueue = []

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
    async def setVoice(self, channel):
        self._voice = await channel.connect()

    async def setVolume(self, message):
        print(message.content)
        # self._volume = newVolume

    '''----- Functionality -----'''
    # Owner Commands
    async def shutdown(self, message):
        # Signoff message
        await message.channel.send(
            'I am going to head out now, I do hope you enjoyed the music!'
        )
        time.sleep(5)

        # If connected to voice, disconnect
        if self._voice:
            await self.disconnect(message)

        # Clean up the chat before shutting down
        await self.cleanChat(message)

        # Logout and close the discord connection
        await self._client.logout()

    # Trusted Commands
    async def deleteNP(self):
        pass

    '''----- Disconnect AcaBot from current voice channel -----'''
    async def disconnect(self, message):
        if self._voice:
            # If there is something playing, stop it and do some cleanup
            if self._voice.is_playing():
                self._voice.stop()
                self._voice.cleanup()

            # Disconnect from voice and set AcaBot's voice channel to None
            await self._voice.disconnect()
            self._voice = None
        else:
            await message.channel.send(
                'AcaBot is not connected to a voice channel, currently!!!'
            )

    async def pause(self):
        pass

    async def playlist(self, message):
        await message.channel.send(
            'The current playlist is:\n\t\t {} \n\n'.format(self._autoplaylistName)
        )

    async def store(self, message):
        splitMessage = message.content.split(' ')

        if len(splitMessage) > 1:
            if splitMessage[1] == 'true' and self._configs.saveQueuedSongs is not True:
                self._configs.saveQueuedSongs = True
            elif splitMessage[1] == 'false' and self._configs.saveQueuedSongs is not False:
                self._configs.saveQueuedSongs = False

            await message.channel.send(
                'Storing queued songs is now set to: {}'.format(self._configs.saveQueuedSongs)
            )
        else:
            await message.channel.send(
                'Storing queued songs is currently set to: {}'.format(self._configs.saveQueuedSongs)
            )

    '''----- Summon AcaBot to a voice channel -----'''
    async def summon(self, message):
        # Check to see if AcaBot is in a voice channel
        botVoiceChannels = self._client.voice_clients

        # Check to see if the user summoning the bot is in a voice channel
        if not message.author.voice:
            await message.channel.send(
                '{}, you are not currently in a voice channel! Please join one before trying to summon me.'
                .format(message.author.nick)
            )
        else:  # Get AcaBot into the summoner's channel
            # Announce AcaBot's Arrival
            await message.channel.send(
                'Get ready for some MUSIC, AcaBot is joining this voice channel'
            )

            if not botVoiceChannels:
                await self.setVoice(message.author.voice.channel)
            elif botVoiceChannels:
                await self._voice.move_to(message.author.voice.channel)

    # General Commands
    def deleteMessageCheck(self, message):
        return message.content.startswith(self._configs.commandPrefix) or message.author.id == self._client.user.id

    async def cleanChat(self, message):
        deleted = await message.channel.purge(limit=200, check=self.deleteMessageCheck)

    async def help(self):
        pass

    async def nowPlaying(self):
        pass

    async def play(self):
        pass

    async def showQueue(self):
        pass

    async def skip(self):
        pass
