import sys
import random
import discord
import asyncio
from discord.ext import commands

from config import Config, DefaultConfigs
#from personal_config import Config, DefaultConfigs


# Stores the file that has the user input settings
config_file = DefaultConfigs.Settings

# Discord client connection
client = discord.Client()
# Holds all of AcaBot's configurations
config = Config(config_file)


@client.event
async def on_ready():
	print('%s has logged into the discord channel' % client.user.name)


@client.event
async def on_message(message):
	msg = message.content.lower()

	# Determine whether the message was a command for the bot, parse out the Command_Prefix
	if msg.startswith(config.Command_Prefix):
		# Grabs message content, makes it all lowercase, and stores it in a variable
		msg = msg[1:]
	else:
		return


	'''------OWNER COMMANDS------'''

	# Makes sure the GIVEN owner of the server is the one using the command
	if msg in config.OwnerCommands:
		if str(message.author.id) == config.Owner_ID:
			# User enters a new playlist file for the bot to pull from (if empty it will not use an autoplaylist)
			if msg.startswith('playlist'):
				pass

			# This will restart the bot incase a problem occurs and it needs to be restarted (No clue how to do this one yet)
			elif msg == 'restart':
				print("This will not be implemented until the very end most likely.")

			# Shuts down the bot (Not the correct way to do this, need to look into it still...  Technically works though atm)
			elif msg == 'shutdown':
				sys.exit(0)


	'''------TRUSTED COMMANDS------'''

	# Makes sure that only TRUSTED users can use these commands
	if msg in config.TrustedCommands:
		if config.Trusted_Permissions is None and str(message.author.top_role) in config.Role_Permissions:
			# Toggles shuffle for the queue
			if msg == 'shuffle':
				pass

			# Toggles storing the youtube videos into the current autoplaylist (should not add duplicates)
			elif msg == 'store':
				pass

			# Summons the bot to the the caller's voice channel
			elif msg == 'summon':
				pass

			elif msg.startswith('v'):
				pass
		elif message.author.id in config.Trusted_Permissions:
			# Toggles shuffle for the queue
			if msg == 'shuffle':
				pass

			# Toggles storing the youtube videos into the current autoplaylist (should not add duplicates)
			elif msg == 'store':
				pass

			# Summons the bot to the the caller's voice channel
			elif msg == 'summon':
				pass

			elif msg.startswith('v'):
				pass	
	

	'''------GENERAL COMMANDS------'''

	# Check for GENERAL command usage
	if msg in config.GeneralCommands:
		# Outputs information about the song that is currently playing
		if msg == 'help':
			await client.send_message(message.channel, 
					"~ - means that functionality has not yet been implemented as of yet. \n\n"

					"OWNER SPECIFIC COMMANDS \n"
					"	~!playlist <name of a .txt file> - This changed the autoplaylist to a user defined list (if no .txt file is specified the autoplaylist will be NONE). \n"
					"	~!restart - restarts the bot. \n"
					"	!shutdown - Kills AcaBot, RIP. \n\n"

					"TRUSTED USER COMMANDS \n"
					"	~!shuffle - Determines whether the queue should be shuffles (Toggled). \n"
					"	~!store - Determines whether songs that users play should be added to the current autoplaylist (Toggled). \n"
					"	~!summon - Summons the bot to the caller's voice channel"
					"	~!volume (or !v) - Changes the volume level for the entire server. \n\n"

					"COMMANDS FOR EVERYONE \n"
					"	!help - Outputs the bot's commands. \n"
					"	~!np - Outputs information on the song that is currently playing. \n"
					"	~!pause - Pauses the currently playing song. \n"
					"	~!queue (or !q) - Outputs the list of songs that users have asked to be played (in order). \n"
					"	~!quiet - Mutes the bot for a single user (if owner uses the command it mutes the bot for the entire server). \n"
					"	~!skip (or !s) - Skips the currently playing song. \n"
					"	~!play <YOUTUBE URL> (or !p) - This will queue a song to be played (will be sentence recognition later). \n"
					"	~!roll <<number of dice>d<type of dice>> - Will roll a specified dice for the user (example: !roll 5d20 (rolls 5 dice that are 20 sided)). \n"	
				)

		# Outputs information about the song that is currently playing
		elif msg == 'np':
			pass

		# Pause the bot (Not sure if I want everyone to be able to do this or not)
		elif msg == 'pause':
			pass

		# Outputs the list of songs that have been queued by people in the discord channel
		elif msg == 'q' or msg == 'queue':
			await client.send_message(message.channel, "Testing")

		# If the owner uses this command it will mute the bot for the entire channel
		# If anyone else uses this command it will only mute the bot for them alone
		elif msg == 'quiet':
			pass

		# Skips the current song
		elif msg == 's' or msg == 'skip':
			pass

		# User enters a youtube link to be played
		elif msg.startswith('p'):
			counter = 0
			tmp = await client.send_message(message.channel, 'Calculating messages...')
			async for log in client.logs_from(message.channel, limit=100000):
				counter += 1

			await client.edit_message(tmp, 'You have {} messages.' .format(counter))

		# User enters a new playlist file for the bot to pull from
		elif msg.startswith('roll'):
			pass


'''async def summon(self, ctx):
	summoned_channel = ctx.message.author.voice_channel
	if summoned_channel is None:
		await self.bot.say('You are not currently in a voice channel')
		return False

	state = self.get_voice_state(ctx.message.server)
	if state.voice is None:
		state.voice = await self.bot.join_voice_channel(summoned_channel)
	else:
		await state.voice.move_to(summoned_channel)

	return True
'''

client.run(config.Token)