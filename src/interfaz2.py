import pygame
import subprocess  as sp
import sys
import os
import signal

USER = "pi2"
class graphicalInterface:
  
  appList = {
      "netflix": "https://www.netflix.com/mx", 
      "disney" : "https://www.disneyplus.com/es-mx",
      "spotify": "https://open.spotify.com/intl-es",
      "youtube": "https://music.youtube.com/" 
  }
    
  logos = {
      "netflix": f"/home/{USER}/logos/netflix.png", 
      "disney+": f"/home/{USER}/logos/disney.png",
      "spotify": f"/home/{USER}/logos/spotify.png",
      "youtube": f"/home/{USER}/logos/youtube.png"
  }
  
  logos2 = [
      "/home/rodrigo/Pictures/prueba/logos-proyecto/netflix.png",
      "/home/rodrigo/Pictures/prueba/logos-proyecto/disney.png",
      "/home/rodrigo/Pictures/prueba/logos-proyecto/spotify.png",
      "/home/rodrigo/Pictures/prueba/logos-proyecto/youtube.png"
    ]
  
  mediaDir = {}
  media_items = []

  def __init__(self):
    pygame.init()

    #Pantalla completa
    self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    
    pygame.display.set_caption("Centro Multimedia")
    self.font_big = pygame.font.SysFont(None, 64)
    self.font_med = pygame.font.SysFont(None, 42)
    self.font_small = pygame.font.SysFont(None, 36)
    
    
    #Obtener las dimensiones de la pantalla
    self.screenwidth, self.screenheight = self.screen.get_size()

    # Para manejo de procesos externos
    self.external_process = None

    # Para navegación del menú
    self.section = 0
    self.index = 0

    #Listado de servicios que aparecen en la plataforma
    self.streamingApps = ["netflix", "disney+", "spotify", "youtube"]
    
    #Para control de condicionales internas y externas
    self.isUsbMounted = False
    self.isAppRunning = True
    
    # Colores
    self.bg = (20, 20, 20)
    self.white = (255, 255, 255)
    self.gray = (80, 80, 80)
    self.blue = (0, 120, 200)
    self.red = (200, 60, 60)

  # Para finalización de subprocesos generados  
  def kill_external(self):
    if self.external_process:
      try:
        os.killpg(os.getpgid(self.external_process.pid), signal.SIGTERM)
      except:
          pass
      self.external_process = None

  # Abrir servicios de streaing en el navegador.
  def open_app(self):
    self.kill_external()
    self.external_process = sp.Popen([
            "chromium",
            "--start-fullscreen",
            "--kiosk",
            self.appList.get(self.streamingApps[self.index])
        ], preexec_fn=os.setsid)
   
  # Reproducir multimedia haciendo uso de script que usa pythonvlc VLC 
  def play_video(self):
    self.kill_external()
    playlist = []
    mediaType = self.media_items[self.index]
    playlist.append(mediaType)
    playlist = playlist + self.mediaDir.get(mediaType)
    self.external_process = sp.Popen([
          "python3",
          f"/home/{USER}/mediaManager.py",
      ] + playlist, preexec_fn=os.setsid)
  
  #Salir del programa pricniapl
  def exit_app(self):
    self.kill_external()
    self.isAppRunning = False
    pygame.quit()
    sp.Popen(["sudo", "shutdown", "-h", "now"])
    sys.exit()

  # Para renderizar el encabezado
  def drawHeader(self):
      
    mainHeader = self.screenheight * 0.18

    pygame.draw.rect(self.screen, self.gray, (0, 0, self.screenwidth, mainHeader))
    title = self.font_big.render("Centro multimedia FSE 2026-1", True, self.white)
    self.screen.blit(title, (self.screenwidth//2 - title.get_width()//2,
                              mainHeader//2 - title.get_height()//2))

    # Boton para salir (debe de apagar el equipo)
    exitWidth, exitHeight = 140, 60
    xPos = self.screenwidth - exitWidth - 40
    yPos = mainHeader // 2 - exitHeight // 2

    color = self.blue if (self.section == 0) else self.red
    pygame.draw.rect(self.screen, color, (xPos, yPos, exitWidth, exitHeight), border_radius=10)

    ex = self.font_med.render("Exit", True, self.white)
    self.screen.blit(ex, (xPos + exitWidth//2 - ex.get_width()//2,
                          yPos + exitHeight//2 - ex.get_height()//2))

  def drawStreaming(self):
    
    area_y = self.screenheight * 0.18
    area_h = self.screenheight * 0.42

    pygame.draw.rect(self.screen, (40, 40, 40), (0, area_y, self.screenwidth, area_h))

    # STREAMING title
    txt = self.font_small.render("Streaming", True, self.white)
    self.screen.blit(txt, (self.screenwidth//2 - txt.get_width()//2, area_y + 10))

    # Layout buttons
    total = len(self.streamingApps)
    section_w = self.screenwidth / total
    item_size = int(area_h * 0.45)
    
    for i, name in enumerate(self.streamingApps):
      cx = section_w * i + section_w/2
      cy = area_y + area_h/2  # push down under header text

      rect = pygame.Rect(
          cx - item_size/2,
          cy - item_size/2,
          230,
          230
      )

      # highlight if selected
      if self.section == 1 and self.index == i:
          pygame.draw.rect(self.screen, self.blue, rect, border_radius=0)
      else:
          pygame.draw.rect(self.screen, self.gray, rect, border_radius=0)

      img = pygame.image.load(self.logos[name]).convert()  # already loaded/sized image
      img_rect = img.get_rect(center=rect.center)

      self.screen.blit(img, img_rect)


  def draw_media_section(self):
    area_y = self.screenheight * 0.60
    area_h = self.screenheight * 0.40
    pygame.draw.rect(self.screen, (30, 30, 30), (0, area_y, self.screenwidth, area_h))

    if not self.isUsbMounted:
      txt = self.font_small.render("Media: conecte una USB con archivos multimedia", True, self.white)
      self.screen.blit(txt, (self.screenwidth//2 - txt.get_width()//2, area_y + 10))
    else:
      txt = self.font_small.render("Media presione un boton para reproducir el tipo de archivo", True, self.white)
      self.screen.blit(txt, (self.screenwidth//2 - txt.get_width()//2, area_y + 10))

    total = len(self.media_items)
    if total > 0 and self.isUsbMounted:
      
      section_w = self.screenwidth / total
      button_w = 180
      button_h = 60

      for i, label in enumerate(self.media_items):
        cx = section_w * i + section_w/2
        cy = area_y + area_h/2 + 20  

        rect = pygame.Rect(cx - button_w/2, cy - button_h/2,
                            button_w, button_h)
        #Remarcar la opcion seleccionada
        color = self.blue if (self.section == 2 and self.index == i) else self.gray
        pygame.draw.rect(self.screen, color, rect, border_radius=10)

        txt_label = self.font_med.render(f"{label}", True, self.white)
        self.screen.blit(txt_label, txt_label.get_rect(center=rect.center))

  def navigation(self, event):
        
    if self.isUsbMounted:
      numSections = 3
    else:
      numSections = 2
      
    if event.key == pygame.K_ESCAPE:
      if self.external_process:
          self.kill_external()
      else:
          self.exit_app()
    elif event.key == pygame.K_UP:
      self.section = (self.section - 1) % numSections
      self.index = 0

    elif event.key == pygame.K_DOWN:
      self.section = (self.section + 1) % numSections
      self.index = 0

    elif event.key == pygame.K_LEFT:
      if self.section == 1:
          self.index = (self.index - 1) % len(self.streamingApps)
      elif self.section == 2 and self.isUsbMounted:
          self.index = (self.index - 1) % len(self.media_items)

    elif event.key == pygame.K_RIGHT:
      if self.section == 1:
          self.index = (self.index + 1) % len(self.streamingApps)
      elif self.section == 2 and self.isUsbMounted:
          self.index = (self.index + 1) % len(self.media_items)

    elif event.key == pygame.K_RETURN:
      self.activate()

  def activate(self):
    if self.section == 0:
        self.exit_app()
    elif self.section == 1:
        self.open_app()
    elif self.section == 2:
        self.play_video()

  #Loop Principal
  def run(self):
    clock = pygame.time.Clock()

    while True:
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            self.navigation(event)

      self.screen.fill(self.bg)
      self.drawHeader()
      self.drawStreaming()
      self.draw_media_section()

      pygame.display.flip()
      clock.tick(30)

  #Edicion dinamica de la Interfaz Grafica
  def addButtons(self):
    pass
  
  def deleteButtons(self):
    pass
    
