# coding=utf-8

from gi.repository import Gtk

class CategoriesBox(Gtk.Box):
    def __init__(self, configuration):
        Gtk.Box.__init__(self)
        self.catalog = None
        self.categoriesButtons = []
        self.set_spacing(5)
        self.configuration = configuration

    def addCategory(self, name, path):
        self.button = Gtk.ToggleButton(label = name)
        self.button.connect('toggled', self.on_button_toggled, path)
        self.categoriesButtons.append(self.button)
        self.pack_start(self.button, True, True, 0)

    def setCatalog(self, catalog):
        self.catalog = catalog

    def activateButton(self, buttonPosition=0):
        if len(self.categoriesButtons) > 0:
            if buttonPosition < len(self.categoriesButtons):
                self.categoriesButtons[buttonPosition].set_active(True)
            else:
                self.categoriesButtons[0].set_active(True)

    def on_button_toggled(self, button, path):
        if button.get_active():
            self.configuration.getLogger().info(u'Button with path "' + path.decode(self.configuration.getEncoding()) + u'" was pushed')
            for item in self.categoriesButtons:
                if item != button:
                    item.set_active(False)
                else:
                    if self.catalog != None:
                        self.catalog.setTargetPath(path)
                        self.configuration.getLogger().info('"' + path.decode(self.configuration.getEncoding()) + u'" activated')
        else:
            hasPushed = False
            for item in self.categoriesButtons:
                if button != item and item.get_active():
                    hasPushed = True
            if not hasPushed:
                button.set_active(True)
