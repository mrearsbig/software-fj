"""
Pruebas de registro y logging del gestor de Software FJ.

Ejecutar desde la raíz del proyecto:
    python -m unittest discover tests -v
"""

# Importa unittest para definir las pruebas.
import unittest
from pathlib import Path

# Importa las clases y excepciones necesarias.
from software_fj.exceptions.excepciones import DatoInvalidoError
from software_fj.gestor import GestorSistema
from software_fj.models.cliente import Cliente
from software_fj.services.sala import ReservaSala
from software_fj.utils.logger import obtener_logger


class PruebasGestor(unittest.TestCase):
    """Pruebas unitarias del GestorSistema."""

    # Verifica el rechazo de documentos duplicados.
    def test_documento_duplicado(self):
        """Lanza DatoInvalidoError al registrar el mismo documento dos veces."""
        # Crea el gestor vacío.
        gestor = GestorSistema()
        # Crea el primer cliente válido.
        cliente = Cliente("1234567890", "Ana Ruiz", "ana@gmail.com", "3001234567")
        # Lo registra correctamente.
        gestor.registrar_cliente(cliente)
        # Crea otro cliente con el mismo documento.
        duplicado = Cliente("1234567890", "Pedro Gomez", "pedro@gmail.com", "3012345678")
        # Confirma que el segundo registro lance la excepción propia.
        with self.assertRaises(DatoInvalidoError):
            gestor.registrar_cliente(duplicado)

    # Verifica el registro correcto de los datos.
    def test_registro_correcto(self):
        """Registra un cliente y un servicio y devuelve copias de las listas."""
        # Crea el gestor vacío.
        gestor = GestorSistema()
        # Crea y registra un cliente válido.
        cliente = Cliente("1234567890", "Ana Ruiz", "ana@gmail.com", "3001234567")
        gestor.registrar_cliente(cliente)
        # Crea y registra una sala válida.
        sala = ReservaSala("Sala A", 50000, 10)
        gestor.registrar_servicio(sala)
        # Comprueba el contenido de las consultas.
        self.assertEqual(len(gestor.obtener_clientes()), 1)
        self.assertEqual(len(gestor.obtener_servicios()), 1)
        # Comprueba que las consultas devuelvan listas independientes.
        copia = gestor.obtener_clientes()
        copia.clear()
        self.assertEqual(len(gestor.obtener_clientes()), 1)

    # Verifica que el logger escriba en el archivo.
    def test_log_se_escribe(self):
        """Escribe un evento y confirma que quede en logs/software_fj.log."""
        # Obtiene el logger para registrar el evento de prueba.
        logger = obtener_logger()
        # Escribe una línea única y fácil de reconocer.
        mensaje = "Prueba de escritura del log del gestor"
        logger.info(mensaje)
        # Fuerza la escritura de manejadores de archivo pendientes.
        for manejador in logger.handlers:
            if hasattr(manejador, "flush"):
                manejador.flush()
        # Construye la ruta esperada del archivo de log.
        ruta_log = Path(__file__).resolve().parents[1] / "logs" / "software_fj.log"
        # Lee el archivo y verifica que contenga el mensaje.
        self.assertIn(mensaje, ruta_log.read_text(encoding="utf-8"))


# Permite ejecutar directamente este módulo de pruebas.
if __name__ == "__main__":
    unittest.main()
