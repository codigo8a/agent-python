# Telegram Bot "Que Pasa"

Un bot simple de Telegram que responde "que pasa?" a cualquier mensaje recibido.

## Requisitos

- Python 3.10 o superior.
- Una cuenta de Telegram y un Token de Bot (ya configurado en `bot.py`).

## Instalación Local

1.  Clona o descarga este repositorio.
2.  Crea un entorno virtual:
    ```bash
    python -m venv venv
    ```
3.  Activa el entorno virtual:
    - **Windows**: `venv\Scripts\activate`
    - **Linux/macOS**: `source venv/bin/activate`
4.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
5.  Ejecuta el bot:
    ```bash
    python bot.py
    ```

## Despliegue en Servidor Linux (Ubuntu/Debian)

Para que el bot corra permanentemente en un servidor, se recomienda usar **systemd**.

### 1. Preparar el servidor

```bash
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y venv si no están presentes
sudo apt install python3 python3-venv -y

# Mover los archivos a una carpeta (ejemplo: /home/usuario/telegram-bot)
mkdir ~/telegram-bot
# (Copia bot.py y requirements.txt a esa carpeta)
cd ~/telegram-bot

# Crear entorno virtual e instalar dependencias
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Crear el servicio de systemd

Crea un archivo de servicio para que el bot se inicie automáticamente:

```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

Pega el siguiente contenido (ajusta `User` y `WorkingDirectory` según tu caso):

```ini
[Unit]
Description=Telegram Bot - Que Pasa
After=network.target

[Service]
User=tu_usuario
WorkingDirectory=/home/tu_usuario/telegram-bot
ExecStart=/home/tu_usuario/telegram-bot/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 3. Activar el servicio

```bash
# Recargar systemd
sudo systemctl daemon-reload

# Habilitar para que inicie con el sistema
sudo systemctl enable telegram-bot

# Iniciar el bot
sudo systemctl start telegram-bot

# Ver estado
sudo systemctl status telegram-bot
```

### 4. Ver logs del bot

Si algo falla, puedes ver los logs con:
```bash
journalctl -u telegram-bot -f
```
