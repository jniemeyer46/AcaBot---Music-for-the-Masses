import configparser

class Config:
	# Holds the commands that do not take any parameters
	GeneralCommands = ['help', 'np', 'pause', 'q', 'queue', 'quiet', 's', 'skip']
	OwnerCommands = ['playlist', 'restart', 'shuffle', 'shutdown', 'store', 'v', 'volume']

	def __init__(self, config_file):
		config = configparser.ConfigParser(interpolation=None)
		config.read(config_file, encoding='utf-8')

		confSections = {"Credentials", "OwnerPermissions", "TrustedPermissions", "TextChannels", "MusicBot"}.difference(config.sections())
		if confSections:
			raise HelpfulError(
				"There seems to be a problem with the configuration sections.",
				"You should have 4 different sections in the settings.ini file, please fix the problem and try again."
			)

		self.Token = config.get('Credentials', 'Token', fallback = DefaultConfigs.Token)
		self.Owner_ID = config.get('OwnerPermissions', 'Owner_ID', fallback = DefaultConfigs.Owner_ID)
		self.Command_Prefix = config.get('TextChannels', 'Command_Prefix', fallback = DefaultConfigs.Command_Prefix)
		self.Volume = config.get('MusicBot', 'Volume', fallback = DefaultConfigs.Default_Volume)
		self.Autoplaylist = config.get('MusicBot', 'Autoplaylist', fallback = DefaultConfigs.Default_Autoplaylist)
		self.Save = config.get('MusicBot', 'Save', fallback = DefaultConfigs.Save_to_Playlist)
		self.Shuffle = config.get('MusicBot', 'Shuffle', fallback = DefaultConfigs.Shuffle_Queue)

		# Make sure all is good
		self.run_checks()
		self.get_autoplaylist()

	def run_checks(self):
		if self.Token is None:
			raise HelpfulError(
				"Sorry, the Token given for your AcaBot is not correct...",
				"Please get the token from 'https://discordapp.com/developers/applications/me' and "
				"place it into the Settings.ini file after 'Token = '."
			)

		if self.Owner_ID is None:
			raise HelpfulError(
				"Sorry, there has to be a valid Owner_ID in order to use AcaBot...",
				"Please fille in the 'Owner_ID = ' field with the server owner's ID "
				"in order to be able to use AcaBot."
			)


class DefaultConfigs:
	# Stores the ID of a server's owner
	Owner_ID = None
	# Stores the token for the bot
	Token = None

	# Default command prefix that is used to determine a bot command
	Command_Prefix = '\\'

	# Default volume
	Default_Volume = 0.10
	# No playlist will play if the owner does not set one
	Default_Autoplaylist = None
	# Whether or not the user queued songs will be stored
	Save_to_Playlist = False
	# Whether the user queued songs will be shuffled
	Shuffle_Queue = False

	# File of settings
	Settings = 'configs/Settings.ini'

