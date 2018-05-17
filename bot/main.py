import sys
import time
import random
import discord
import asyncio
import itertools
import youtube_dl
import os.path
from discord.ext import commands
from math import floor

#from config import Config, DefaultConfigs
from personal_config import Config, DefaultConfigs

# Stores the file that has the user input settings
config_file = DefaultConfigs.Settings

# Discord client connection
client = discord.Client()
# Holds all of AcaBot's configurations
config = Config(config_file)

if not discord.opus.is_loaded():
	discord.opus.load_opus('opus.dll')

# Variable Holders
voice = None
player = None

@client.event
async def on_ready():
	print('%s has logged into the discord channel' % client.user.name)


@client.event
async def on_message(message):
	msg = message.content.lower()
	global player

	# Determine whether the message was a command for the bot, parse out the Command_Prefix
	if msg.startswith(config.Command_Prefix):
		# Grabs message content, makes it all lowercase, and stores it in a variable
		msg = msg[1:].split(' ')


	'''------OWNER COMMANDS------'''

	# Makes sure the GIVEN owner of the server is the one using the command
	if msg[0] in config.OwnerCommands:
		if str(message.author.id) == config.Owner_ID:
			# Shuts down the bot (Not the correct way to do this, need to look into it still...  Technically works though atm)
			if msg[0] == 'shutdown':
				# Just some holders
				counter = 0
				msgs = []

				# Just a friends message
				await client.send_message(message.channel, 'Cleaning the chat before I leave...')

				# Create the list to be deleted
				async for log in client.logs_from(message.channel):
					if str(log.author.id) == client.user.id or log.content.startswith(config.Command_Prefix):
						msgs.append(log)
						counter += 1

				# Time to delete the old commands
				if len(msgs) < 2:
					await client.delete_message(msgs[0])
				elif len(msgs) >= 2 and len(msgs) <= 100:
					await client.delete_messages(msgs)

				# Just a funny message
				await client.send_message(message.channel, 'I was always taught to leave a place better than I found it, {} total deleted messages.' .format(counter+1))

				await asyncio.sleep(5)

				# Deleting the funny message
				async for log in client.logs_from(message.channel):
					if str(log.author.id) == client.user.id:
						await client.delete_message(log)

				# Stop the music
				if player is not None and player.is_playing():
					player.stop()

				# Disconnect from voice
				for voice in client.voice_clients:
					if voice.is_connected():
						voice.disconnect()
				
				# Logs the bot out
				await client.logout()

				# Closes the client connection to allow for perfect shutdown
				await client.close()

			elif msg[0] == 'testing':
				pass


	'''------TRUSTED COMMANDS------'''

	# Makes sure that only TRUSTED users can use these commands
	if msg[0] in config.TrustedCommands:
		if config.Trusted_Permissions is None and str(message.author.top_role) in config.Role_Permissions:
			# Delete all of the bot's previous outputs
			if msg[0] == 'delete':
				# Just some holders
				counter = 0
				msgs = []

				await client.send_message(message.channel, 'Calculating messages...')
				async for log in client.logs_from(message.channel):
					if str(log.author.id) == client.user.id or log.content.startswith(config.Command_Prefix):
						msgs.append(log)
						counter += 1

				if len(msgs) < 2:
					await client.delete_message(msgs[0])
				elif len(msgs) >= 2 and len(msgs) <= 100:
					await client.delete_messages(msgs)

				await client.send_message(message.channel, 'You have delete {} of my messages...  Well make that {} messages' .format(counter, counter+1))
				await asyncio.sleep(5)

				async for log in client.logs_from(message.channel):
					if str(log.author.id) == client.user.id:
						await client.delete_message(log)

			elif msg[0] == 'deletenp':
				await client.send_message(message.channel, 'You have delete the song {0} with the url {1}... Please queue it again if you would like it in the playlist again.' .format(player.title, player.url))
				config.Autoplaylist.remove(player.url)

				if '.txt' in config.AutoplaylistName:
					f = open('playlists/' + config.AutoplaylistName, "w")

					for song in config.Autoplaylist:
						f.write(song + '\n')
				elif '.txt' not in config.AutoplaylistName:
					f = open('playlists/' + config.AutoplaylistName + '.txt', "w")

					for song in config.Autoplaylist:
						f.write(song + '\n')

			# User enters a new playlist file for the bot to pull from (if empty it will not use an autoplaylist)
			elif msg[0] == 'playlist':
				temp = message.content
				playlistName = temp.split(' ')

				config.CoolDownQueue.clear()

				if len(playlistName) < 2:
					await client.send_message(message.channel, 'You have turned off AcaBot\'s autoplaylist.')

					if config.AutoplaylistName is not None:
						# Clears the autoplaylist
						config.Autoplaylist.clear()

				elif '.txt' in playlistName[1]:
					await client.send_message(message.channel, 'You have changed AcaBot\'s playlist to {}' .format(playlistName[1]))

					# Set the autoplaylist name
					config.AutoplaylistName = playlistName[1]

					if os.path.exists('playlists/' + config.AutoplaylistName):
						with open('playlists/' + config.AutoplaylistName) as f:
							config.Autoplaylist = f.read().split()

					else:
						# Create the file if it doesn't exist already
						f = open('playlists/' + playlistName[1], "w+")
						config.Autoplaylist = f.read().split()
						f.close()

				elif '.txt' not in playlistName[1]:
					await client.send_message(message.channel, 'You have changed AcaBot\'s playlist to {}.txt' .format(playlistName[1]))

					# Set the autoplaylist name
					config.AutoplaylistName = playlistName[1]

					if os.path.exists('playlists/' + config.AutoplaylistName + '.txt'):
						with open('playlists/' + config.AutoplaylistName + '.txt') as f:
							config.Autoplaylist = f.read().split()

					else:
						# Create the file if it doesn't exist already
						f = open('playlists/' + playlistName[1] + '.txt', "w+")
						config.Autoplaylist = f.read().split()
						f.close()

			# Toggles shuffle for the queue
			elif msg[0] == 'shuffle':
				if config.Shuffle:
					config.Shuffle = False
					await client.send_message(message.channel, 'The queued songs will not be shuffled.')
				elif not config.Shuffle:
					config.Shuffle = True
					await client.send_message(message.channel, 'The queued songs will be shuffled.')

			# Toggles storing the youtube videos into the current autoplaylist (should not add duplicates)
			elif msg[0] == 'store':
				if config.Store:
					config.Store = False
					await client.send_message(message.channel, 'The queued songs will no longer be added to the autoplaylist.')
				elif not config.Store:
					config.Store = True
					await client.send_message(message.channel, 'The queued songs will now be added to the autoplaylist.')

			# Summons the bot to the the caller's voice channel
			elif msg[0] == 'summon':
				await summon(message)

			# CHange the volume level of the music
			elif msg[0].startswith('v'):
				if len(msg) > 1:
					if msg[1].isdigit():
						player.volume = int(msg[1]) / 100
						config.Volume = int(msg[1]) / 100
						await client.send_message(message.channel, 'The volume is now set to {}' .format(msg[1]))
				else:
					await client.send_message(message.channel, 'The current volume is {}' .format(config.Volume * 100))

		elif config.Trusted_Permissions is not None and str(message.author.id) in config.Trusted_Permissions:
			# Delete all of the bot's previous outputs
			if msg[0] == 'delete':
				counter = 0
				msgs = []
				await client.send_message(message.channel, 'Calculating messages...')
				async for log in client.logs_from(message.channel):
					if str(log.author.id) == client.user.id or log.content.startswith(config.Command_Prefix):
						msgs.append(log)
						counter += 1

				if len(msgs) < 2:
					await client.delete_message(msgs[0])
				elif len(msgs) >= 2 and len(msgs) <= 100:
					await client.delete_messages(msgs)

				await client.send_message(message.channel, 'You have delete {} of my messages...  Well make that {} messages' .format(counter, counter+1))
				time.sleep(5)

				async for log in client.logs_from(message.channel):
					if str(log.author.id) == client.user.id:
						await client.delete_message(log)

			elif msg[0] == 'deletenp':
				await client.send_message(message.channel, 'You have delete the song {0} with the url {1}... Please queue it again if you would like it in the playlist again.' .format(player.title, player.url))
				config.Autoplaylist.remove(player.url)

				if '.txt' in config.AutoplaylistName:
					f = open('playlists/' + config.AutoplaylistName, "w")

					for song in config.Autoplaylist:
						f.write(song + '\n')
				elif '.txt' not in config.AutoplaylistName:
					f = open('playlists/' + config.AutoplaylistName + '.txt', "w")

					for song in config.Autoplaylist:
						f.write(song + '\n')

			# User enters a new playlist file for the bot to pull from (if empty it will not use an autoplaylist)
			elif msg[0] == 'playlist':
				temp = message.content
				playlistName = temp.split(' ')

				config.CoolDownQueue.clear()

				if len(playlistName) < 2:
					await client.send_message(message.channel, 'You have turned off AcaBot\'s autoplaylist.')

					if config.AutoplaylistName is not None:
						# Clears the autoplaylist
						config.Autoplaylist.clear()

				elif '.txt' in playlistName[1]:
					await client.send_message(message.channel, 'You have changed AcaBot\'s playlist to {}' .format(playlistName[1]))

					# Set the autoplaylist name
					config.AutoplaylistName = playlistName[1]

					if os.path.exists('playlists/' + config.AutoplaylistName):
						with open('playlists/' + config.AutoplaylistName) as f:
							config.Autoplaylist = f.read().split()

					else:
						# Create the file if it doesn't exist already
						f = open('playlists/' + playlistName[1], "w+")
						config.Autoplaylist = f.read().split()
						f.close()

				elif '.txt' not in playlistName[1]:
					await client.send_message(message.channel, 'You have changed AcaBot\'s playlist to {}.txt' .format(playlistName[1]))

					# Set the autoplaylist name
					config.AutoplaylistName = playlistName[1]

					if os.path.exists('playlists/' + config.AutoplaylistName + '.txt'):
						with open('playlists/' + config.AutoplaylistName + '.txt') as f:
							config.Autoplaylist = f.read().split()

					else:
						# Create the file if it doesn't exist already
						f = open('playlists/' + playlistName[1] + '.txt', "w+")
						config.Autoplaylist = f.read().split()
						f.close()

			# Toggles shuffle for the queue
			elif msg[0] == 'shuffle':
				if config.Shuffle:
					config.Shuffle = False
					await client.send_message(message.channel, 'The queued songs will not be shuffled.')
				elif not config.Shuffle:
					config.Shuffle = True
					await client.send_message(message.channel, 'The queued songs will be shuffled.')

			# Toggles storing the youtube videos into the current autoplaylist (should not add duplicates)
			elif msg[0] == 'store':
				if config.Store:
					config.Store = False
					await client.send_message(message.channel, 'The queued songs will no longer be added to the autoplaylist.')
				elif not config.Store:
					config.Store = True
					await client.send_message(message.channel, 'The queued songs will now be added to the autoplaylist.')

			# Summons the bot to the the caller's voice channel
			elif msg[0] == 'summon':
				await summon(message)
				if player is not None:
					await MusicPlayer()

			# Sets the volume of the bot for the entire voice chat
			elif msg[0].startswith('v'):
				if len(msg) > 1:
					if msg[1].isdigit():
						player.volume = int(msg[1]) / 100
						config.Volume = int(msg[1]) / 100
						await client.send_message(message.channel, 'The volume is now set to {}' .format(msg[1]))
				else:
					await client.send_message(message.channel, 'The current volume is {}' .format(config.Volume * 100))


	'''------GENERAL COMMANDS------'''

	# Check for GENERAL command usage
	if msg[0] in config.GeneralCommands:
		# Outputs information about the song that is currently playing
		if msg[0] == 'help':
			await client.send_message(message.channel, 
					'~ - means that functionality has not yet been implemented as of yet. \n\n'

					'OWNER SPECIFIC COMMANDS \n'
					'	{0}shutdown - Kills AcaBot, RIP. \n\n'

					'TRUSTED USER COMMANDS \n'
					'	{0}delete - Deletes the last 100 commands for AcaBot and AcaBot message, can use multiple times to delete them all. \n'
					'	{0}deletenp - Deletes the song that is currently playing from the autoplaylist. \n'
					'	{0}playlist <name of a .txt file> - This changed the autoplaylist to a user defined list (if no .txt file is specified the autoplaylist will be NONE). \n'
					'	{0}shuffle - Determines whether the queue should be shuffles (Toggled). \n'
					'	{0}store - Determines whether songs that users play should be added to the current autoplaylist (Toggled). \n'
					'	{0}summon - Summons the bot to the caller\'s voice channel'
					'	{0}volume (or !v) - Changes the volume level for the entire server. \n\n'

					'COMMANDS FOR EVERYONE \n'
					'	{0}help - Outputs commands for AcaBot. \n'
					'	{0}np - Outputs information on the song that is currently playing. \n'
					'	~{0}pause - Pauses the currently playing song. \n'
					'	{0}queue (or !q) - Outputs the list of songs that users have asked to be played (in order). \n'
					'	~{0}quiet - Mutes AcaBot for a single user (if owner uses the command it mutes the bot for the entire server). \n'
					'	{0}skip (or !s) - Skips the currently playing song. \n'
					'	{0}play <YOUTUBE URL> (or !p) - This will queue a song to be played (will be sentence recognition later). \n'
					'	{0}roll <<number of dice>d<type of dice>> - Will roll a specified dice for the user (example: !roll 5d20 (rolls 5 dice that are 20 sided)). \n' .format(config.Command_Prefix)
				)

		# Outputs information about the song that is currently playing
		elif msg[0] == 'np':
			await client.send_message(message.channel, 
				'You are currently listening to {0}. \n' 
				'The URL for the current song is {1}' .format(player.title, player.url))

		# Pause the bot (Not sure if I want everyone to be able to do this or not)
		elif msg[0] == 'pause':
			pass

		# Outputs the list of songs that have been queued by people in the discord channel
		elif msg[0] == 'q' or msg == 'queue':
			await client.send_message(message.channel, 
					config.Userplaylist
				)

		# If the owner uses this command it will mute the bot for the entire channel
		# If anyone else uses this command it will only mute the bot for them alone
		elif msg[0] == 'quiet':
			pass

		# Skips the current song
		elif msg[0] == 's' or msg == 'skip':
			if player is not None:
				player.stop()

		# User enters a youtube link to be played ADD STORE HERE
		elif msg[0].startswith('p'):
			urls = message.content.split(' ')

			for url in urls:
				if 'www.youtube.com/watch' in url:
					if config.Store:
						config.Userplaylist.append(url)

						if url not in config.Autoplaylist:
							if '.txt' in config.AutoplaylistName:
								# Open the Autoplaylist file and put the new url in
								with open('playlists/{}' .format(config.AutoplaylistName), 'a') as f:
									f.write('{}\n' .format(url))
								f.close()

							elif '.txt' not in config.AutoplaylistName:
								# Open the Autoplaylist file and put the new url in
								with open('playlists/{}.txt' .format(config.AutoplaylistName), 'a') as f:
									f.write('{}\n' .format(url))
								f.close()

							# Queue up the songs
							config.Autoplaylist.append(url)
					else:
						config.Userplaylist.append(url)

		# User enters a new playlist file for the bot to pull from
		elif msg[0].startswith('roll'):
			dice = ["".join(x) for _, x in itertools.groupby(msg[1], key=str.isdigit)]

			dice_rolls = []
			for i in range(0, int(dice[0])):
				dice_rolls.append(random.randrange(1, int(dice[2])+1))

			await client.send_message(message.channel,
					'The following are your rolls in order from left to right: \n\t{}' .format(dice_rolls)
				)


# Summons the bot to the voice channel of the message author if they have the proper permissions
async def summon(message):
	global voice
	summoned_channel = message.author.voice.voice_channel

	# Checks to see if the message sender is in a voice channel
	if summoned_channel is None:
		await client.send_message(message.channel, '{}, You are not currently in a voice channel' .format(message.author.nick))
		return False

	# Makes a list of the voice channels joined by the bot
	voiceChannel = client.voice_clients

	# Places the bot in the appropriate voice channel
	if not voiceChannel:
		voice = await client.join_voice_channel(summoned_channel)
		await MusicPlayer()
		print('AcaBot has joined the channel "{}"!' .format(summoned_channel))
	else:
		for voice in client.voice_clients:
			await voice.move_to(summoned_channel)
			print('AcaBot has moved to the channel "{}"!' .format(summoned_channel))
	return True


# Attempts to constantly play music (needs reworked)
async def MusicPlayer():
	global voice
	global player

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

client.run(config.Token)