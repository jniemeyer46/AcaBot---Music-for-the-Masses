import configparser

class Config:
	# Holds the commands that do not take any parameters
	OwnerCommands = ['shutdown', 'testing']
	TrustedCommands = ['delete','playlist', 'shuffle','store', 'summon', 'v','volume']
	GeneralCommands = ['help', 'np', 'pause', 'p', 'play', 'q', 'queue', 'quiet', 'roll', 's', 'skip']

	# Playlists
	Autoplaylist = []
	# Where the playlist is eventually saved
	Userplaylist = []

	# Used to make sure the bot doesnt repeat songs too often
	CoolDownQueue = []

	def __init__(self, config_file):
		config = configparser.ConfigParser(interpolation=None)
		config.read(config_file, encoding='utf-8')

		confSections = {"Credentials", "OwnerPermissions", "TrustedPermissions", "TextChannels", "MusicBot"}.difference(config.sections())

		if confSections:
			raise Error(
				"There seems to be a problem with the configuration sections.",
				"You should have 4 different sections in the settings.ini file, please fix the problem and try again."
			)

		# .get commands
		self.Token = config.get('Credentials', 'Token', fallback = DefaultConfigs.Token)
		self.Owner_ID = config.get('OwnerPermissions', 'Owner_ID', fallback = DefaultConfigs.Owner_ID)
		self.Role_Permissions = config.get('TrustedPermissions', 'Role_Permissions', fallback = DefaultConfigs.Default_Role_Permissions).split(' ')
		self.Trusted_Permissions = config.get('TrustedPermissions', 'Trusted_Permissions', fallback = DefaultConfigs.Default_Trusted_Permissions)
		self.Command_Prefix = config.get('TextChannels', 'Command_Prefix', fallback = DefaultConfigs.Command_Prefix)
		self.AutoplaylistName = config.get('MusicBot', 'Autoplaylist', fallback = DefaultConfigs.Default_Autoplaylist)

		# .getfloat commands
		self.Volume = config.getfloat('MusicBot', 'Volume', fallback = DefaultConfigs.Default_Volume)

		# .getint commands
		self.CoolDownQueueSize = config.getfloat('MusicBot', 'CoolDownQueueSize', fallback = DefaultConfigs.DefaultCoolDownQueueSize)

		# .getboolean commands
		self.Store = config.getboolean('MusicBot', 'Save', fallback = DefaultConfigs.Save_to_Playlist)
		self.Shuffle = config.getboolean('MusicBot', 'Shuffle', fallback = DefaultConfigs.Shuffle_Queue)

		# Make sure all is good
		self.checks()

		# Create a list containing links to youtube videos
		self.Create_Autoplaylist()

		# Create the list of Trusted_Permissions
		self.Create_Trusted_List()


	def Create_Autoplaylist(self):
		if self.AutoplaylistName is not None and self.AutoplaylistName != 'None':
			if '.txt' in self.AutoplaylistName:
				with open('playlists/' + self.AutoplaylistName) as f:
					self.Autoplaylist = f.read().split()

			elif '.txt' not in self.AutoplaylistName:
				with open('playlists/' + self.AutoplaylistName + '.txt') as f:
					self.Autoplaylist = f.read().split()
			else:
				raise Error(
					"There seems to be a problem with the Autoplaylist you have set in the Settings.ini file")


	def Create_Trusted_List(self):
		if self.Trusted_Permissions is not None:
			with open('configs/' + self.Trusted_Permissions + '.txt') as f:
				self.Trusted_Permissions = f.read().split()


	def checks(self):
		if self.Token is None:
			raise Error(
				"Sorry, the Token given for your AcaBot is not correct...",
				"Please get the token from 'https://discordapp.com/developers/applications/me' and "
				"place it into the Settings.ini file after 'Token = '."
			)

		if self.Owner_ID is None:
			raise Error(
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

	# Trusted people on the server
	Default_Role_Permissions = None
	Default_Trusted_Permissions = None

	# Default volume
	Default_Volume = 0.10
	# Default Cool Down Queue Size
	DefaultCoolDownQueueSize = 75
	# No playlist will play if the owner does not set one
	Default_Autoplaylist = None
	# Whether or not the user queued songs will be stored
	Save_to_Playlist = True
	# Whether the user queued songs will be shuffled
	Shuffle_Queue = False

	# File of settings
	Settings = 'configs/PersonalSettings.ini'

