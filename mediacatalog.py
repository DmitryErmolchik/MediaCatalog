#!/usr/bin/python
# coding=utf-8

from gi.repository import Gtk, GObject
from window import mainwindow
from configuration import configuration
from lircproc import lircproc
from multiprocessing import Process, Queue
import sys
import time
from os import kill
import signal
from dbus.mainloop.glib import DBusGMainLoop
from worker.dbuslistener import MediaplaceDBUSService

GObject.threads_init()
configuration = configuration.Configuration()
categories = []
player = None
selectedCategory = 0
remoteProcesse=None
dataQueue = Queue()
lircProcPid = None
lircProcStatus = None


def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

if (module_exists('pylirc')):
    configuration.getLogger().info('LIRC module was loaded')
    try:
        proc = lircproc.LircProc(configuration);
        remoteProcesse = Process(target = proc.startRemoteControll, args=(dataQueue,))
        remoteProcesse.start()
        lircProcPid = dataQueue.get()[1]
        lircProcStatus = dataQueue.get()[1]
    except RuntimeError as e:
        sys.stderr.write(str(e) + "\n")

else:
    print('Media catalog started without LIRC support')

win = mainwindow.MainWindow(configuration)

DBusGMainLoop(set_as_default=True)
dbusService = MediaplaceDBUSService(win, configuration)
time.sleep(0.5)

win.addCategories(configuration.getCategories())
win.activateCategory(configuration.getSelectedCategory())
win.connect('delete-event', Gtk.main_quit)
win.show_all()

Gtk.main()

if lircProcPid != None and lircProcStatus == 0:
    configuration.getLogger().info('Killing remote control process. Sending signal ' + unicode(signal.SIGKILL) + ' to process ' + unicode(lircProcPid))
    kill(lircProcPid, signal.SIGKILL)
    time.sleep(1)