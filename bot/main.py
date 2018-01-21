import sys
import random
import discord
import asyncio
import configparser
from discord.ext import commands

import config

client = discord.Client()

@client.event
async def on_ready():
	print('%s has logged into the discord channel' % client.user.name)


@client.event
async def on_message(message):
	# Grabs message content, makes it all lowercase, and stores it in a variable
	msg = message.content.lower()


	'''------OWNER COMMANDS------'''

	# Makes sure the owner of the server is the one using the command
	if str(message.author.id) == str(config.OWNER_ID):
		await client.send_message(message.channel, "Test")

		# Deals with commands that do not have extra parameters (EX: the shutdown command)
		if msg[1:] in config.OwnerCommands:
			await client.send_message(message.channel, "Testing")
			'''# User enters a new playlist file for the bot to pull from (if empty it will not use an autoplaylist)
			if msg.startswith('!playlist'):
				pass

			# This will restart the bot incase a problem occurs and it needs to be restarted (No clue how to do this one yet)
			elif msg == '!restart':
				print("Hello")

			# Toggles shuffle for the queue
			elif msg == '!shuffle':
				pass

			# Shuts down the bot (Not the correct way to do this, need to look into it still...  Technically works though atm)
			elif msg == '!shutdown':
				sys.exit(0)

			# Toggles storing the youtube videos into the current autoplaylist (should not add duplicates)
			elif msg == '!store':
				pass

			# Summons the bot to the the caller's voice channel
			elif msg == '!summon':
				await summon(ctx.message.author.voice_channel)

			# Outputs the current volume level or allows adjustment of volume level
			elif msg.startswith('!v'):
				pass'''

	'''------TRUSTED COMMANDS------'''

	'''elif message.author.id in TRUSTED_IDS:
		pass

	'''



	'''------GENERAL COMMANDS------'''

	# Check if the user message is a command for the bot not including the commands that take extra perameters
	'''elif msg in Globals.GeneralCommands:
		# Outputs information about the song that is currently playing
		if msg == '!help':
			await client.send_message(message.channel, 
					"~ - means that functionality has not yet been implemented as of yet. \n\n"

					"OWNER SPECIFIC COMMANDS \n"
					"	~!playlist <name of a .txt file> - This changed the autoplaylist to a user defined list (if no .txt file is specified the autoplaylist will be NONE). \n"
					"	~!restart - restarts the bot. \n"
					"	~!shuffle - Determines whether the queue should be shuffles (Toggled). \n"
					"	!shutdown - Kills AcaBot, RIP. \n"
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
		elif msg == '!np':
			pass

		# Pause the bot (Not sure if I want everyone to be able to do this or not)
		elif msg == '!pause':
			pass

		# Outputs the list of songs that have been queued by people in the discord channel
		elif msg == '!q' or msg == '!queue':
			await client.send_message(message.channel, "Testing")

		# If the owner uses this command it will mute the bot for the entire channel
		# If anyone else uses this command it will only mute the bot for them alone
		elif msg == '!quiet':
			pass

		# Skips the current song
		elif msg == '!s' or msg == '!skip':
			pass

	# User enters a youtube link to be played
	elif msg.startswith('!p'):
		counter = 0
		tmp = await client.send_message(message.channel, 'Calculating messages...')
		async for log in client.logs_from(message.channel, limit=100000):
			counter += 1

		await client.edit_message(tmp, 'You have {} messages.' .format(counter))

	# User enters a new playlist file for the bot to pull from
	elif msg.startswith('!roll'):
		pass


async def summon(self, ctx):
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


client.run('Mzk3NTE0MTc5NzE3NzU4OTc3.DUZvcw.vdWbZ5ZaChfVLB-SfqIR85LgLYQ')