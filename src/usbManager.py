# usbManager.py
#
# Author:  Rodrigo
# Date:    2025.11.20
# License: MIT
#
# Montaje automàtico de dispositivos de bloques y extracciòn de rutas de
# archivos multimedia del dispositivo

import os
import pyudev
import subprocess as sp

class usbManager:
  imageFormats = ['gif', 'jpeg', 'png', 'jpg']
  videoFormats = ['mp4', 'avi', 'wmv']
  audioFormats = ['wav', 'flac', 'mp3']
  
  def __init__(self):
    self.context = pyudev.Context()
    self.monitor = pyudev.Monitor.from_netlink(self.context)
    self.monitor.filter_by(subsystem="block", device_type="partition")
    self.foundMedia = {"fotos" : [], "videos": [], "audio": []}
    self.mediaLock = False
    self.isMediaMounted = False
  
  def autoMount(self, path):
    args = ["udisksctl", "mount", "-b", path]
    sp.run(args)
 
  def getMountPoint(self, path):
    args = ["findmnt", "-unl", "-S", path]
    cp = sp.run(args, capture_output=True, text=True)
    out = cp.stdout.split(" ")[0]
    return out


  def getMediaFromDir(self, path):
    
    for element in os.listdir(path):
      fullPath = f"{path}/{element}"
      if os.path.isdir(fullPath):
        self.getMediaFromDir(fullPath)
      else:
        fileExtension = element.split(".")[-1]
        if fileExtension in self.imageFormats:
          self.foundMedia['fotos'].append(fullPath)
        elif  fileExtension in self.videoFormats:
          self.foundMedia['videos'].append(fullPath)
        elif fileExtension in self.audioFormats:
          self.foundMedia['audio'].append(fullPath)
      
        
    
  def monitorDevices(self):
    while True:
      action, device = self.monitor.receive_device()
      if action == "add":
        self.autoMount("/dev/" + device.sys_name)
        mp = self.getMountPoint("/dev/" + device.sys_name)
        mediaLock = True
        self.getMediaFromDir(mp)
        mediaLock = False
        print(self.foundMedia)
        self.isMediaMounted = True 
      elif action == "remove":
        mediaLock = True
        for v in self.foundMedia.values():
          v.clear()
        mediaLock = False
        print(self.foundMedia)
        self.isMediaMounted = False 
        
# #Para propositos de testing:
# usb = usbManager()
# usb.monitorDevices()
          


        