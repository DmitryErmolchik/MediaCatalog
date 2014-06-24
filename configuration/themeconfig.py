# coding=utf-8

from os import listdir
from os.path import isfile, isdir, join
from sys import exit

class ThemeConfig(object):

    def __init__(self, baseFolder, logger, encoding):
        self.logger = logger
        self.encoding = encoding
        self.name = None
        self.baseFolder = baseFolder
        self.backIcon = None
        self.folderIcon = None
        self.videoIcon = None
    
    def setBaseFolder(self, baseFolder):
        self.baseFolder = baseFolder
        
    def getThemeFolders(self):
        try:
            dirs = []
            for f in listdir(self.baseFolder):
                if isdir(join(self.baseFolder,f)):
                    dirs.append(join(self.baseFolder, f))
            dirs = sorted(dirs)
            if len(dirs) != 0:
                return dirs
            else:
                self.logger.error(u'No themes directories found')
                exit(1) 
        except OSError as e:
            self.logger.error(str(e).decode(self.encoding))
            exit(1)
    
    def readTheme(self, themeFolder):
        if isdir(themeFolder) and isfile(join(themeFolder, 'theme.cfg')):
            i = 0
            for line in open(join(themeFolder, 'theme.cfg')).read().splitlines():
                pos = line.find('#')
                if pos != -1:
                    line = line[0:pos]
                if line != "":
                    words = line.strip().split()
                    if words[0].lower() == 'name':
                        self.name = line[len(words[0]):].strip()
                    elif words[0].lower() == 'back':
                        self.backIcon = join(themeFolder, line[len(words[0]):].strip())
                    elif words[0].lower() == 'folder':
                        self.folderIcon = join(themeFolder, line[len(words[0]):].strip())
                    elif words[0].lower() == 'video':
                        self.videoIcon = join(themeFolder, line[len(words[0]):].strip())

        else:
            self.logger.error('Can not find theme configuration file "' + join(themeFolder, 'theme.cfg') + '"')
            exit(1)
    
    def getName(self):
        return self.name
    
    def getBackIcon(self):
        return self.backIcon
    
    def getFolderIcon(self):
        return self.folderIcon
    
    def getVideoIcon(self):
        return self.videoIcon