# General Imports
import random
import discord
import asyncio
import itertools
from discord.ext import commands

# Bot Files
import functions
from MusicBot import MusicBot
#from config import Config, DefaultConfigs
from personal_config import Config, DefaultConfigs

# Stores the file that has the user input settings
config_file = DefaultConfigs.Settings


''' SETUP FOR THE ENTIRE BOT '''
# Discord client connection
client = discord.Client()
# Holds all of AcaBot's configurations
config = Config(config_file)



# CHECK IF THIS IS EVEN NEEDED JOHN
if not discord.opus.is_loaded():
	discord.opus.load_opus('opus.dll')



''' BOT STARTS HERE '''

AcaBot = MusicBot(client, config.Volume)

@client.event
async def on_ready():
	print('%s has logged into the discord channel' % client.user.name)


@client.event
async def on_message(message):
	msg = message.content.lower()

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
				await AcaBot.shutdown(client, config, message)

			elif msg[0] == 'testing':
				await AcaBot.MusicPlayer(client, config)


	'''------TRUSTED COMMANDS------'''

	# Makes sure that only TRUSTED users can use these commands
	if msg[0] in config.TrustedCommands:
		if ((config.Role_Permissions is not None and config.Trusted_Permissions is None) and str(message.author.top_role) in config.Role_Permissions) or (config.Trusted_Permissions is not None and str(message.author.id) in config.Trusted_Permissions):
			# Delete all of the bot's previous outputs
			if msg[0] == 'delete':
				await functions.cleanChat(client, config, message, 0)

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

			elif msg[0] == 'disconnect':
				await AcaBot.disconnect()

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
				await AcaBot.summonToVoice(client, config, message)

			# CHange the volume level of the music
			elif msg[0] == 'v' or msg[0] == 'volume':
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
					'	~{0}deletenp - Deletes the song that is currently playing from the autoplaylist. \n'
					'	~{0}playlist <name of a .txt file> - This changed the autoplaylist to a user defined list (if no .txt file is specified the autoplaylist will be NONE). \n'
					'	{0}shuffle - Determines whether the queue should be shuffles (Toggled). \n'
					'	{0}store - Determines whether songs that users play should be added to the current autoplaylist (Toggled). \n'
					'	{0}summon - Summons the bot to the caller\'s voice channel'
					'	~{0}volume (or !v) - Changes the volume level for the entire server. \n\n'

					'COMMANDS FOR EVERYONE \n'
					'	{0}help - Outputs commands for AcaBot. \n'
					'	~{0}np - Outputs information on the song that is currently playing. \n'
					'	~{0}pause - Pauses the currently playing song. \n'
					'	~{0}queue (or \\q) - Outputs the list of songs that users have asked to be played (in order). \n'
					'	~{0}quiet - Mutes AcaBot for a single user (if owner uses the command it mutes the bot for the entire server). \n'
					'	~{0}skip (or !s) - Skips the currently playing song. \n'
					'	~{0}play <YOUTUBE URL> (or !p) - This will queue a song to be played (will be sentence recognition later). \n'
					'	~{0}roll <<number of dice>d<type of dice>> - Will roll a specified dice for the user (example: !roll 5d20 (rolls 5 dice that are 20 sided)). \n' .format(config.Command_Prefix)
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

client.run(config.Token)