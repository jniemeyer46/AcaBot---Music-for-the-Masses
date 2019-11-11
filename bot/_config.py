from configparser import ConfigParser

class Config:
    def __init__(self, configFile='../configs/settings.ini'):
        config = ConfigParser()
        config.read(configFile, encoding='utf-8')
        confSections = {
            'Credentials',
            'Permissions',
            'MusicBot'
        }.difference(config.sections())

        if confSections:
            raise KeyError(
                "There seems to be a problem with the configuration sections.",
                "You should have 3 different sections in the settings.ini file, please fix the problem and try again."
            )

        # Holds the commands that do not take any parameters
        OwnerCommands = ['pause', 'restart', 'shutdown']
        TrustedCommands = ['clean', 'deletenp', 'disconnect', 'playlist', 'shuffle', 'store', 'summon', 'v', 'volume']
        GeneralCommands = ['help', 'np', 'p', 'play', 'q', 'queue', 'roll', 's', 'skip']

        # Playlists
        autoplaylist = []

        # Used to make sure the bot doesnt repeat songs too often
        coolDownQueue = []

        # .get commands
        self.botToken = config.get('Credentials', 'botToken', fallback=None)

        self.ownerID = config.get('Permissions', 'ownerID', fallback=None)
        self.rolePermissions = config.get('Permissions', 'rolePermissions', fallback='Owner')

        self.commandPrefix = config.get('MusicBot', 'commandPrefix', fallback='\\')
        self.volume = config.getfloat('MusicBot', 'volume', fallback=0.95)
        self.cooldownQueueSizePercent = config.getfloat('MusicBot', 'cooldownQueueSizePercent', fallback=0.95)
        self.autoplayListName = config.get('MusicBot', 'autoplaylist', fallback='defaultPlaylist.txt')
        self.saveQueuedSongs = config.getboolean('MusicBot', 'saveQueuedSongs', fallback=False)

        self.errorChecks()

        self.createAutoplaylist()

    def errorChecks(self):
        if self.botToken is None:
            raise NameError(
                "Sorry, the Token given for your AcaBot is not correct...",
                "Please get the token from 'https://discordapp.com/developers/applications/me' and "
                "place it into the Settings.ini file after 'Token = '."
            )

        if self.ownerID is None:
            raise NameError(
                "Sorry, there has to be a valid Owner_ID in order to use AcaBot...",
                "Please fille in the 'Owner_ID = ' field with the server owner's ID "
                "in order to be able to use AcaBot."
            )

    def createAutoplaylist(self):
        if self.autoplayListName is not None and self.autoplayListName != 'None':
            try:
                if '.txt' not in self.autoplayListName:
                    self.autoplayListName = self.autoplayListName + '.txt'

                with open('../playlists/' + self.autoplayListName) as f:
                    self.autoplaylist = f.read().split()

                print(self.autoplayListName)
                print(self.autoplaylist)
            except NameError:
                print("There seems to be a problem with the Autoplaylist you have set in the Settings.ini file")

if __name__ == '__main__':
    testConfig = Config()
