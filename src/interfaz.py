import tkinter as tk
import subprocess
from time import sleep
import threading


# def cerrar_chromium():
#     try:
#         # Encuentra la ventana de Chromium
#         window_id = subprocess.check_output(
#             ["xdotool", "search", "--onlyvisible", "--class", "chromium"]
#         ).splitlines()
        
#         # Envía Ctrl+Shift+W a cada ventana encontrada
#         for win in window_id:
#             subprocess.run(["xdotool", "windowactivate", win, "key", "ctrl+shift+w"])
#     except Exception as e:
#         print("Error cerrando Chromium:", e)
        
class graphicalInterface:
    
    appList = {
        "netflix": "https://www.netflix.com/mx", 
        "disney" : "https://www.disneyplus.com/es-mx",
        "spotify": "https://open.spotify.com/intl-es",
        "youtube": "https://music.youtube.com/" 
    }
    
    mediaList = []

    def __init__(self):
        # ===== Configuración de la ventana =====
        self.root = tk.Tk()
        self.root.title("Centro Multimedia")
        self.screenwidth = self.root.winfo_screenwidth()
        self.screenheight = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screenwidth}x{self.screenheight}+0+0")
        self.root.attributes("-fullscreen", True)
        self.root.update_idletasks()
        self.root.configure(bg="black")
        self.root.config(cursor="arrow")
        self.root.focus_force()
        # ===== Título visible en pantalla =====
        self.title_label = tk.Label(self.root, text="FSE-2026-1-Centro Multimeda", font=("Arial", 36, "bold"),
                            fg="white", bg="black")
        self.title_label.pack(pady=40)
        # ===== Lista de botones del menú =====
        self.menu_items = [
            ("Netflix", lambda: self.abrir_app("netflix")),
            ("Disney+", lambda: self.abrir_app("disney")),
            ("Spotify", lambda: self.abrir_app("spotify")),
            ("Youtube Music", lambda: self.abrir_app("youtube")),
            ("Medios Extraíbles", self.abrir_vlc),
            ("Salir", self.salir_app)
        ]
        
        self.buttons = []
        # ===== Crear botones y vincular clic derecho =====
        for text, command in self.menu_items:
            btn = tk.Button(self.root, text=text, font=("Arial", 24), width=25, height=2,
                            bg="gray20", fg="white", activebackground="blue",
                            command=lambda c=command: c())
            btn.pack(pady=10)
            self.buttons.append(btn)

        # ===== Manejo de navegación con teclado =====
        self.current_index = 0
        self.buttons[self.current_index].focus_set()
        
        self.root.bind("<Up>", self.mover_foco)
        self.root.bind("<Down>", self.mover_foco)
        self.root.bind("<Return>", self.mover_foco)
        
        # ===== Mensaje de instrucciones =====
        self.label = tk.Label(self.root, text="Usa las flechas ↑ ↓ y Enter para seleccionar \n O \n Bien usa tu mouse para navegar", 
                        font=("Arial", 16), fg="white", bg="black")
        self.label.pack(side="bottom", pady=20)

        
        
    def abrir_app(self,app):
        try:
            # Abrir Chromium en pantalla completa con barra de título
            subprocess.Popen([
                "chromium",
                "--start-fullscreen",
                "--kiosk",
                "--window-position=0,0",
                f"--window-size={self.screenwidth},{self.screenheight}",
                self.appList.get(app)
            ])
        except Exception as e:
            print("Error al abrir Chromium:", e)
    

    def abrir_vlc(self, event=None):
        try:
            subprocess.Popen(["vlc", "--fullscreen", "/home/pi/Videos/prueba.mp4"])
        except Exception as e:
            print("Error al abrir VLC:", e)

    def salir_app(self, event=None):
        self.root.destroy()


    def mover_foco(self, event):
        if event.keysym == "Down":
            self.current_index = (self.current_index + 1) % len(self.buttons)
        elif event.keysym == "Up":
            self.current_index = (self.current_index - 1) % len(self.buttons)
        elif event.keysym == "Return":
            self.buttons[self.current_index].invoke()
        self.buttons[self.current_index].focus_set()

    def inicia_interfaz(self):        
        # ===== Ejecutar la aplicación =====
        self.root.mainloop()
        
    def addMediaButtons(self):
        for item in self.mediaList:
            btn = tk.Button(self.root, text=item, font=("Arial", 24), width=25, height=2,
                                bg="gray20", fg="white", activebackground="blue",
                                command=lambda c=self.abrir_app: c("netflix"))
            btn.pack(pady=10)
            self.buttons.append(btn)



def checkEvent():
    #Objeto para la interfaz gràfica
    global i
    e = True
    sleep(5)
    if e :
        i.mediaList.append("Fotos")
        i.mediaList.append("Videos")
        i.root.after(0, i.addMediaButtons)
        

i = graphicalInterface()
eventThread = threading.Thread(target=checkEvent)

eventThread.start()

i.inicia_interfaz()