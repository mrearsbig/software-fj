"""Servicio de alquiler de equipos."""

from numbers import Real

from software_fj.exceptions.excepciones import (
    DatoInvalidoError,
    ServicioNoDisponibleError,
)
from software_fj.services.servicio import Servicio


class AlquilerEquipo(Servicio):
    """Equipo que se cobra por día y por unidad alquilada."""

    DESCUENTO_AUTOMATICO = 0.10
    DIAS_DESCUENTO_AUTOMATICO = 7

    def __init__(
        self, nombre: str, tarifa_base: Real, unidades: int, disponible: bool = True
    ) -> None:
        """Crea un alquiler con una cantidad entera positiva de unidades."""
        self.unidades = unidades
        super().__init__(nombre, tarifa_base, disponible)

    @property
    def unidades(self) -> int:
        """Devuelve las unidades disponibles."""
        return self._unidades

    @unidades.setter
    def unidades(self, valor: int) -> None:
        """Valida y guarda la cantidad de unidades."""
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise DatoInvalidoError("Las unidades deben ser un entero positivo.")
        self._unidades = valor

    def validar(self) -> bool:
        """Revalida los datos comunes y las unidades del equipo."""
        super().validar()
        self.unidades = self._unidades
        return True

    def calcular_costo(
        self, duracion: Real, impuesto: Real = 0.0, descuento: Real = 0.0
    ) -> Real:
        """Calcula el costo diario por la cantidad de unidades."""
        if not self.disponible:
            raise ServicioNoDisponibleError("El equipo no está disponible.")
        duracion = self._validar_duracion(duracion)
        if descuento == 0.0 and duracion >= self.DIAS_DESCUENTO_AUTOMATICO:
            descuento = self.DESCUENTO_AUTOMATICO
        costo = self.tarifa_base * duracion * self.unidades
        return self._aplicar_descuento_e_impuesto(costo, impuesto, descuento)

    def describir(self) -> str:
        """Devuelve una descripción del alquiler de equipo."""
        estado = "disponible" if self.disponible else "no disponible"
        return (
            f"Equipo #{self.id}: {self.nombre} | Unidades: {self.unidades} | "
            f"Tarifa por día: {self.tarifa_base} | {estado}"
        )
