#!/usr/bin/python
# coding=utf-8

import sys
import getopt
import subprocess
from os import listdir, makedirs
from os.path import isfile, join, isdir, abspath
import dbus

class MiniatureGenerator(object):
    
    def __init__(self, miniatureDir, encoding):
        self.miniatureDir = miniatureDir
        self.encoding = encoding
        #get the session bus
        bus = dbus.SessionBus()
        #get the object
        theObject = bus.get_object('com.dim4tech.mediaplace', '/com/dim4tech/mediaplace')
        #get the interface
        self.theInterface = dbus.Interface(theObject, 'com.dim4tech.mediaplace')
        
    def generateMiniature(self, workingDir):
        store = self.miniatureDir + workingDir[1:]
        self.log('Generating miniatures to: ' + store.decode(self.encoding), 'info')
        if (not isdir(store)):
            makedirs(store)

        for mediaFile in self.__getFiles__(workingDir):    
            targetFile = store + '/' + mediaFile + '.jpg'
            if (not isfile(targetFile)):
                if (subprocess.call(['ffmpegthumbnailer', '-i', join(workingDir, mediaFile), '-o', targetFile, '-q', '10', '-s', '0']) == 0):
                    self.log('File ' + targetFile.decode(self.encoding) + ' generated', 'debug')
            else:
                self.log('File ' + targetFile.decode(self.encoding) + ' exists', 'debug')
       
    def __getFiles__(self, path):
        files = [ f for f in listdir(path) if isfile(join(path, f)) ]
        return sorted(files) 

    def redrawCatalog(self, path):
        self.theInterface.redrawCatalog(path)
        
    def log(self, message, level):
        self.theInterface.logMessage(message, level)

def main(argv):
    miniatureDir = ''
    workingDir = ''
    encoding = 'utf-8'
    try:
        opts, args = getopt.getopt(argv,'hi:o:e:',['indir=','outdir=' 'encoding='])
    except getopt.GetoptError:
        print 'miniaturegenerator.py -i <inDirectoryir> -o <outDirectory> -e <encoding>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'miniaturegenerator.py -i <inDirectoryir> -o <outDirectory> -e <encoding>'
            sys.exit()
        elif opt in ('-i', '--indir'):
            workingDir = arg
        elif opt in ('-o', '--outdir'):
            miniatureDir = arg
        elif opt in ('-e', '--encoding'):
            encoding = arg
    miniatureDir = join(abspath(miniatureDir), '')
    workingDir = join(abspath(workingDir), '')

    miniatureGenerator = MiniatureGenerator(miniatureDir, encoding)
    
    miniatureGenerator.log('In directory: ' + workingDir.decode(encoding), 'info')
    miniatureGenerator.log('Out directory: ' + miniatureDir.decode(encoding), 'info')
        
    miniatureGenerator.generateMiniature(workingDir)
    miniatureGenerator.redrawCatalog(workingDir)

if __name__ == '__main__':
    main(sys.argv[1:])