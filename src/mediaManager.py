# usbManager.py
#
# Author:  Rodrigo
# Date:    2025.11.20
# License: MIT
#
# Clase para con metodos para la reproducciòn de listas de archivos 
# de multimedia

import vlc
from time import sleep

import argparse



class mediaManager:
  
  def __init__(self, mediaFileList, mediaType):
    args = ["--fullscreen"]
    if mediaType == "fotos":
      args.append("--vout=x11")
      
    self.vlcInstance = vlc.Instance(args)
    self.mediaFileList = mediaFileList
    self.mediaList = self.vlcInstance.media_list_new()
    for file in mediaFileList:
      print(file)
      self.mediaList.add_media(self.vlcInstance.media_new(file))
    self.mediaListPlayer =  self.vlcInstance.media_list_player_new()
    self.mediaListPlayer.set_media_list(self.mediaList)
    self.mediaPlayer = self.mediaListPlayer.get_media_player()
    self.keepPlaying = True #Para controlar el ciclo de reproduccion
    
    self.mediaPlayer.audio_set_volume(50)
    self.mediaPlayer.video_set_key_input(True)
    self.mediaPlayer.video_set_scale(0)
    self.mediaType = mediaType
       
  def playMedia(self):
    counter = 0
    max = len(self.mediaFileList)
    self.mediaListPlayer.play()
    sleep(0.01)
    self.mediaPlayer.set_fullscreen(True)
    sleep(1)
    if self.mediaType == "videos" or self.mediaType == "audio":
      while self.keepPlaying:
        self.mediaListPlayer.play()
        sleep(1)
    else:
      while self.keepPlaying and counter < max:
        self.mediaPlayer.set_fullscreen(True)
        sleep(5)
        self.mediaListPlayer.next()
        counter += 1

    self.stop()

  def stop(self):
    self.keepPlaying = False
    self.mediaListPlayer.stop()
    self.mediaPlayer.stop()
    self.mediaPlayer.release()
    self.mediaListPlayer.release()
    self.vlcInstance.release()
    
  def pauseMedia():
    pass
  
  def playNext():
    pass
  
  def playPrevious():
    pass
  
  def volumenUp():
    pass
  
  def volumeDown():
    pass
  
# files = [
#   "/home/rodrigo/Pictures/pictures/pic01.jpg",
#   "/home/rodrigo/Pictures/pictures/pic02.jpg",
#   "/home/rodrigo/Pictures/pictures/pic03.jpg",
#   # "/home/rodrigo/Pictures/v3.mp4"
# ]
# mediaHandler = mediaManager(files, "foto")
# mediaHandler.playMedia()

parser = argparse.ArgumentParser()
parser.add_argument(
    "files",
    nargs="+",            # zero or more values
    help="Archivos a reproducir"
)

args = parser.parse_args()
print(args.files)
p = mediaManager(args.files[1:], args.files[0])

p.playMedia()