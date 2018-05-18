import asyncio
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

	# Queues
	coolDownPlaylist = []
	userPlaylist = []

	def __init__(self, client, volume):
		self.__volume = volume


	'''------------- SETTERS AND GETTERS-------------'''
	# Get the current volume level
	async def getVolume(self):
		return self.__volume


	# Set the player variable
	async def setPlayer(self, song):
		self.__player = await self.__voice.create_ytdl_player(song)


	async def setPlayerVolume(self):
		self.__player.volume = self.__volume


	# Set a new volume level
	async def setVolume(self, config, newVolume):
		self.__volume = newVolume


	# Setup the voice variable
	async def setVoice(self, client, channel):
		self.__voice = await client.join_voice_channel(channel)


	'''-------------FUNCTIONALITY-------------'''
	# Delete the currently playing song from the Autoplaylist and skip the rest of the song
	async def deleteAndSkipNP(self, client, config, message):
		url = self.__player.url
		songTitle = self.__player.title

		await client.send_message(message.channel, 'You have delete the song {0} with the url {1}... Please queue it again if you want it back in the playlist.' .format(songTitle, url))
		config.Autoplaylist.remove(url)

		# rewrite the Autoplaylist excluding the removed song
		if '.txt' in config.AutoplaylistName:
			f = open('playlists/' + config.AutoplaylistName, 'w')

			for song in config.Autoplaylist:
				f.write(song + '\n')

		elif '.txt' not in config.AutoplaylistName:
			f = open('playlists/' + config.AutoplaylistName + '.txt', 'w')

			for song in config.Autoplaylist:
				f.write(song + '\n')

		# Now skip the song
		await self.skipSong()


	# Disconnect from the current voice channel
	async def disconnect(self):
		if self.__voice is not None and self.__voice.is_connected():
			self.__player.pause()
			await self.__voice.disconnect()
			self.__voice = None
			print(self.__voice)


	async def displayQueue(self, client, message):
		await client.send_message(message.channel, 
			self.userPlaylist
			)


	# Plays music continuously
	async def MusicPlayer(self, client, config):
		# If no Autoplaylist exists or if it is empty
		if config.Autoplaylist is None or not config.Autoplaylist:
			self.__player = await self.__voice.create_ytdl_player("ytsearch:start")

		# Otherwise start the music
		else:
			# Random starting song
			song = random.choice(config.Autoplaylist)

			# Create the stream for music
			await self.setPlayer(song)
			await self.setPlayerVolume()

			# # Start the coolDownQeueu creation
			if len(config.Autoplaylist) > 1:
				self.coolDownPlaylist.append(song)

			await asyncio.sleep(3)

			# Begin the music
			self.__player.start()

		# Continue the music
		while self.__voice is not None:
			# Waiting
			if (config.Autoplaylist is None or not config.Autoplaylist or self.__player.is_playing()) and not self.__player.is_done():
				await asyncio.sleep(2)

			# Time for a new song
			elif self.__player.is_done():
				self.__player.stop()

				# If a user queued a song
				if self.userPlaylist:
					# Song that will be played
					if config.Shuffle:
						song = random.choice(self.userPlaylist)
					else:
						song = self.userPlaylist[0]

					# Create the stream for music
					await self.setPlayer(song)
					await self.setPlayerVolume()

					if len(self.coolDownPlaylist) >= floor(len(config.Autoplaylist) * config.CoolDownQueueSize) and len(self.coolDownPlaylist) > 0:
						# Remove the first song in the Cool Down Queue
						self.coolDownPlaylist.pop(0)

						# Add to the cool down queue so no repeats happen
						self.coolDownPlaylist.append(song)

					elif len(self.coolDownPlaylist) < floor(len(config.Autoplaylist) * config.CoolDownQueueSize) and len(config.Autoplaylist) > 1:
						# Add to the cool down queue so no repeats happen
						self.coolDownPlaylist.append(song)

					# Remove the song from the user playlist
					self.userPlaylist.remove(song)

					await asyncio.sleep(3)

					# Begins playing music through voice chat
					self.__player.start()

				# When the userPlaylist is empty
				elif config.Autoplaylist:
					# Song url that will be played
					song = random.choice(config.Autoplaylist)

					# Make sure the song isnt on cool down
					while song in self.coolDownPlaylist:
						song = random.choice(config.Autoplaylist)

					# Create the stream for music
					await self.setPlayer(song)
					await self.setPlayerVolume()

					if len(self.coolDownPlaylist) >= floor(len(config.Autoplaylist) * config.CoolDownQueueSize) and len(self.coolDownPlaylist) > 0:
						# Remove the first song in the Cool Down Queue
						self.coolDownPlaylist.pop(0)

						# Add to the cool down queue so no repeats happen
						self.coolDownPlaylist.append(song)

					elif len(self.coolDownPlaylist) < floor(len(config.Autoplaylist) * config.CoolDownQueueSize) and len(config.Autoplaylist) > 1:
						# Add to the cool down queue so no repeats happen
						self.coolDownPlaylist.append(song)

					await asyncio.sleep(3)

					# Begins playing music through voice chat
					self.__player.start()


	# Output information on the song that is currently playing
	async def nowPlaying(self, client, message):
		await client.send_message(message.channel, 
			'You are currently listening to {0}. \n' 
			'The URL for the current song is {1}' .format(self.__player.title, self.__player.url))


	async def queueToUserPlaylist(self, client, config, message):
		songs = message.content.split(' ')

		for song in songs:
			if 'www.youtube.com/watch' in song:
				self.userPlaylist.append(song)

				if song not in config.Autoplaylist:
					if '.txt' in config.AutoplaylistName:
						# open the Autoplaylist file and put the new url in
						with open('playlists/{}' .format(config.AutoplaylistName), 'a') as f:
							f.write('{} \n' .format(song))
						f.close()

					elif '.txt' not in config.AutoplaylistName:
						# Open the Autoplaylist file and put the new url in
						with open('playlists/{}.txt' .format(config.AutoplaylistName), 'a') as f:
							f.write('{}\n' .format(song))
						f.close()

					# Also add it to the current Autoplaylist being used
					config.Autoplaylist.append(song)

				else:
					self.userPlaylist.append(song)


	# Shutdown the bot
	async def shutdown(self, client, config, message):
		await functions.cleanChat(client, config, message, 1)

		# Stop the music
		if self.__player is not None and self.__player.is_playing():
			self.__player.stop()

		# Disconnect from voice if needed
		await self.disconnect()

		# Log AcaBot out of Discord
		await client.logout()

		# Finally close the client connection
		await client.close()


	# Skip the currently playing song
	async def skipSong(self):
		if self.__player is not None:
			self.__player.stop()


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

			# Make sure the bot doesnt kill itself
			if self.__player is not None:
				self.__player.stop()

			# Start the music
			await self.MusicPlayer(client, config)

			# Announces AcaBot's arrival
			await client.send_message(message.channel, 'AcaBot has joined the voice channel "{}", get ready for some music!' .format(summoned_channel))

		else:
			await self.__voice.move_to(summoned_channel)

			# Make sure the bot doesnt kill itself
			if self.__player is not None:
				self.__player.stop()

			# Announces AcaBot's arrival
			await client.send_message(message.channel, 'AcaBot has moved to the voice channel "{}", get ready for some music!' .format(summoned_channel))

		return True


	async def volumeController(self, client, message):
		splitMessage = message.content.split(' ')
		minArgs = 1
		maxArgs = 3

		if (minArgs < len(splitMessage) < maxArgs) and splitMessage[1].isdigit():
			newVolume = int(splitMessage[1])

			if newVolume > 100:
				newVolume = 100

			self.__volume = newVolume / 100
			self.__player.volume = self.__volume

			await client.send_message(message.channel, 'The volume is now set to {} percent' .format(newVolume))

		else:
			await client.send_message(message.channel, 'The current volume is {}' .format(await self.getVolume() * 100))


	# Get Song
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
			'''