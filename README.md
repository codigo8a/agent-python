# Telegram Bot "Que Pasa" (Async Modular Version)

Este es un bot de Telegram modular y asíncrono que responde "que pasa?" a cualquier mensaje recibido.

## Arquitectura

El proyecto sigue reglas de separación de responsabilidades:

- **`run.py`**: Punto de entrada principal.
- **`app/main.py`**: Inicialización de la aplicación.
- **`app/config.py`**: Carga de variables de entorno y configuración de logs.
- **`app/bot/telegram_bot.py`**: Manejo de la comunicación con la API de Telegram.
- **`app/core/router.py`**: Lógica de enrutamiento de mensajes.
- **`app/services/responder.py`**: Lógica de negocio (generación de respuestas).

## Requisitos

- Python 3.10 o superior.
- Una cuenta de Telegram y un Token de Bot (obtenido de [@BotFather](https://t.me/BotFather)).

## Instalación y Ejecución

1.  **Clona o descarga este repositorio.**
2.  **Configura las variables de entorno:**
    Crea un archivo `.env` en la raíz (si no existe ya) y añade tu token:
    ```env
    TELEGRAM_BOT_TOKEN=tu_token_aqui
    ```
3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Ejecuta el bot:**
    ```bash
    python run.py
    ```

## Comandos de Gestión de Archivos

Ahora el bot permite interactuar con el sistema de archivos del proyecto:

- `/list [ruta]`: Lista los archivos y carpetas en la ruta especificada (por defecto la raíz).
- `/read [archivo]`: Muestra el contenido de un archivo de texto.
- `/create [archivo] [contenido]`: Crea un nuevo archivo con el contenido proporcionado.
- `/edit [archivo] [texto_viejo] [texto_nuevo]`: Reemplaza una cadena de texto por otra dentro de un archivo.

## Despliegue en Servidor

Para que el bot corra permanentemente, puedes usar un gestor de procesos como **Docker** o **systemd**.

### Ejemplo con systemd

Crea `/etc/systemd/system/telegram-bot.service`:

```ini
[Unit]
Description=Modular Telegram Bot
After=network.target

[Service]
User=tu_usuario
WorkingDirectory=/ruta/al/proyecto
ExecStart=/ruta/al/proyecto/venv/bin/python run.py
Restart=always

[Install]
WantedBy=multi-user.target
```
