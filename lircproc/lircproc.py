# coding=utf-8

import os.path
import pylirc
import subprocess
from os import getpid
import sys

class LircProc(object):
    def __init__(self, configuration):
        self.configuration = configuration
        self.initialized = False
        self.blocking = 1;
        self.config = ''
        if (os.path.isfile(self.configuration.getHome() + '/.lircrc')):
            self.config = self.configuration.getHome() + '/.lircrc'
        else:
            self.config = '/etc/lirc/lircrc'
        configuration.getLogger().info('Reading config from: ' + self.config)

    def startRemoteControll(self, dataQueue):
        dataQueue.put(['pid', getpid()])
        try:
            if(pylirc.init('mediacatalog', self.config, self.blocking)):
                self.configuration.getLogger().info('Remote control process was started')
                dataQueue.put(['status', 0])
                code = ""
                isTerminate = False
                DEVNULL = open(os.devnull, 'w')
                while not isTerminate:
                    codesList = pylirc.nextcode(1)
                    out = subprocess.Popen(['/bin/sh', '-c', 'ps -ae | grep `xdotool getwindowfocus getwindowpid` | grep mediacatalog.py'], stdout=subprocess.PIPE)
                    isHasFocus = out.communicate()[0].rstrip()
                    if (isHasFocus != ""):
                        self.configuration.getLogger().debug('Application has focus')
                        if(codesList):
                            for code in codesList:
                                self.configuration.getLogger().info('Command: %s, Repeat: %d' % (code['config'], code['repeat']))
                                if code['config'] != None:
                                    if code['repeat'] > 1:
                                        for i in range(code['repeat']-1):
                                            xmacroProc = subprocess.Popen(['xmacroplay', ':0.0'], stdin=subprocess.PIPE, stdout=DEVNULL, stderr=subprocess.STDOUT)
                                            xmacroProc.communicate('KeyStrPress ' + code['config'] + ' KeyStrRelease ' + code['config'])
                                    else:
                                        xmacroProc = subprocess.Popen(['xmacroplay', ':0.0'], stdin=subprocess.PIPE, stdout=DEVNULL, stderr=subprocess.STDOUT)
                                        xmacroProc.communicate('KeyStrPress ' + code['config'] + ' KeyStrRelease ' + code['config'])
                    else:
                        self.configuration.getLogger().debug('Application has not focus')
        except RuntimeError:
            dataQueue.put(['status', 1])
            self.configuration.getLogger().error('Remote control not initialized')
            self.configuration.getLogger().error(sys.exc_info()[1])
    