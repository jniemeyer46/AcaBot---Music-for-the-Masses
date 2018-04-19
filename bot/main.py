import sys
import time
import random
import discord
import asyncio
import itertools
import youtube_dl
from discord.ext import commands

import commands
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
			# User enters a new playlist file for the bot to pull from (if empty it will not use an autoplaylist)
			if msg[0] == 'playlist':
				if '.txt' in msg[1]:
					await client.send_message(message.channel, 'You have changed AcaBot\'s playlist to {}' .format(msg[1]))
					config.autoplaylist = msg[1]
				elif '.txt' not in msg[1]:
					await client.send_message(message.channel, 'You have changed AcaBot\'s playlist to {}.txt' .format(msg[1]))
					config.autoplaylist = msg[1] + '.txt'

			# This will restart the bot incase a problem occurs and it needs to be restarted (No clue how to do this one yet)
			elif msg[0] == 'restart':
				print('This will not be implemented until the very end most likely.')

			# Shuts down the bot (Not the correct way to do this, need to look into it still...  Technically works though atm)
			elif msg[0] == 'shutdown':
				print('This will be correctly implemented later on, just wanted a fast way to kill AcaBot')
				sys.exit(0)
			elif msg[0] == 'testing':
				pass


	'''------TRUSTED COMMANDS------'''

	# Makes sure that only TRUSTED users can use these commands
	if msg[0] in config.TrustedCommands:
		if config.Trusted_Permissions is None and str(message.author.top_role) in config.Role_Permissions:
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

		elif message.author.id in config.Trusted_Permissions:
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
					'	~{0}playlist <name of a .txt file> - This changed the autoplaylist to a user defined list (if no .txt file is specified the autoplaylist will be NONE). \n'
					'	~{0}restart - restarts AcaBot (Won\'t be implemented for a while). \n'
					'	{0}shutdown - Kills AcaBot, RIP. \n\n'

					'TRUSTED USER COMMANDS \n'
					'	{0}delete - Deletes the last 100 commands for AcaBot and AcaBot message, can use multiple times to delete them all. \n'
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
				'You are currently listening to {0}.' .format(player.title))

		# Pause the bot (Not sure if I want everyone to be able to do this or not)
		elif msg[0] == 'pause':
			if player is not None:
				if player.is_playing():
					player.pause()

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
			if 'www.youtube.com/watch' in msg[1]:
				if config.Store:
					# Required in order to fix casing
					url = message.content.split(' ')
					config.Userplaylist.append(url[1])

					if url[1] not in config.Autoplaylist:
						# Open the Autoplaylist file and put the new url in
						with open('playlists/{}.txt' .format(config.AutoplaylistName), 'a') as f:
							f.write('{}\n' .format(url[1]))
						f.close()

						# Queue up the songs
						config.Autoplaylist.append(url[1])
				else:
					# Required in order to fix casing
					url = message.content.split(' ')
					config.Userplaylist.append(url[1])

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
		for key in client.voice_clients:
			await key.move_to(summoned_channel)
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
			config.Userplaylist.remove(url)
			player.volume = config.Volume

			# Begins playing music through voice chat
			player.start()
		else:
			# Creates a stream for music playing
			player = await voice.create_ytdl_player(config.Userplaylist[0])
			config.Userplaylist.pop(0)
			player.volume = config.Volume

			# Begins playing music through voice chat
			player.start()
	elif config.Autoplaylist:
		# Creates a stream for music playing
		player = await voice.create_ytdl_player(random.choice(config.Autoplaylist))
		player.volume = config.Volume

		# Begins playing music through voice chat
		player.start()

	# Continuous Loop that will continuously check if there is music playing.
	# Wait if there is music playing, queue a song otherwise.
	while True:
		if player.is_playing():
			await asyncio.sleep(2)
		elif player.is_done():
			player.stop()

			if config.Userplaylist:
				if config.Shuffle:
					url = random.choice(config.Userplaylist)

					# Creates a stream for music playing
					player = await voice.create_ytdl_player(url)
					config.Userplaylist.remove(url)
					player.volume = config.Volume

					# Begins playing music through voice chat
					player.start()
				else:
					# Creates a stream for music playing
					player = await voice.create_ytdl_player(config.Userplaylist[0])
					config.Userplaylist.pop(0)
					player.volume = config.Volume

					# Begins playing music through voice chat
					player.start()
			elif config.Autoplaylist:
				# Creates a stream for music playing
				player = await voice.create_ytdl_player(random.choice(config.Autoplaylist))
				player.volume = config.Volume

				# Begins playing music through voice chat
				player.start()


client.run(config.Token)