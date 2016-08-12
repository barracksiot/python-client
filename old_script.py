#!/usr/bin/env python

import requests
import time
import subprocess
import hashlib
import sys
import os
import threading
import pygtk
pygtk.require('2.0')
import gtk
import gobject
gobject.threads_init()
#from pymsgbox import *


# Barracks account properties ............................................
apiKey = '53741b8ac429164b0def684fe94106f419b7fba6c56f387998f3c1afdc3c4f72'

versionId = 'pi_0'
unitId = 'RaspberryPi'
# ........................................................................




class Updater(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print 'created thread'

    def setWindow(self, window):
        self.window = window
        return

    def download_file(self, url, h):

        local_filename = "update.tar"
        r = requests.get(url, stream=True, headers=h)
        with open(local_filename, 'wb') as f:
            print 'Start downloading'
            sys.stdout.flush()
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

        return local_filename

    def run(self):
        # Barracks update request
        checkUrl = 'http://192.168.1.48/device/update/check'
        headers = {'Authorization': apiKey,'Content-Type': 'application/json'}
        checkUpdateData = {'unitId': unitId, 'versionId': versionId}

        rep = requests.post(checkUrl, json=checkUpdateData, headers=headers)

        while rep.status_code != 200 :
            time.sleep(1.5)
            rep = requests.post(checkUrl, json=checkUpdateData, headers=headers)

        if rep.status_code == 200 :
            if rep.json is not None :

                md5 = rep.json()['packageInfo']['md5']
                url = rep.json()['packageInfo']['url']
            
                if url is not None :
                    self.window.updateLabel('<span size="18000" color="#FFF">New update available for your device</span>')
                    time.sleep(2)

                    print " > New update available"

                    # Download the file
                    self.window.updateLabel('<span size="18000" color="#FFF">New update available for your device</span>\n<span size="14000" color="#FFF">Downloading package...</span>')
                    time.sleep(2)

                    f = self.download_file(url, headers)
                    fullPath = os.path.realpath(f)

                    # Get md5
                    fileMd5 = hashlib.md5(open(fullPath, 'rb').read()).hexdigest()

                    if md5 == fileMd5 :
                        self.window.updateLabel('<span size="18000" color="#FFF">New update available for your device</span>\n<span size="14000" color="#FFF">Downloading package...</span>\n<span size="14000" color="#FFF">Package downloaded, restarting...</span>')
                        time.sleep(2)

                        scriptName = "/home/pi/install_update.sh %s" % fullPath

                        # Call shell scrip that will unzip the file install the update
                        subprocess.call([scriptName], shell=True)
            
                    else :
                        print " > Error : md5 doesn't match"

            else :
                print " > Error : Response 200 without json"

        else :
            print " > Error : status code $d" % rep.status_code



class BarracksUI:
    def __init__(self, updater):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect('destroy', self.destroy)
        self.window.set_resizable(False)

        self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(4607, 46591, 31487))

        self.window.set_title('Barracks')
        self.window.set_size_request(425, 200)
        self.window.set_position(gtk.WIN_POS_CENTER)

        self.vbox = gtk.VBox(False, 2)
        self.window.add(self.vbox)
        self.vbox.show()

        barracksLabel = gtk.Label('<span size="45000" color="#FFF">Barracks</span>')
        barracksLabel.set_alignment(xalign=0.5, yalign=0.5)
        barracksLabel.set_use_markup(True)
        self.vbox.pack_start(barracksLabel, True, True, 0)
        barracksLabel.show()

        self.label = gtk.Label('<span size="18000" color="#FFF">Checking for updates...</span>')
        self.label.set_alignment(xalign=0.5, yalign=0.5)
        self.label.set_use_markup(True)
        self.vbox.pack_start(self.label, True, True, 0)
        self.label.show()

        self.updater = updater
        self.updater.setWindow(self)

        self.window.show()

    def destroy(self, widget, data=None):
        gtk.main_quit()
        return

    def updateLabel(self, labelValue):
        self.label.set_text(labelValue)
        self.label.set_use_markup(True)
        return




updater = Updater()
BarracksUI(updater)
updater.start()
gtk.main()