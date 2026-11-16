"""
Clase abstracta base para los servicios de Software FJ.

Centraliza los datos comunes, las validaciones y el cálculo de costos de
los servicios concretos.
"""

from abc import abstractmethod
from numbers import Real

from software_fj.exceptions.excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
)
from software_fj.models.entidad import Entidad


class Servicio(Entidad):
    """Clase abstracta para un servicio ofrecido por Software FJ."""

    def __init__(self, nombre: str, tarifa_base: Real, disponible: bool = True) -> None:
        """Crea un servicio después de validar sus datos básicos."""
        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self.disponible = disponible
        super().__init__()

    @property
    def nombre(self) -> str:
        """Devuelve el nombre del servicio."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y guarda el nombre del servicio."""
        if valor is None:
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        if not isinstance(valor, str):
            raise DatoInvalidoError("El nombre del servicio debe ser texto.")
        texto = " ".join(valor.strip().split())
        if not texto:
            raise ParametroFaltanteError("El nombre del servicio no puede estar vacío.")
        self._nombre = texto

    @property
    def tarifa_base(self) -> Real:
        """Devuelve la tarifa base del servicio."""
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: Real) -> None:
        """Valida y guarda la tarifa base."""
        if valor is None:
            raise ParametroFaltanteError("La tarifa base es obligatoria.")
        if isinstance(valor, bool) or not isinstance(valor, Real):
            raise DatoInvalidoError("La tarifa base debe ser numérica.")
        if valor <= 0:
            raise DatoInvalidoError("La tarifa base debe ser mayor que cero.")
        self._tarifa_base = valor

    @property
    def disponible(self) -> bool:
        """Indica si el servicio puede ser reservado."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        """Valida y guarda la disponibilidad del servicio."""
        if not isinstance(valor, bool):
            raise DatoInvalidoError("La disponibilidad debe ser booleana.")
        self._disponible = valor

    def validar(self) -> bool:
        """Revalida los datos comunes del servicio."""
        self.nombre = self._nombre
        self.tarifa_base = self._tarifa_base
        self.disponible = self._disponible
        return True

    @staticmethod
    def _validar_duracion(duracion: Real) -> Real:
        """Valida una duración numérica y positiva."""
        if duracion is None:
            raise ParametroFaltanteError("La duración es obligatoria.")
        if isinstance(duracion, bool) or not isinstance(duracion, Real):
            raise DatoInvalidoError("La duración debe ser numérica.")
        if duracion <= 0:
            raise DatoInvalidoError("La duración debe ser mayor que cero.")
        return duracion

    @staticmethod
    def _validar_porcentaje(valor: Real, campo: str) -> Real:
        """Valida un descuento o impuesto entre cero y uno."""
        if isinstance(valor, bool) or not isinstance(valor, Real):
            raise DatoInvalidoError(f"El {campo} debe ser numérico.")
        if not 0 <= valor <= 1:
            raise DatoInvalidoError(f"El {campo} debe estar entre 0 y 1.")
        return valor

    def _aplicar_descuento_e_impuesto(
        self, costo: Real, impuesto: Real, descuento: Real
    ) -> Real:
        """Aplica primero el descuento y después el impuesto."""
        descuento = self._validar_porcentaje(descuento, "descuento")
        impuesto = self._validar_porcentaje(impuesto, "impuesto")
        return costo * (1 - descuento) * (1 + impuesto)

    def calcular_costo_con_iva(self, duracion: Real, iva: Real = 0.19) -> Real:
        """Calcula el costo usando el IVA indicado."""
        return self.calcular_costo(duracion, impuesto=iva)

    @abstractmethod
    def calcular_costo(
        self, duracion: Real, impuesto: Real = 0.0, descuento: Real = 0.0
    ) -> Real:
        """Calcula el costo del servicio para una duración dada."""
        pass

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción legible del servicio."""
        pass
