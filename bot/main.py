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

AcaBot = MusicBot(client, config.Volume, config.AutoplaylistName)

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
					pass


		'''------TRUSTED COMMANDS------'''

		# Makes sure that only TRUSTED users can use these commands
		if msg[0] in config.TrustedCommands:
			if ((config.Role_Permissions is not None and config.Trusted_Permissions is None) and str(message.author.top_role) in config.Role_Permissions) or (config.Trusted_Permissions is not None and str(message.author.id) in config.Trusted_Permissions):
				# Delete all of the bot's previous outputs
				if msg[0] == 'delete':
					await functions.cleanChat(client, config, message, 0)

				elif msg[0] == 'deletenp':
					await AcaBot.deleteAndSkipNP(client, config, message)

				elif msg[0] == 'disconnect':
					await AcaBot.disconnect()

				# User enters a new playlist file for the bot to pull from (if empty it will not use an autoplaylist)
				elif msg[0] == 'playlist':
					await AcaBot.switchPlaylists(client, config, message)

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
					await AcaBot.volumeController(client, message)


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
						'	{0}disconnect - stops the music streaming and disconnects AcaBot from voice. \n'
						'	{0}playlist <name of a .txt file> - This changed the autoplaylist to a user defined list (if no .txt file is specified the autoplaylist will be NONE). \n'
						'	{0}shuffle - Determines whether the queue should be shuffles (Toggled). \n'
						'	{0}store - Determines whether songs that users play should be added to the current autoplaylist (Toggled). \n'
						'	{0}summon - Summons the bot to the caller\'s voice channel'
						'	{0}volume (or !v) - Changes the volume level for the entire server. \n\n'

						'COMMANDS FOR EVERYONE \n'
						'	{0}help - Outputs commands for AcaBot. \n'
						'	{0}np - Outputs information on the song that is currently playing. \n'
						'	{0}queue (or {0}q) - Outputs the list of songs that users have asked to be played (in order). \n'
						'	~{0}quiet - Mutes AcaBot for a single user (if owner uses the command it mutes the bot for the entire server). \n'
						'	{0}skip (or {0}s) - Skips the currently playing song. \n'
						'	{0}play <YOUTUBE URL> (or {0}p) - This will queue a song to be played (will be sentence recognition later). \n'
						'	~{0}roll <<number of dice>d<type of dice>> - Will roll a specified dice for the user (example: !roll 5d20 (rolls 5 dice that are 20 sided)). \n' .format(config.Command_Prefix)
					)

			# Outputs information about the song that is currently playing
			elif msg[0] == 'np':
				await AcaBot.nowPlaying(client, message)

			# Outputs the list of songs that have been queued by people in the discord channel
			elif msg[0] == 'q' or msg[0] == 'queue':
				await AcaBot.displayQueue(client, message)	

			# Skips the current song
			elif msg[0] == 's' or msg[0] == 'skip':
				await AcaBot.skipSong()

			# User enters a youtube link to be played ADD STORE HERE
			elif msg[0] == 'p' or msg[0] == 'play':
				await AcaBot.play(client, config, message)
				
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