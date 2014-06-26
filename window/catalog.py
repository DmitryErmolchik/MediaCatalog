# coding=utf-8

from gi.repository import Gtk, GObject, GLib, Gdk
from gi.repository.GdkPixbuf import Pixbuf
import subprocess
from os import listdir
from os.path import isfile, join, isdir, splitext

class Catalog(GObject.GObject):

    def __init__(self, configuration):
        GObject.GObject.__init__(self)
        self.configuration = configuration
        self.targetPath = None
        self.player = None
        self.currentPath = None
        self.selectedItem = None
        
        self.liststore = Gtk.ListStore(Pixbuf, str, str, bool)

        self.catalogView = Gtk.IconView.new()
        self.catalogView.set_item_width(configuration.getWidth())
        self.catalogView.set_model(self.liststore)
        self.catalogView.set_pixbuf_column(0)
        self.catalogView.set_text_column(1)
        self.catalogView.set_selection_mode(Gtk.SelectionMode.SINGLE)
        
        self.catalogView.connect('item-activated', self.__on_item_activated__)
        self.catalogView.connect('show', self.__on_generate_miniature_finished__)
        self.catalogView.connect('selection-changed', self.__on_selection_changed__)

    def __on_item_activated__(self, iconview, path):
        listiter = self.liststore.get_iter(path)
        value = self.liststore.get_value(listiter, 2)

        if self.liststore.get_value(listiter, 3):
            self.configuration.getLogger().info('Changing current path to: ' + value.decode(self.configuration.getEncoding()))
            self.selectedItem = None
            self.currentPath = value
            self.__loadPath__(self.currentPath)
        else:
            self.configuration.getLogger().info('Play file: ' + value.decode(self.configuration.getEncoding()))
            subprocess.Popen([self.player, value])

    def __on_generate_miniature_finished__(self, iconview):
        self.__loadPath__(self.currentPath)

    def __on_selection_changed__(self, iconView):
        self.configuration.getLogger().debug('Selection changed')
        for item in iconView.get_selected_items():
            self.configuration.getLogger().debug(item)
            self.selectedItem = item

    def __loadPath__(self, path):
        self.liststore.clear()
        needGenerateMiniature = False
        
        for targetDir in self.__getDirs__(path):
            if targetDir == '..':
                pixbuf = Pixbuf.new_from_file_at_size(self.configuration.getTheme().getBackIcon(), self.configuration.getFolderIconSize(), self.configuration.getFolderIconSize())
                backPath = path[0:path.rindex('/')]
                self.liststore.append([pixbuf, '', backPath, True])
            else:
                pixbuf = Pixbuf.new_from_file_at_size(self.configuration.getTheme().getFolderIcon(), self.configuration.getFolderIconSize(), self.configuration.getFolderIconSize())
                self.liststore.append([pixbuf, targetDir, join(path, targetDir), True])

        for targetFile in self.__getFiles__(path):
            miniature = self.__getMiniature__(path, targetFile)
            if (miniature != None):
                try:
                    pixbuf = Pixbuf.new_from_file_at_size(miniature, self.configuration.getFileIconSize(), self.configuration.getFileIconSize())
                except GLib.GError:
                    pixbuf = Pixbuf.new_from_file_at_size(self.configuration.getTheme().getVideoIcon(), self.configuration.getFolderIconSize(), self.configuration.getFolderIconSize())
            else:
                pixbuf = Pixbuf.new_from_file_at_size(self.configuration.getTheme().getVideoIcon(), self.configuration.getFolderIconSize(), self.configuration.getFolderIconSize())
                needGenerateMiniature = True

            self.liststore.append([pixbuf, targetFile, join(path, targetFile), False])

        self.currentPath = path;

        if self.selectedItem != None:
            self.configuration.getLogger().debug('Reset selected item to ' + unicode(self.selectedItem))
            self.catalogView.select_path(self.selectedItem)
            self.catalogView.set_cursor(self.selectedItem, None, False)
            
        if (needGenerateMiniature == True):
            subprocess.Popen(['python', self.configuration.getAppStartDir() + 'worker/miniaturegenerator.py',
                              '-i', self.currentPath, 
                              '-o', self.configuration.getMiniatureDir(), 
                              '-e', self.configuration.getEncoding()])

    def __getFiles__(self, path):
        files = [ f for f in listdir(path) if isfile(join(path,f)) ]
        return sorted(files)
                    
    def __getDirs__(self, path):
        dirs = []
        for f in listdir(path):
            if isdir(join(path,f)):
                dirs.append(f)
        dirs = sorted(dirs)
        if (path != self.targetPath):
            dirs.insert(0, '..')
        return dirs

    def __getMiniature__(self, path, file):
        fileName, fileExtension = splitext(file)
        if fileExtension[1:].lower() in self.configuration.getSupportedImageExtensions():
            return path + '/' + file
        targetFile = self.configuration.getHome() + self.configuration.getAppDir() + '/miniatureCache' + path + '/' + file + '.jpg'
        if (isfile(targetFile)):
            return targetFile
        else:
            return None

    def setTargetPath(self, path):
        self.targetPath = path
        self.currentPath = self.targetPath
        self.__loadPath__(self.currentPath)
    
    def setPlayer(self, player):
        self.player = player

    def redrawCatalogIfNeed(self, path):
        if path == join(self.currentPath, '').decode(self.configuration.getEncoding()):
            self.configuration.getLogger().debug('Redrawing catalog')
            self.catalogView.hide()
            self.catalogView.show()

    def getView(self):
        return self.catalogView