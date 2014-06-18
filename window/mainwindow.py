# coding=utf-8

from gi.repository import Gtk
from window.categoriesbox import CategoriesBox
from window.catalog import Catalog

class MainWindow(Gtk.Window):
    def __init__(self, configuration):
        Gtk.Window.__init__(self, title=u'Media catalog')

        self.set_size_request(1280, 720)
        self.maximize()
        # self.fullscreen()
        
        vPaned = Gtk.VPaned()
        self.add(vPaned)

        self.categoriesBox = CategoriesBox(configuration)
        
        self.catalog = Catalog(configuration)
        self.categoriesBox.setCatalog(self.catalog)
        self.catalog.setPlayer(configuration.getPlayer())

        self.scrolledWindow = Gtk.ScrolledWindow()
        self.scrolledWindow.add(self.catalog.getView())
        self.scrolledWindow.hide()
        
        vPaned.add1(self.categoriesBox)
        vPaned.add2(self.scrolledWindow)
    
        self.catalog.getView().grab_focus()

    def addCategories(self, categories):
        for category in categories:
            self.categoriesBox.addCategory(category["name"], category["path"])
    
    def activateCategory(self, categoryNumber=0):
        self.categoriesBox.activateButton(categoryNumber)

    def getCatalog(self):
        return self.catalog