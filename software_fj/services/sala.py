"""Servicio de reserva de salas."""

# Importa Real para validar los datos numéricos compartidos.
from numbers import Real
from typing import Optional

# Importa las excepciones propias de reservas y servicios.
from software_fj.exceptions.excepciones import (
    DatoInvalidoError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)

# Importa la clase abstracta base de los servicios.
from software_fj.services.servicio import Servicio


# Clase concreta: representa una sala reservada por horas.
class ReservaSala(Servicio):
    """Sala que se cobra por hora y tiene una capacidad definida."""

    # Máximo permitido para una reserva de sala.
    MAX_HORAS = 12

    # Constructor: valida la capacidad y luego crea el servicio base.
    def __init__(
        self, nombre: str, tarifa_base: Real, capacidad: int, disponible: bool = True
    ) -> None:
        """Crea una sala con capacidad entera positiva."""
        self.capacidad = capacidad
        super().__init__(nombre, tarifa_base, disponible)

    # Capacidad

    # Getter: permite consultar la capacidad de la sala.
    @property
    def capacidad(self) -> int:
        """Devuelve la capacidad de la sala."""
        return self._capacidad

    # Setter: exige un entero positivo para la capacidad.
    @capacidad.setter
    def capacidad(self, valor: int) -> None:
        """Valida y guarda la capacidad."""
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise DatoInvalidoError("La capacidad debe ser un entero positivo.")
        self._capacidad = valor

    # Revalida los datos comunes y la capacidad actual.
    def validar(self) -> bool:
        """Revalida los datos comunes y la capacidad de la sala."""
        super().validar()
        self.capacidad = self._capacidad
        return True

    # Cálculo de costo: valida disponibilidad, duración y límites antes de cobrar.
    def calcular_costo(
        self,
        duracion: float,
        impuesto: float = 0.0,
        descuento: Optional[float] = None,
    ) -> float:
        """Calcula el costo de una sala por horas."""
        if not self.disponible:
            raise ServicioNoDisponibleError("La sala no está disponible.")
        duracion = self._validar_duracion(duracion)
        if duracion > self.MAX_HORAS:
            raise ReservaInvalidaError("Una sala no puede reservarse por más de 12 horas.")
        # Un descuento omitido se interpreta como cero para esta clase.
        if descuento is None:
            descuento = 0.0
        costo = self.tarifa_base * duracion
        return self._aplicar_descuento_e_impuesto(costo, impuesto, descuento)

    # Construye una descripción legible del estado y las características de la sala.
    def describir(self) -> str:
        """Devuelve una descripción de la sala."""
        estado = "disponible" if self.disponible else "no disponible"
        return (
            f"Sala #{self.id}: {self.nombre} | Capacidad: {self.capacidad} | "
            f"Tarifa por hora: {self.tarifa_base} | {estado}"
        )
