"""
Configuración centralizada del registro de eventos de Software FJ.

Proporciona un único logger reutilizable, con salida al archivo de log
y a la consola, evitando la creación repetida de handlers.
"""

# Importa logging para crear el logger y sus manejadores.
import logging

# Importa Path para construir rutas independientes del sistema operativo.
from pathlib import Path

# Obtiene el directorio raíz del proyecto a partir de la ubicación de este archivo.
_RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
# Construye la ruta del archivo de registro dentro del proyecto.
_RUTA_LOG = _RAIZ_PROYECTO / "logs" / "software_fj.log"


def obtener_logger() -> logging.Logger:
    """Devuelve el logger compartido de Software FJ."""
    # Crea o recupera el logger con el nombre fijo del proyecto.
    logger = logging.getLogger("software_fj")
    # Evita que los mensajes se propaguen a otros logger configurados.
    logger.propagate = False
    # Define el nivel mínimo que se registrará.
    logger.setLevel(logging.DEBUG)

    # Si el logger ya tiene un manejador propio, reutiliza la configuración.
    if getattr(logger, "_software_fj_configurado", False):
        return logger

    # Crea la carpeta de logs si todavía no existe.
    _RUTA_LOG.parent.mkdir(parents=True, exist_ok=True)
    # Define el formato solicitado: fecha, nivel y mensaje.
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Crea el manejador de archivo con codificación UTF-8.
    manejador_archivo = logging.FileHandler(_RUTA_LOG, encoding="utf-8")
    # Aplica el formato al manejador de archivo.
    manejador_archivo.setFormatter(formato)
    # Agrega el archivo como destino del logger.
    logger.addHandler(manejador_archivo)

    # Crea el manejador que escribe los eventos en consola.
    manejador_consola = logging.StreamHandler()
    # Aplica el mismo formato a la salida de consola.
    manejador_consola.setFormatter(formato)
    # Agrega la consola como destino del logger.
    logger.addHandler(manejador_consola)

    # Marca el logger para evitar que futuras llamadas dupliquen handlers.
    logger._software_fj_configurado = True
    # Devuelve el logger configurado.
    return logger
