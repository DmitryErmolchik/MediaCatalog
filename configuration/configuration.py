# coding=utf-8

from os.path import isfile, isdir, expanduser, dirname, join, abspath
import sys
from gi.repository.GdkPixbuf import Pixbuf
from os import makedirs
from configuredlogger import ConfigureLogger

class Configuration(object):

    def __init__(self):
        self.categories = []
        self.selectedCategory = 0;
        self.player = None
        self.fileIconSize = 64
        self.folderIconSize = 64
        self.appDir = '/.mediacatalog'
        self.miniatureCache = '/miniatureCache'
        self.appStartDir = join(abspath(dirname(sys.argv[0])), '')
        self.extensions = self.__initAvailablePicturesExtensions__()
        self.configFile = '/mediacatalog.conf'
        self.logFile = '/tmp/mediacatalog.log'
        self.home = expanduser('~')
        self.encoding = 'utf-8'
        self.logLevel = 'info'
        self.enableConsoleLog = False

        parseCategory = False
        name = None
        path = None
        if (isdir(self.home + self.appDir) and isfile(self.home + self.appDir + self.configFile)):
            i = 0
            for line in open(self.home + self.appDir + self.configFile).read().splitlines():
                pos = line.find('#')
                if pos != -1:
                    line = line[0:pos]
                if line != "":
                    words = line.strip().split()
                    if not parseCategory:
                        if words[0].lower() == 'category':
                            parseCategory = True
                            name = None
                            path = None
                        elif words[0].lower() == 'player':
                            self.player = line[len(words[0]):].strip()
                        elif words[0].lower() == 'fileiconsize':
                            self.fileIconSize = int(line[len(words[0]):].strip())
                        elif words[0].lower() == 'foldericonsize':
                            self.folderIconSize = int(line[len(words[0]):].strip())
                        elif words[0].lower() == 'logfile':
                            self.logFile = line[len(words[0]):].strip()
                        elif words[0].lower() == 'encoding':
                            self.encoding = line[len(words[0]):].strip()
                        elif words[0].lower() == 'loglevel':
                            self.logLevel = line[len(words[0]):].strip().upper()
                        elif words[0].lower() == 'enableconsolelog' and line.strip()[len(words[0]):].strip().lower() == 'true':
                            self.enableConsoleLog = True
                    elif parseCategory:
                        if words[0].lower() == 'name':
                            name = line.strip()[len(words[0]):].strip()
                        elif words[0].lower() == 'path':
                            path = line.strip()[len(words[0]):].strip()
                        elif words[0].lower() == 'selected' and line.strip()[len(words[0]):].strip().lower() == 'true':
                            self.selectedCategory = i;
                        elif words[0].lower() == 'end':
                            self.categories.append({'name' : name, 'path': path})
                            parseCategory = False
                            i += 1
        else:
            sys.stderr.write('Can not find configuration file at "' + self.home + self.appDir + self.configFile + '"')
            sys.exit(1)

        if (not isdir(self.getMiniatureDir())):
            makedirs(self.getMiniatureDir())
        
        self.logger = ConfigureLogger(self.logFile)
        if self.enableConsoleLog:
            self.logger.plugOnConsoleHandler()

        # Log data from config file
        if self.player == None or self.player == '':
            self.logger.getLogger().error('Player command not found in configuration file. Please add "Player <player command>" to "' + self.home + self.appDir + self.configFile + '"')
            exit(1)
        self.logger.getLogger().info('Player: ' + self.player)
        self.logger.getLogger().info('FileIconSize: ' + unicode(self.fileIconSize))
        self.logger.getLogger().info('FolderIconSize: ' + unicode(self.folderIconSize))
        self.logger.getLogger().info('Logfile: ' + self.logFile)
        self.logger.getLogger().info('Encoding: ' + self.encoding)
        self.logger.getLogger().info('LogLevel: ' + self.logLevel)
        self.logger.getLogger().info('EnableConsoleLog: ' + unicode(self.enableConsoleLog))
        
        if len(self.categories) > 0:
            self.logger.getLogger().info('Categories:')
            for category in self.categories:
                self.logger.getLogger().info('Name: ' + category['name'].decode(self.encoding) + '   Path: ' + category['path'].decode(self.encoding))
            self.logger.getLogger().info('Selected category: ' + unicode(self.selectedCategory) + " (" + self.categories[self.selectedCategory]['name'].decode(self.encoding) + ")")
        else:
            self.logger.getLogger().error('No categories found. Please add category to "' + self.home + self.appDir + self.configFile + '"')
            exit(1)
            
        self.logger.setLogLevel(self.logLevel)

    def __initAvailablePicturesExtensions__(self):
        extensions = []
        formats = Pixbuf.get_formats ()
        for picFormat in formats:
            for extension in picFormat.get_extensions():
                extensions.append(extension)
        return extensions

    def getCategories(self):
        return self.categories
    
    def getSelectedCategory(self):
        return self.selectedCategory
    
    def getPlayer(self):
        return self.player
    
    def getAppDir(self):
        return self.appDir
    
    def getFileIconSize(self):
        return self.fileIconSize
    
    def getFolderIconSize(self):
        return self.folderIconSize
    
    def getAppStartDir(self):
        return self.appStartDir
    
    def getSupportedImageExtensions(self):
        return self.extensions
    
    def getMiniatureDir(self):
        return join(self.home + self.appDir + self.miniatureCache, '')
    
    def getLogger(self):
        return self.logger.getLogger()
    
    def getHome(self):
        return self.home
    
    def getEncoding(self):
        return self.encoding
    
    def getLogFile(self):
        return self.logFile