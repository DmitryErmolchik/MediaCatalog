# coding=utf-8

import dbus
import dbus.service

class MediaplaceDBUSService(dbus.service.Object):
    def __init__(self, mainWindow, configuration):
        bus_name = dbus.service.BusName('com.dim4tech.mediaplace', bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/com/dim4tech/mediaplace')
        
        self.mainWindow = mainWindow
        self.configuration = configuration

    @dbus.service.method('com.dim4tech.mediaplace')
    def redrawCatalog(self, path):
        self.configuration.getLogger().info('Miniature generated for path: '+  path)
        self.mainWindow.getCatalog().redrawCatalogIfNeed(path)

    @dbus.service.method('com.dim4tech.mediaplace')
    def logMessage(self, message, logLevel):
        if logLevel.upper() == 'CRITICAL':
            self.configuration.getLogger().critical(message)
        elif logLevel.upper() == 'ERROR':
            self.configuration.getLogger().error(message)
        elif logLevel.upper() == 'WARN' or logLevel.upper() == 'WARNING':
            self.configuration.getLogger().warning(message)
        elif logLevel.upper() == 'INFO':
            self.configuration.getLogger().info(message)
        elif logLevel.upper() == 'DEBUG':
            self.configuration.getLogger().debug(message)