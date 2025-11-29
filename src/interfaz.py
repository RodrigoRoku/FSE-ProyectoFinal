import tkinter as tk
import subprocess
import mediaManager
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
    
    logos = {
        "Netflix": "/home/pi2/logos/netflix.png", 
        "Disney+" : "/home/pi2/logos/disney.png",
        "Spotify": "/home/pi2/logos/spotify.png",
        "Youtube": "/home/pi2/logos/youtube.png"
    }
    
    mediaDir = {}

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
        
        self.buttons = []
        
        #Frame para el titulo 
        self.title_frame = tk.Frame(self.root, bg="gray20")
        self.title_frame.pack(fill="x", pady=0)

        self.title_label = tk.Label(self.title_frame, text="FSE-2026-1-Centro Multimeda", font=("Arial", 36, "bold"),
                            fg="white", bg="gray20")
        self.title_label.grid(row=0, column=0, pady=40, padx=50)
        
        self.label = tk.Label(self.title_frame, text="Usa las flechas ↑ ↓ y Enter para seleccionar \n O \n Bien usa tu mouse para navegar", 
                        font=("Arial", 16), fg="white", bg="gray20")
        self.label.grid(row=0, column=1,padx=50,  pady=20)
        
        exit_btn = tk.Button(self.title_frame, text="Salir", font=("Arial", 30), width=15, height=2,
                            bg="gray20", fg="white", activebackground="blue",
                            command=lambda c=self.salir_app: c())
        exit_btn.grid(row=0, column=2, padx=50,pady=5)
        
        #Frame para espaciar elementos
        self.spacer1 = tk.Frame(self.root, height=150, bg="black")
        self.spacer1.pack()
        
        self.streaming_label = tk.Label(self.spacer1, text="Streaming", 
                        font=("Arial", 16), fg="white", bg="black")
        self.streaming_label.pack(pady=20)
        
        #Frame para botones de apps de streamin
        
        self.streamingApp_frame = tk.Frame(self.root, bg="black")
        self.streamingApp_frame.pack(pady=10)
        
        # ===== Lista de botones del menú =====
        self.appButtonDictionary = [
            ("Netflix", lambda: self.abrir_app("netflix")),
            ("Disney+", lambda: self.abrir_app("disney")),
            ("Spotify", lambda: self.abrir_app("spotify")),
            ("Youtube", lambda: self.abrir_app("youtube")),
        ]
        
        # self.extraButtons = {
        #     ("fotos", lambda: self.abrir_vlc("fotos")),
        #     ("videos", lambda: self.abrir_vlc("videos")),
        # }
        
        self.images = []
        # ===== Crear botones y vincular clic derecho =====
        i=0
        for text, command in self.appButtonDictionary:
            img = tk.PhotoImage(file=self.logos[text])
            
            self.images.append(img)
            btn = tk.Button(self.streamingApp_frame, image=img, bg="black", bd=0, relief="flat", highlightthickness=0,
                            command=lambda c=command: c())
            btn.grid(row=0,column=i, pady=5, padx = 40)
            self.buttons.append(btn)
            i+=1
        
        #Frame para espaciar elementos
        self.spacer2 = tk.Frame(self.root, height=150, bg="black")
        self.spacer2.pack()
        
        self.streaming_label = tk.Label(self.spacer2, text="Medios Externos", 
                        font=("Arial", 16), fg="white", bg="black")
        self.streaming_label.pack(pady=20)
        
        #Frame para los archivos multimedia de medios extraibles
        
        self.media_frame = tk.Frame(self.root, bg="black")
        self.media_frame.pack(pady=10)
        i=0
        # for text, command in self.extraButtons:
        #     btn = tk.Button(self.media_frame, text=text, font=("Arial", 24), width=25, height=2,
        #                     bg="gray20", fg="white", activebackground="blue",
        #                     command=lambda c=command: c())
        #     btn.grid(row=1, column=i, pady=5)
        #     self.buttons.append(btn)
        #     i += 1

        # ===== Manejo de navegación con teclado =====
        self.current_index = 0
        self.buttons[self.current_index].focus_set()
        
        self.root.bind("<Up>", self.mover_foco)
        self.root.bind("<Down>", self.mover_foco)
        self.root.bind("<Return>", self.mover_foco)
        
        

        
        
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
    

    def abrir_vlc(self, mediaType):
        try:
            # m = mediaManager.mediaManager(self.mediaDir[mediaType], mediaType )
            # mediaThread = threading.Thread(target=m.playMedia)
            # mediaThread.start()
            
            # del m
            print(f"Abriendo las {mediaType}")
            print(self.mediaDir)
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
        i = 0
        for k in self.mediaDir.keys():
            btn = tk.Button(self.media_frame, text=k, font=("Arial", 24), width=15, height=2,
                                bg="gray20", fg="white", activebackground="blue",
                                command=lambda c=self.abrir_vlc: c(k))
            print(k)
            btn.grid(row=0, column=i, pady=10, padx=30)
            self.buttons.append(btn)
            i += 1
    
    def deleteMediaButtons(self):
        index = -1
        
        for i in self.mediaDir:
            self.buttons[index].destroy()
            index -= 1
    
            

