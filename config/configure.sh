#!/bin/bash

#El script debe ejecutarse con root.
if [ $USER != "root" ]; then
  echo "El script debe ejecutarse root"
  exit 1
else
  echo "OK el usuario es root"
fi

# Configuraciones iniciales de la raspberry Pi, zona horaria, Habilitar ssh (opcional), configurar pais para wifi Y activar el autologin
timedatectl set-timezone America/Mexico_City

if [[ "$ENABLE_SSH" == "YES" ]]; then
    sudo raspi-config nonint do_ssh 0    
fi

sudo raspi-config nonint do_wifi_country MX

echo ">>> Enabling console autologin"
sudo raspi-config nonint do_boot_behaviour B2  

sleep 5
# Revisar que haya conexión a internet

if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
  echo "OK - Hay conexión a internet"
else
  echo "No hay conexión, abriendo asistente gráfico para conexión a internet."
  nmtui-connect
  #Vuelve a revisar que haya conexión
  if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
    echo "OK - Hay conexión a internet"
  else
    echo "Error - No fue posible conectarse a internet."
    exit 1
  fi
fi

#ACtualización del sistema operativo

echo "→ Actualizando Sistema"
if ! apt update -y; then
    echo "Error durante update"
    exit 1
fi


if ! apt upgrade -y; then
    echo "Error durante upgrade"
    exit 1
fi

#Instalacion de paquetes necesarios.
apt -y install nodm pulseaudio vlc python3-vlc python3-pyudev python3-tk libwidevinecdm0 chromium-browser xorg

# Instalacion y configuracion del bluetooth
echo "→ Instalando paquetes Bluetooth"
apt -y install pi-bluetooth bluez bluez-tools python3-dbus python3-evdev

echo "→ Reiniciando Bluetooth en modo -C -E"
systemctl stop bluetooth
/usr/lib/bluetooth/bluetoothd -C -n -E &

USER=multimedia

#Creacion de directorios
MULTIMEDIAPP_HOME=/home/${USER}/multimediaapp
mkdir -p $MULTIMEDIAPP_HOME

cp ../src/* $MULTIMEDIAPP_HOME

cd /home/${USER}

#Para iniciar automáticamente el programa del centro multimedia al ejecutar xinit
cat > /home/${USER}/.xinitrc << EOF
#!/bin/bash
sleep 1
python3 ${MULTIMEDIAPP_HOME}/interfaz.py
wait
EOF

chmod +x .xinitrc
chown -R ${USER}:${USER} /home/${USER}

#Para iniciar el la sesión gráfica al momento del arranque
echo "xinit > /dev/null 2>&1" >>  /home/${USER}/.profile

echo "quiet loglevel=0 logo.nologo vt.global_cursor_default=0" >> /boot/firmware/cmdline.txt

reboot
