import tkinter as tk
import subprocess

# ===== Funciones de acción =====
import subprocess

def cerrar_chromium():
    try:
        # Encuentra la ventana de Chromium
        window_id = subprocess.check_output(
            ["xdotool", "search", "--onlyvisible", "--class", "chromium"]
        ).splitlines()
        
        # Envía Ctrl+Shift+W a cada ventana encontrada
        for win in window_id:
            subprocess.run(["xdotool", "windowactivate", win, "key", "ctrl+shift+w"])
    except Exception as e:
        print("Error cerrando Chromium:", e)


def abrir_netflix():
    try:
        # Abrir Chromium en pantalla completa con barra de título
        subprocess.Popen([
            "chromium",
            "--start-fullscreen",
            "--no-sandbox",
            "--new-window",
            "https://www.netflix.com/mx"
        ])
    except Exception as e:
        print("Error al abrir Chromium:", e)


def abrir_disney():
    try:
        # Abrir Chromium en pantalla completa con barra de título
        subprocess.Popen([
            "chromium",
            "--start-fullscreen",
            "--no-sandbox",
            "--new-window",
            "https://www.disneyplus.com/es-mx"
        ])
    except Exception as e:
        print("Error al abrir Chromium:", e)

def abrir_spoti():
    try:
        # Abrir Chromium en pantalla completa con barra de título
        subprocess.Popen([
            "chromium",
            "--start-fullscreen",
            "--no-sandbox",
            "--new-window",
            "https://open.spotify.com/intl-es"
        ])
    except Exception as e:
        print("Error al abrir Chromium:", e)

def abrir_youtube():
    try:
        # Abrir Chromium en pantalla completa con barra de título
        subprocess.Popen([
            "chromium",
            "--start-fullscreen",
            "--no-sandbox",
            "--new-window",
            "https://music.youtube.com/"
        ])
    except Exception as e:
        print("Error al abrir Chromium:", e)


def abrir_vlc(event=None):
    try:
        subprocess.Popen(["vlc", "--fullscreen", "/home/pi/Videos/prueba.mp4"])
    except Exception as e:
        print("Error al abrir VLC:", e)

def salir_app(event=None):
    root.destroy()

# ===== Configuración de la ventana =====
root = tk.Tk()
root.title("Centro Multimedia")
root.attributes("-fullscreen", True)
root.update_idletasks()
root.configure(bg="black")
root.config(cursor="arrow")
root.focus_force()

# ===== Título visible en pantalla =====
title_label = tk.Label(root, text="CENTRO MULTIMEDIA", font=("Arial", 36, "bold"),
                       fg="white", bg="black")
title_label.pack(pady=40)

# ===== Lista de botones del menú =====
menu_items = [
    ("Netflix", abrir_netflix),
    ("Disney+", abrir_disney),
    ("Spotify", abrir_spoti),
    ("Youtube Music", abrir_youtube),
    ("Medios Extraíbles", abrir_vlc),
    ("Salir", salir_app)
]

buttons = []

# ===== Crear botones y vincular clic derecho =====
for text, command in menu_items:
    btn = tk.Button(root, text=text, font=("Arial", 24), width=25, height=2,
                    bg="gray20", fg="white", activebackground="blue",
                    command=lambda c=command: c())
    btn.pack(pady=10)
    buttons.append(btn)
 
    # Vincular clic derecho y clic izquierdo manualmente
    btn.bind("<Button-3>", lambda e, c=command: c())
    btn.bind("<Button-1>", lambda e, c=command: c())

# ===== Manejo de navegación con teclado =====
current_index = 0
buttons[current_index].focus_set()

def mover_foco(event):
    global current_index
    if event.keysym == "Down":
        current_index = (current_index + 1) % len(buttons)
    elif event.keysym == "Up":
        current_index = (current_index - 1) % len(buttons)
    elif event.keysym == "Return":
        buttons[current_index].invoke()
    buttons[current_index].focus_set()

root.bind("<Up>", mover_foco)
root.bind("<Down>", mover_foco)
root.bind("<Return>", mover_foco)

# ===== Mensaje de instrucciones =====
label = tk.Label(root, text="Usa las flechas ↑ ↓ y Enter para seleccionar \n O \n Bien usa tu mouse para navegar", 
                 font=("Arial", 16), fg="white", bg="black")
label.pack(side="bottom", pady=20)

# ===== Ejecutar la aplicación =====
root.mainloop()
