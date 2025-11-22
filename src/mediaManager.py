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


class mediaManager:
  
  def __init__(self, mediaFileList, mediaType):
    self.vlcInstance = vlc.Instance()
    self.mediaList = self.vlcInstance.media_list_new()
    for file in mediaFileList:
      print(file)
      self.mediaList.add_media(self.vlcInstance.media_new(file))
    self.mediaListPlayer =  self.vlcInstance.media_list_player_new()
    self.mediaListPlayer.set_media_list(self.mediaList)
    self.mediaPlayer = self.mediaListPlayer.get_media_player()
    self.keepPlaying = True #Para controlar el ciclo de reproduccion
    
    self.mediaPlayer.audio_set_volume(50)
    self.mediaType = mediaType
       
  def playMedia(self):
    
    self.mediaListPlayer.play()
    sleep(1)
    if self.mediaType == "videos" or self.mediaType == "audio":
      while self.keepPlaying:
        self.mediaListPlayer.play()
        sleep(1)
        if self.mediaListPlayer.is_playing() == 0:
          self.mediaListPlayer.next()
    else:
      while self.keepPlaying:
        sleep(3)
        self.mediaListPlayer.next()

  def stop():
    self.keepPlaying = False
    self.mediaListPlayer.stop()
  
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
