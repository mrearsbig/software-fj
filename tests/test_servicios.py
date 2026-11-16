"""Pruebas unitarias de los servicios de Software FJ."""

import unittest

from software_fj.exceptions.excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)
from software_fj.services.equipo import AlquilerEquipo
from software_fj.services.sala import ReservaSala


class PruebasServicios(unittest.TestCase):
    """Verifica validaciones, costos y polimorfismo de los servicios."""

    def test_crea_servicios_validos(self):
        sala = ReservaSala("Sala principal", 100000, 20)
        equipo = AlquilerEquipo("Proyector", 50000, 2)
        self.assertTrue(sala.validar())
        self.assertTrue(equipo.validar())

    def test_nombre_vacio(self):
        with self.assertRaises(ParametroFaltanteError):
            ReservaSala("   ", 100000, 10)

    def test_tarifa_negativa(self):
        with self.assertRaises(DatoInvalidoError):
            ReservaSala("Sala", -1, 10)

    def test_capacidad_cero(self):
        with self.assertRaises(DatoInvalidoError):
            ReservaSala("Sala", 100000, 0)

    def test_unidades_cero(self):
        with self.assertRaises(DatoInvalidoError):
            AlquilerEquipo("Proyector", 50000, 0)

    def test_rechaza_bool_como_numero(self):
        with self.assertRaises(DatoInvalidoError):
            ReservaSala("Sala", True, 10)

    def test_duracion_none(self):
        with self.assertRaises(ParametroFaltanteError):
            ReservaSala("Sala", 100000, 10).calcular_costo(None)

    def test_duracion_mayor_al_maximo(self):
        with self.assertRaises(ReservaInvalidaError):
            ReservaSala("Sala", 100000, 10).calcular_costo(13)

    def test_servicio_no_disponible(self):
        with self.assertRaises(ServicioNoDisponibleError):
            ReservaSala("Sala", 100000, 10, disponible=False).calcular_costo(1)

    def test_descuento_fuera_de_rango(self):
        with self.assertRaises(DatoInvalidoError):
            ReservaSala("Sala", 100000, 10).calcular_costo(1, descuento=1.1)

    def test_aplica_descuento_antes_del_impuesto(self):
        sala = ReservaSala("Sala", 100, 10)
        self.assertEqual(sala.calcular_costo(2, impuesto=0.19, descuento=0.10), 214.2)

    def test_descuento_automatico_de_equipo(self):
        equipo = AlquilerEquipo("Proyector", 100, 2)
        self.assertEqual(equipo.calcular_costo(7), 1260.0)

    def test_polimorfismo(self):
        servicios = [ReservaSala("Sala", 100, 10), AlquilerEquipo("Equipo", 100, 2)]
        costos = [servicio.calcular_costo(2) for servicio in servicios]
        self.assertEqual(costos, [200, 400])


if __name__ == "__main__":
    unittest.main()
