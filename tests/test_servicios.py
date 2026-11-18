"""Pruebas unitarias de los servicios de Software FJ."""

# Importa el ejecutor de pruebas incluido en la biblioteca estándar.
import unittest

# Importa las excepciones que deben aparecer al usar datos inválidos.
from software_fj.exceptions.excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)

# Importa las clases concretas cuyos comportamientos se verifican.
from software_fj.services.equipo import AlquilerEquipo
from software_fj.services.sala import ReservaSala


# Clase de pruebas: agrupa las verificaciones de los servicios.
class PruebasServicios(unittest.TestCase):
    """Verifica validaciones, costos y polimorfismo de los servicios."""

    # Verifica que las clases concretas puedan crear y validar objetos válidos.
    def test_crea_servicios_validos(self):
        sala = ReservaSala("Sala principal", 100000, 20)
        equipo = AlquilerEquipo("Proyector", 50000, 2)
        self.assertTrue(sala.validar())
        self.assertTrue(equipo.validar())

    # Verifica que un nombre vacío se rechace.
    def test_nombre_vacio(self):
        with self.assertRaises(ParametroFaltanteError):
            ReservaSala("   ", 100000, 10)

    # Verifica que una tarifa negativa se rechace.
    def test_tarifa_negativa(self):
        with self.assertRaises(DatoInvalidoError):
            ReservaSala("Sala", -1, 10)

    # Verifica que una capacidad cero se rechace.
    def test_capacidad_cero(self):
        with self.assertRaises(DatoInvalidoError):
            ReservaSala("Sala", 100000, 0)

    # Verifica que las unidades cero se rechacen.
    def test_unidades_cero(self):
        with self.assertRaises(DatoInvalidoError):
            AlquilerEquipo("Proyector", 50000, 0)

    # Verifica que los booleanos no sean aceptados como cantidades numéricas.
    def test_rechaza_bool_como_numero(self):
        with self.assertRaises(DatoInvalidoError):
            ReservaSala("Sala", True, 10)

    # Verifica que una duración faltante lance el error correspondiente.
    def test_duracion_none(self):
        with self.assertRaises(ParametroFaltanteError):
            ReservaSala("Sala", 100000, 10).calcular_costo(None)

    # Verifica el límite máximo de duración de una reserva de sala.
    def test_duracion_mayor_al_maximo(self):
        with self.assertRaises(ReservaInvalidaError):
            ReservaSala("Sala", 100000, 10).calcular_costo(13)

    # Verifica que no se pueda calcular el costo de un servicio no disponible.
    def test_servicio_no_disponible(self):
        with self.assertRaises(ServicioNoDisponibleError):
            ReservaSala("Sala", 100000, 10, disponible=False).calcular_costo(1)

    # Verifica que el descuento debe estar entre cero y uno.
    def test_descuento_fuera_de_rango(self):
        with self.assertRaises(DatoInvalidoError):
            ReservaSala("Sala", 100000, 10).calcular_costo(1, descuento=1.1)

    # Verifica el orden lógico: primero descuento y después impuesto.
    def test_aplica_descuento_antes_del_impuesto(self):
        sala = ReservaSala("Sala", 100, 10)
        self.assertAlmostEqual(
            sala.calcular_costo(2, impuesto=0.19, descuento=0.10),
            214.2,
            places=2,
        )

    # Verifica el descuento automático al omitir el descuento.
    def test_descuento_automatico_de_equipo(self):
        equipo = AlquilerEquipo("Proyector", 100, 2)
        self.assertAlmostEqual(equipo.calcular_costo(7), 1260.0, places=2)

    # Verifica que cero explícito desactive el descuento automático.
    def test_descuento_cero_explicito_desactiva_descuento_automatico(self):
        equipo = AlquilerEquipo("Proyector", 100, 2)
        self.assertAlmostEqual(equipo.calcular_costo(7, descuento=0.0), 1400.0, places=2)

    # Verifica que ambos servicios puedan calcular costos de manera polimórfica.
    def test_polimorfismo(self):
        servicios = [ReservaSala("Sala", 100, 10), AlquilerEquipo("Equipo", 100, 2)]
        costos = [servicio.calcular_costo(2) for servicio in servicios]
        self.assertEqual(costos, [200, 400])


if __name__ == "__main__":
    unittest.main()
