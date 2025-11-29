import usbManager
import interfaz2
import threading
from time import sleep


def checkMedia():
  global usbHandler
  global ui
  isMediaLoaded = False
  while ui.isAppRunning:
    if usbHandler.isMediaMounted and not isMediaLoaded:
      #Revisa los medios detectados y cargalos en la lista de medios de UI
      if  len(usbHandler.foundMedia.get("fotos")) > 0:
        ui.media_items.append("fotos")
        ui.mediaDir["fotos"] = usbHandler.foundMedia.get("fotos")[:]
      
      if  len(usbHandler.foundMedia.get("videos")) > 0:
        ui.media_items.append("videos")
        ui.mediaDir["videos"] = usbHandler.foundMedia.get("videos")[:]
        
      if  len(usbHandler.foundMedia.get("audio")) > 0:
        ui.media_items.append("audio")
        ui.mediaDir["audio"] = usbHandler.foundMedia.get("audio")[:]
      print(ui.mediaDir)
      print(ui.media_items)
      ui.isUsbMounted = True
      isMediaLoaded = True
    
    elif not usbHandler.isMediaMounted:
      #Limpia la lista de elementos (y borra los botones?)
      ui.isUsbMounted = False
      ui.media_items.clear()
      ui.mediaDir.clear()
      isMediaLoaded = False

  usbHandler.continueLoop = False
      


usbHandler = usbManager.usbManager()
ui = interfaz2.graphicalInterface()

usbThread = threading.Thread(target=usbHandler.monitorDevices, daemon=True)
eventThread = threading.Thread(target=checkMedia)

usbThread.start()
eventThread.start()

ui.run()

