import functions
import os.path
import random
import youtube_dl
from math import floor

class MusicBot:
	# Holds the youtube data information
	__player = None
	# Holds the current voice session information
	__voice = None

	def __init__(self, client, volume):
		self.__volume = volume


	'''------------- SETTERS AND GETTERS-------------'''
	# Set the player variable
	async def setPlayer(self, song):
		self.__player = await self.__voice.create_ytdl_player(song)


	# Set a new volume level
	async def setVolume(self, config, newVolume):
		self.__volume = newVolume


	# Setup the voice variable
	async def setVoice(self, client, channel):
		self.__voice = await client.join_voice_channel(channel)


	'''-------------FUNCTIONALITY-------------'''
	# Disconnect from the current voice channel
	async def disconnect(self):
		if self.__voice is not None and self.__voice.is_connected():
			await self.__voice.disconnect()


	async def MusicPlayer(self, client, config):
		pass


	# Shutdown the bot
	async def shutdown(self, client, config, message):
		await functions.cleanChat(client, config, message, 1)

		# Stop the music
		if self.__player is not None and player.is_playing():
			self.__player.stop()

		# Disconnect from voice if needed
		await self.disconnect()

		# Log AcaBot out of Discord
		await client.logout()

		# Finally close the client connection
		await client.close()


	# Attempts to join a voice channel
	# Config used later for music settings
	async def summonToVoice(self, client, config, message):
		summoned_channel = message.author.voice.voice_channel

		# Checks to see if the summoning user is actually in a voice channel
		if summoned_channel is None:
			await client.send_message(message.channel, '{}, you are not currently in a voice channel' .format(message.author.nick))
			return False

		# List the voice channels that AcaBot is currently in
		voiceChannels = client.voice_clients

		# Place AcaBot in the appropriate channel in terms of the summoner
		if not voiceChannels:
			await self.setVoice(client, summoned_channel)

			# Start the music
			await self.MusicPlayer(client, config)

			# Announces AcaBot's arrival
			await client.send_message(message.channel, 'AcaBot has joined the voice channel "{}", get ready for some music!' .format(summoned_channel))

		else:
			await self.__voice.move_to(summoned_channel)

			# Start the music
			await self.MusicPlayer(client, config)

			# Announces AcaBot's arrival
			await client.send_message(message.channel, 'AcaBot has moved to the voice channel "{}", get ready for some music!' .format(summoned_channel))

		return True

	# Get Song
	# MusicPlayer
	# Play
	# Pause
	# Get Playlist
	# Set Playlist
	# Deletenp
	# now playing
	# queue
	# Quiet
	# Skip
	
'''
# Sets the player
	self.__player = await self.__voice.create_ytdl_player("ytsearch:hello")
	self.__player.volume = self.__volume

	self.__player.start()

# Attempts to constantly play music (needs reworked)
async def MusicPlayer():
	# Initial music video queued here
	if config.Userplaylist:
		if config.Shuffle:
			url = random.choice(config.Userplaylist)

			# Creates a stream for music playing
			player = await voice.create_ytdl_player(url)
			player.volume = config.Volume

			if len(config.Autoplaylist) > 1:
				# Start creating a cool down queue so no repeats happen
				config.CoolDownQueue.append(url)

			# Remove the song from the user playlist
			config.Userplaylist.remove(url)

			await asyncio.sleep(3)

			# Begins playing music through voice chat
			player.start()

		else:
			# Creates a stream for music playing
			player = await voice.create_ytdl_player(config.Userplaylist[0])
			player.volume = config.Volume

			if len(config.Autoplaylist) > 1:
				# Start creating a cool down queue so no repeats happen
				config.CoolDownQueue.append(config.Userplaylist[0])

			# Remove the song from the user playlist
			config.Userplaylist.pop(0)

			await asyncio.sleep(3)

			# Begins playing music through voice chat
			player.start()

	elif config.Autoplaylist:
		# Song url that will be played
		song = random.choice(config.Autoplaylist)

		# Creates a stream for music playing
		player = await voice.create_ytdl_player(song)
		player.volume = config.Volume

		if len(config.Autoplaylist) > 1:
			# Start creating a cool down queue so no repeats happen
			config.CoolDownQueue.append(song)

		await asyncio.sleep(3)

		# Begins playing music through voice chat
		player.start()

	# Continuous Loop that will continuously check if there is music playing.
	# Wait if there is music playing, queue a song otherwise.
	while True:
		if config.Autoplaylist is None or not config.Autoplaylist or player.is_playing():
			await asyncio.sleep(2)

		elif player.is_done():
			player.stop()

			if config.Userplaylist:
				if config.Shuffle:
					# Song url that will be played
					url = random.choice(config.Userplaylist)

					# Creates a stream for music playing
					player = await voice.create_ytdl_player(url)
					player.volume = config.Volume

					if len(config.CoolDownQueue) >= floor(len(config.Autoplaylist) * config.CoolDownQueueSize):
						if len(config.CoolDownQueue) > 0:
							# Remove the first song in the Cool Down Queue
							config.CoolDownQueue.pop(0)
						
						if len(config.Autoplaylist) > 1:
							# Add to the cool down queue so no repeats happen
							config.CoolDownQueue.append(url)

					elif len(config.CoolDownQueue) < floor(len(config.Autoplaylist) * config.CoolDownQueueSize):
						# Add to the cool down queue so no repeats happen
						config.CoolDownQueue.append(url)

					# Remove the song from the user playlist
					config.Userplaylist.remove(url)

					await asyncio.sleep(3)

					# Begins playing music through voice chat
					player.start()

				else:
					# Song url that will be played
					song = config.Userplaylist[0]

					# Creates a stream for music playing
					player = await voice.create_ytdl_player(song)
					player.volume = config.Volume
				
					if len(config.CoolDownQueue) >= floor(len(config.Autoplaylist) * config.CoolDownQueueSize):
						if len(config.CoolDownQueue) > 0:
							# Remove the first song in the Cool Down Queue
							config.CoolDownQueue.pop(0)
						
						if len(config.Autoplaylist) > 1:
							# Add to the cool down queue so no repeats happen
							config.CoolDownQueue.append(song)

					elif len(config.CoolDownQueue) < floor(len(config.Autoplaylist) * config.CoolDownQueueSize):
						# Add to the cool down queue so no repeats happen
						config.CoolDownQueue.append(song)

					# Remove the song from the user playlist
					config.Userplaylist.pop(0)

					await asyncio.sleep(3)

					# Begins playing music through voice chat
					player.start()

			elif config.Autoplaylist:
				# Song url that will be played
				song = random.choice(config.Autoplaylist)

				while song in config.CoolDownQueue:
					song = random.choice(config.Autoplaylist)

				# Creates a stream for music playing
				player = await voice.create_ytdl_player(song)
				player.volume = config.Volume

				if len(config.CoolDownQueue) >= floor(len(config.Autoplaylist) * config.CoolDownQueueSize):
					if len(config.CoolDownQueue) > 0:
						# Remove the first song in the Cool Down Queue
						config.CoolDownQueue.pop(0)

					if len(config.Autoplaylist) > 1:
						# Add to the cool down queue so no repeats happen
						config.CoolDownQueue.append(song)

				elif len(config.CoolDownQueue) < floor(len(config.Autoplaylist) * config.CoolDownQueueSize):
					if len(config.Autoplaylist) > 1:
						# Add to the cool down queue so no repeats happen
						config.CoolDownQueue.append(song)

				await asyncio.sleep(3)

				# Begins playing music through voice chat
				player.start()

			print(config.CoolDownQueue)
			'''