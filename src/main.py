import tkinter as tk
import subprocess

# ===== Funciones de acción =====
def abrir_chromium():
    try:
        subprocess.Popen(["chromium-browser", "--kiosk", "https://www.youtube.com"])
    except Exception as e:
        print("Error al abrir Chromium:", e)

def abrir_vlc():
    try:
        subprocess.Popen(["vlc", "--fullscreen", "/home/pi/Videos/prueba.mp4"])
    except Exception as e:
        print("Error al abrir VLC:", e)

def salir_app():
    root.destroy()

# ===== Configuración de la ventana =====
root = tk.Tk()
root.title("Centro Multimedia")  # Este título no se ve en fullscreen
root.attributes("-fullscreen", True)  # Pantalla completa
root.configure(bg="black")

# ===== Título visible en pantalla =====
title_label = tk.Label(root, text="CENTRO MULTIMEDIA", font=("Arial", 36, "bold"),
                       fg="white", bg="black")
title_label.pack(pady=40)

# ===== Lista de botones del menú =====
menu_items = [
    ("Video Streaming", abrir_chromium),
    ("Música Streaming", abrir_chromium),
    ("Medios Extraíbles", abrir_vlc),
    ("Salir", salir_app)
]

buttons = []

# ===== Crear botones =====
for i, (text, command) in enumerate(menu_items):
    btn = tk.Button(root, text=text, font=("Arial", 24), width=25, height=2,
                    bg="gray20", fg="white", activebackground="blue",
                    command=command)
    btn.pack(pady=10)
    buttons.append(btn)

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
label = tk.Label(root, text="Usa las flechas ↑ ↓ y Enter para seleccionar", 
                 font=("Arial", 16), fg="white", bg="black")
label.pack(side="bottom", pady=20)

# ===== Ejecutar la aplicación =====
root.mainloop()

