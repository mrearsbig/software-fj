"""Servicio de alquiler de equipos."""

# Importa Real para validar los datos numéricos compartidos.
from numbers import Real
from typing import Optional

# Importa las excepciones usadas al validar o prestar equipos.
from software_fj.exceptions.excepciones import (
    DatoInvalidoError,
    ServicioNoDisponibleError,
)

# Importa la clase abstracta base de los servicios.
from software_fj.services.servicio import Servicio


# Clase concreta: representa el alquiler de equipos por días y unidades.
class AlquilerEquipo(Servicio):
    """Equipo que se cobra por día y por unidad alquilada."""

    # Porcentaje de descuento aplicado a alquileres largos cuando no se indica uno.
    DESCUENTO_LARGO_PLAZO = 0.10
    # Cantidad mínima de días que activa el descuento largo plazo.
    DIAS_PARA_DESCUENTO = 7

    # Constructor: valida las unidades y luego crea el servicio base.
    def __init__(
        self, nombre: str, tarifa_base: Real, unidades: int, disponible: bool = True
    ) -> None:
        """Crea un alquiler con una cantidad entera positiva de unidades."""
        self.unidades = unidades
        super().__init__(nombre, tarifa_base, disponible)

    # Unidades

    # Getter: permite consultar la cantidad disponible de unidades.
    @property
    def unidades(self) -> int:
        """Devuelve las unidades disponibles."""
        return self._unidades

    # Setter: exige un número entero positivo de unidades.
    @unidades.setter
    def unidades(self, valor: int) -> None:
        """Valida y guarda la cantidad de unidades."""
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise DatoInvalidoError("Las unidades deben ser un entero positivo.")
        self._unidades = valor

    # Revalida los datos comunes y la cantidad actual de unidades.
    def validar(self) -> bool:
        """Revalida los datos comunes y las unidades del equipo."""
        super().validar()
        self.unidades = self._unidades
        return True

    # Cálculo de costo: respeta un descuento explícito y activa el automático solo si se omite.
    def calcular_costo(
        self,
        duracion: float,
        impuesto: float = 0.0,
        descuento: Optional[float] = None,
    ) -> float:
        """Calcula el costo diario por la cantidad de unidades."""
        if not self.disponible:
            raise ServicioNoDisponibleError("El equipo no está disponible.")
        duracion = self._validar_duracion(duracion)
        # Solo se aplica el descuento automático cuando el argumento fue omitido.
        if descuento is None:
            if duracion >= self.DIAS_PARA_DESCUENTO:
                descuento = self.DESCUENTO_LARGO_PLAZO
            else:
                descuento = 0.0
        costo = self.tarifa_base * duracion * self.unidades
        return self._aplicar_descuento_e_impuesto(costo, impuesto, descuento)

    # Construye una descripción legible del estado y las características del equipo.
    def describir(self) -> str:
        """Devuelve una descripción del alquiler de equipo."""
        estado = "disponible" if self.disponible else "no disponible"
        return (
            f"Equipo #{self.id}: {self.nombre} | Unidades: {self.unidades} | "
            f"Tarifa por día: {self.tarifa_base} | {estado}"
        )
