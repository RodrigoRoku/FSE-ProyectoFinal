import tkinter as tk
import subprocess
import threading
import  re
def conectar_bluetooth():
    popup = tk.Toplevel(root)
    popup.title("Bluetooth")
    popup.geometry("600x300")
    popup.configure(bg="black")

    lbl_info = tk.Label(
        popup,
        text="Activando Bluetooth...\nBusca el dispositivo 'pi' en tu teléfono o control.",
        fg="white", bg="black", font=("Arial", 18)
    )
    lbl_info.pack(pady=20)

    lbl_estado = tk.Label(
        popup,
        text="Preparando emparejamiento...",
        fg="cyan", bg="black", font=("Arial", 16)
    )
    lbl_estado.pack(pady=10)

    # Ejecuta bluetoothctl
    process = subprocess.Popen(
        ["bluetoothctl"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    # Inicialización
    init_cmds = """agent on
default-agent
power on
discoverable on
pairable on
scan on
"""
    process.stdin.write(init_cmds)
    process.stdin.flush()

    dispositivo_mac = {"mac": None}

    def escuchar_bt():
        for line in process.stdout:
            line = line.strip()
            print("[BT]", line)

            # Detectar dispositivo nuevo
            if "Device" in line and ("NEW" in line or "Connected" in line):
                m = re.search(r"Device ([0-9A-F:]{17})", line)
                if m and dispositivo_mac["mac"] != m.group(1):
                    dispositivo_mac["mac"] = m.group(1)
                    root.after(0, lambda:
                        lbl_estado.config(text=f"Detectado: {m.group(1)}\nIntentando emparejar...")
                    )
                    process.stdin.write(f"pair {m.group(1)}\n")
                    process.stdin.flush()

            # Confirmación automática de passkey
            if "Confirm passkey" in line or "Request confirmation" in line:
                process.stdin.write("yes\n")
                process.stdin.flush()
                root.after(0, lambda:
                    lbl_estado.config(text="✔ Passkey confirmado automáticamente.")
                )

            # Autorizar servicios automáticamente
            if "Authorize service" in line:
                process.stdin.write("yes\n")
                process.stdin.flush()
                root.after(0, lambda:
                    lbl_estado.config(text="✔ Servicio autorizado automáticamente.")
                )

            # Emparejado correctamente
            if "Paired: yes" in line:
                root.after(0, lambda:
                    lbl_estado.config(text="✔ Emparejado correctamente.\nIntentando conectar...")
                )
                if dispositivo_mac["mac"]:
                    process.stdin.write(f"connect {dispositivo_mac['mac']}\n")
                    process.stdin.flush()

            # Conexión exitosa
            if "Connection successful" in line or "Connected: yes" in line:
                root.after(0, lambda:
                    lbl_estado.config(text="✔ Conectado correctamente.\nDispositivo listo como control remoto.")
                )
                return

    threading.Thread(target=escuchar_bt, daemon=True).start()



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
        global screenwidth
        global screenheight
        # Abrir Chromium en pantalla completa con barra de título
        subprocess.Popen([
            "chromium",
            "--start-fullscreen",
            "--kiosk",
            "--window-position=0,0",
            f"--window-size={screenwidth},{screenheight}",
            "https://www.netflix.com/mx"
        ])
    except Exception as e:
        print("Error al abrir Chromium:", e)


def abrir_disney():
    try:
        global screenwidth
        global screenheight
        # Abrir Chromium en pantalla completa con barra de título
        subprocess.Popen([
            "chromium",
            "--start-fullscreen",
            "--kiosk",
            "--window-position=0,0",
            f"--window-size={screenwidth},{screenheight}",
            "https://www.disneyplus.com/es-mx"
        ])
    except Exception as e:
        print("Error al abrir Chromium:", e)

def abrir_spoti():
    try:
        global screenwidth
        global screenheight
        # Abrir Chromium en pantalla completa con barra de título
        subprocess.Popen([
            "chromium",
            "--start-fullscreen",
            "--kiosk",
            "--window-position=0,0",
            f"--window-size={screenwidth},{screenheight}",
            "https://open.spotify.com/intl-es"
        ])
    except Exception as e:
        print("Error al abrir Chromium:", e)

def abrir_youtube():
    try:
        global screenwidth
        global screenheight
        # Abrir Chromium en pantalla completa con barra de título
        subprocess.Popen([
            "chromium",
            "--start-fullscreen",
            "--kiosk",
            "--window-position=0,0",
            f"--window-size={screenwidth},{screenheight}",
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
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
root.geometry(f"{screenwidth}x{screenheight}+0+0")
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
   ("Conecta su dispositivo", conectar_bluetooth),
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
    # btn.bind("<Button-3>", lambda e, c=command: c())
    # btn.bind("<Button-1>", lambda e, c=command: c())

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
