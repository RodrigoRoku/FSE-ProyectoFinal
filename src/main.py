import mediaManager
import usbManager
import threading


def updateUi(mediaDictionary):
  
  #Desplegar el menu
  d = []
  i = 0
  for k in sorted(mediaDictionary.keys()):
    d.append(k)
    print(f"{i}) Reproducir {k}")
    i += 1
  
  ##Esto iria en otra funcion
  selection = int(input("Selecciona una opcion: "))

  mediaHandler = mediaManager.mediaManager(mediaDictionary.get(d[selection]), d[selection])
  mediaHandler.playMedia()
  

def main():
  usbHandler = usbManager.usbManager()
  
  
  usbDetectorThread = threading.Thread(target=usbHandler.monitorDevices)
  usbDetectorThread.start()
  
  #Revisar periodicamente si se ha encontrado algùn medio
  
  isMediaLoaded = False
  mediaType = {'fotos': False, 'videos':False, 'audio':False}
  
  while True:
    if usbHandler.isMediaMounted and not isMediaLoaded:
      if len(usbHandler.foundMedia.get('fotos')) > 0:
        mediaType['fotos'] = True
        
      if len(usbHandler.foundMedia.get('videos')) > 0:
        mediaType['videos'] = True
        
        
      if len(usbHandler.foundMedia.get('audio')) > 0:
        mediaType['audio'] = True
      
      if mediaType['fotos'] or mediaType['videos'] or mediaType['audio']:
        updateUi(usbHandler.foundMedia)
      
      isMediaLoaded = True
    
    if not usbHandler.isMediaMounted:
      mediaType = {'fotos': False, 'videos':False, 'audio':False}
      isMediaLoaded = False
      
main()
        
      
 
      
 
  
  
  