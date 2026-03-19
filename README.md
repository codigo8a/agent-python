# Telegram Bot "Que Pasa" (Async Modular Version)

Este es un bot de Telegram modular y asíncrono que responde "que pasa?" a cualquier mensaje recibido.

## Arquitectura (Rule Engine)

El proyecto utiliza un motor de reglas para procesar mensajes:

- **`run.py`**: Punto de entrada.
- **`app/core/classifier.py`**: **Intent Classifier** que identifica la intención del usuario usando reglas (Regex/Keywords).
- **`app/core/router.py`**: **Command Router** que delega el mensaje al manejador correspondiente.
- **`app/handlers/`**: Manejadores especializados (`FileHandler`, `SystemHandler`) que ejecutan las acciones.
- **`app/services/file_manager.py`**: Servicio base para operaciones de archivos.

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
