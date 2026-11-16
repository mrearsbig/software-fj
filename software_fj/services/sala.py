"""Servicio de reserva de salas."""

from numbers import Real

from software_fj.exceptions.excepciones import (
    DatoInvalidoError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)
from software_fj.services.servicio import Servicio


class ReservaSala(Servicio):
    """Sala que se cobra por hora y tiene una capacidad definida."""

    MAX_HORAS = 12

    def __init__(
        self, nombre: str, tarifa_base: Real, capacidad: int, disponible: bool = True
    ) -> None:
        """Crea una sala con capacidad entera positiva."""
        self.capacidad = capacidad
        super().__init__(nombre, tarifa_base, disponible)

    @property
    def capacidad(self) -> int:
        """Devuelve la capacidad de la sala."""
        return self._capacidad

    @capacidad.setter
    def capacidad(self, valor: int) -> None:
        """Valida y guarda la capacidad."""
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise DatoInvalidoError("La capacidad debe ser un entero positivo.")
        self._capacidad = valor

    def validar(self) -> bool:
        """Revalida los datos comunes y la capacidad de la sala."""
        super().validar()
        self.capacidad = self._capacidad
        return True

    def calcular_costo(
        self, duracion: Real, impuesto: Real = 0.0, descuento: Real = 0.0
    ) -> Real:
        """Calcula el costo de una sala por horas."""
        if not self.disponible:
            raise ServicioNoDisponibleError("La sala no está disponible.")
        duracion = self._validar_duracion(duracion)
        if duracion > self.MAX_HORAS:
            raise ReservaInvalidaError("Una sala no puede reservarse por más de 12 horas.")
        costo = self.tarifa_base * duracion
        return self._aplicar_descuento_e_impuesto(costo, impuesto, descuento)

    def describir(self) -> str:
        """Devuelve una descripción de la sala."""
        estado = "disponible" if self.disponible else "no disponible"
        return (
            f"Sala #{self.id}: {self.nombre} | Capacidad: {self.capacidad} | "
            f"Tarifa por hora: {self.tarifa_base} | {estado}"
        )
