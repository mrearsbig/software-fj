"""
Pruebas automáticas de la clase Reserva y del servicio Asesoria.

Para ejecutarlas, desde la carpeta raíz del proyecto (software-fj):

    python -m unittest discover tests -v
"""

# Importa unittest, el módulo de pruebas que viene incluido en Python.
import unittest

# Importa las excepciones que se espera que lancen las clases.
from software_fj.exceptions.excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)

# Importa las clases que se van a probar o que se necesitan para crear reservas.
from software_fj.models.cliente import Cliente
from software_fj.models.reserva import Reserva
from software_fj.services.asesoria import Asesoria
from software_fj.services.equipo import AlquilerEquipo
from software_fj.services.sala import ReservaSala

# Datos de prueba centralizados: si se cambian aquí, las pruebas se adaptan solas.
DATOS_CLIENTE = {
    "documento": "1234567890",
    "nombre": "Ana Ruiz",
    "correo": "ana@gmail.com",
    "telefono": "3001234567",
}
TARIFA_ASESORIA = 80000   # Tarifa por hora de la asesoría de prueba.
TARIFA_SALA = 100000      # Tarifa por hora de la sala de prueba.
IMPUESTO = 0.19           # IVA usado en las pruebas.


# Función auxiliar: crea un cliente válido con los datos de prueba.
def crear_cliente():
    """Devuelve un Cliente válido."""
    return Cliente(**DATOS_CLIENTE)

# Función auxiliar: crea una asesoría válida, permitiendo cambiar algunos datos.
def crear_asesoria(**cambios):
    """Devuelve una Asesoria válida, reemplazando los campos recibidos."""
    # Datos por defecto de una asesoría válida.
    datos = {
        "nombre": "Asesoría en seguridad",
        "tarifa_base": TARIFA_ASESORIA,
        "especialidad": "Ciberseguridad",
        "nivel": "BASICO",
    }
    # Reemplaza solo los campos que la prueba quiere cambiar.
    datos.update(cambios)
    # Crea y devuelve la asesoría.
    return Asesoria(**datos)


# Función auxiliar: crea una sala válida.
def crear_sala(disponible=True):
    """Devuelve una ReservaSala válida."""
    return ReservaSala("Sala A", TARIFA_SALA, 10, disponible=disponible)

# Grupo de pruebas del servicio Asesoria.
class PruebasAsesoria(unittest.TestCase):
    """Casos válidos e inválidos del servicio de asesorías."""

    # Cada nivel multiplica la tarifa por su factor.
    def test_costo_segun_nivel(self):
        # Recorre todos los niveles definidos en la clase.
        for nivel, factor in Asesoria.FACTORES_NIVEL.items():
            # subTest muestra cuál nivel falló, si alguno falla.
            with self.subTest(nivel=nivel):
                asesoria = crear_asesoria(nivel=nivel)
                self.assertAlmostEqual(asesoria.calcular_costo(2), TARIFA_ASESORIA * 2 * factor)

    # El nivel se normaliza a mayúsculas y sin espacios.
    def test_normaliza_nivel(self):
        self.assertEqual(crear_asesoria(nivel="  experto ").nivel, "EXPERTO")

    # Aplica impuesto sobre el costo base (método con parámetros opcionales).
    def test_costo_con_impuesto(self):
        asesoria = crear_asesoria()
        esperado = TARIFA_ASESORIA * 2 * (1 + IMPUESTO)
        self.assertAlmostEqual(asesoria.calcular_costo(2, impuesto=IMPUESTO), esperado)

    # Nivel que no existe.
    def test_nivel_invalido(self):
        with self.assertRaises(DatoInvalidoError):
            crear_asesoria(nivel="MASTER")

    # Especialidad vacía.
    def test_especialidad_vacia(self):
        with self.assertRaises(ParametroFaltanteError):
            crear_asesoria(especialidad="   ")

    # Especialidad que no es texto.
    def test_especialidad_no_texto(self):
        with self.assertRaises(DatoInvalidoError):
            crear_asesoria(especialidad=123)

    # Sesión que supera el máximo de horas.
    def test_supera_maximo_de_horas(self):
        with self.assertRaises(ReservaInvalidaError):
            crear_asesoria().calcular_costo(Asesoria.MAX_HORAS + 1)

    # Asesoría marcada como no disponible.
    def test_asesoria_no_disponible(self):
        with self.assertRaises(ServicioNoDisponibleError):
            crear_asesoria(disponible=False).calcular_costo(1)

# Grupo de pruebas de la clase Reserva.
class PruebasReserva(unittest.TestCase):
    """Ciclo de vida y errores de la clase Reserva."""

    # Una reserva nueva inicia en estado PENDIENTE y sin costo.
    def test_reserva_inicia_pendiente(self):
        reserva = Reserva(crear_cliente(), crear_sala(), 2)
        self.assertEqual(reserva.estado, Reserva.PENDIENTE)
        self.assertIsNone(reserva.costo)

    # Flujo completo: confirmar y procesar.
    def test_flujo_completo(self):
        reserva = Reserva(crear_cliente(), crear_sala(), 2)
        costo = reserva.confirmar(impuesto=IMPUESTO)
        reserva.procesar()
        self.assertAlmostEqual(costo, TARIFA_SALA * 2 * (1 + IMPUESTO))
        self.assertEqual(reserva.estado, Reserva.PROCESADA)
        self.assertEqual(
            reserva.historial, [Reserva.PENDIENTE, Reserva.CONFIRMADA, Reserva.PROCESADA]
        )

    # Polimorfismo: la misma Reserva funciona con una asesoría.
    def test_reserva_con_asesoria(self):
        reserva = Reserva(crear_cliente(), crear_asesoria(nivel="EXPERTO"), 2)
        self.assertAlmostEqual(reserva.confirmar(), TARIFA_ASESORIA * 2 * 2.0)

    # Si no se envía descuento, el equipo aplica su descuento automático por largo plazo.
    def test_confirmar_respeta_descuento_automatico_de_equipo(self):
        equipo = AlquilerEquipo("Proyector", 50000, 2)
        dias = AlquilerEquipo.DIAS_PARA_DESCUENTO
        reserva = Reserva(crear_cliente(), equipo, dias)
        esperado = 50000 * dias * 2 * (1 - AlquilerEquipo.DESCUENTO_LARGO_PLAZO)
        self.assertAlmostEqual(reserva.confirmar(), esperado)

    # Se puede cancelar una reserva pendiente.
    def test_cancelar_pendiente(self):
        reserva = Reserva(crear_cliente(), crear_sala(), 2)
        reserva.cancelar()
        self.assertEqual(reserva.estado, Reserva.CANCELADA)

    # No se puede crear sin cliente.
    def test_sin_cliente(self):
        with self.assertRaises(ParametroFaltanteError):
            Reserva(None, crear_sala(), 2)

    # El cliente debe ser un objeto Cliente.
    def test_cliente_invalido(self):
        with self.assertRaises(DatoInvalidoError):
            Reserva("Ana", crear_sala(), 2)

    # No se puede reservar un servicio no disponible.
    def test_servicio_no_disponible(self):
        with self.assertRaises(ServicioNoDisponibleError):
            Reserva(crear_cliente(), crear_sala(disponible=False), 2)

    # La duración debe ser positiva.
    def test_duracion_invalida(self):
        with self.assertRaises(DatoInvalidoError):
            Reserva(crear_cliente(), crear_sala(), 0)

    # No se puede confirmar dos veces.
    def test_confirmar_dos_veces(self):
        reserva = Reserva(crear_cliente(), crear_sala(), 2)
        reserva.confirmar()
        with self.assertRaises(ReservaInvalidaError):
            reserva.confirmar()

    # No se puede procesar una reserva pendiente; el intento igual se cuenta (finally).
    def test_procesar_sin_confirmar(self):
        reserva = Reserva(crear_cliente(), crear_sala(), 2)
        with self.assertRaises(ReservaInvalidaError):
            reserva.procesar()
        self.assertEqual(reserva.intentos_procesamiento, 1)
        self.assertEqual(reserva.estado, Reserva.PENDIENTE)

    # No se puede cancelar una reserva ya cancelada.
    def test_cancelar_dos_veces(self):
        reserva = Reserva(crear_cliente(), crear_sala(), 2)
        reserva.cancelar()
        with self.assertRaises(ReservaInvalidaError):
            reserva.cancelar()

    # Encadenamiento: el error del servicio queda como causa del error de la reserva.
    def test_confirmar_encadena_error_del_servicio(self):
        # Una asesoría de más horas que el máximo se crea bien, pero falla al confirmar.
        reserva = Reserva(crear_cliente(), crear_asesoria(), Asesoria.MAX_HORAS + 1)
        with self.assertRaises(ReservaInvalidaError) as contexto:
            reserva.confirmar()
        # __cause__ guarda el error original del servicio.
        self.assertIsInstance(contexto.exception.__cause__, ReservaInvalidaError)
        # La reserva conserva su estado porque la confirmación falló.
        self.assertEqual(reserva.estado, Reserva.PENDIENTE)

    # Si el servicio deja de estar disponible, procesar falla con encadenamiento.
    def test_procesar_servicio_ya_no_disponible(self):
        sala = crear_sala()
        reserva = Reserva(crear_cliente(), sala, 2)
        reserva.confirmar()
        sala.disponible = False
        with self.assertRaises(ReservaInvalidaError) as contexto:
            reserva.procesar()
        self.assertIsInstance(contexto.exception.__cause__, ServicioNoDisponibleError)
        self.assertEqual(reserva.estado, Reserva.CONFIRMADA)

# Permite ejecutar este archivo directamente con: python tests/test_reserva_asesoria.py
if __name__ == "__main__":
    unittest.main()