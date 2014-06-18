# coding=utf-8

import logging
from os import renames
from os.path import isfile

class ConfigureLogger(object):

    def __init__(self, logFile):
        self.logger = logging.getLogger('MediaCatalog')
        
        if isfile(logFile):
            renames(logFile, logFile + ".old")
        
        self.fileHandler = logging.FileHandler(logFile)
        self.fileHandler.setFormatter(logging.Formatter(u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s'))
        
        self.consoleHandler = logging.StreamHandler()
        self.consoleHandler.setFormatter(logging.Formatter(u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s'))
        
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.fileHandler)
    
    def getLogger(self):
        return self.logger
    
    def setLogLevel(self, logLevel):
        if logLevel == 'CRITICAL':
            self.logger.setLevel(logging.CRITICAL)
        elif logLevel == 'ERROR':
            self.logger.setLevel(logging.ERROR)
        elif logLevel == 'WARN' or logLevel == 'WARNING':
            self.logger.setLevel(logging.WARNING)
        elif logLevel == 'INFO':
            self.logger.setLevel(logging.INFO)
        elif logLevel == 'DEBUG':
            self.logger.setLevel(logging.DEBUG)
    
    def plugOnConsoleHandler(self):
        self.logger.addHandler(self.consoleHandler)
        
    def plugOffConsoleHandler(self):
        self.logger.removeHandler(self.consoleHandler)

    def plugOnFileHandler(self):
        self.logger.addHandler(self.fileHandler)
        
    def plugOffFileHandler(self):
        self.logger.removeHandler(self.fileHandler)