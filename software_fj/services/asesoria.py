"""
Servicio de asesorías especializadas de Software FJ.

Una asesoría se cobra por hora y su precio depende del nivel del asesor
(básico, avanzado o experto). Hereda de Servicio, por lo que reutiliza la
validación del nombre, la tarifa y la disponibilidad, y sobrescribe
calcular_costo(), validar() y describir() (polimorfismo).
"""

# Importa Real para aceptar cualquier tipo numérico (int o float).
from numbers import Real

# Importa las excepciones personalizadas que usa este servicio.
from software_fj.exceptions.excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)

# Importa la clase abstracta Servicio de la que hereda Asesoria.
from software_fj.services.servicio import Servicio

# Hereda de Servicio: recibe nombre, tarifa, disponibilidad y el id de Entidad.
class Asesoria(Servicio):
    """Asesoría especializada que se cobra por hora según el nivel del asesor."""

    # Máximo de horas que puede durar una sesión de asesoría.
    MAX_HORAS = 8

    # Niveles permitidos y el factor que multiplica la tarifa por hora.
    FACTORES_NIVEL = {
        "BASICO": 1.0,
        "AVANZADO": 1.5,
        "EXPERTO": 2.0,
    }

    # Constructor: recibe los datos comunes y los propios de la asesoría.
    def __init__(
        self,
        nombre: str,
        tarifa_base: Real,
        especialidad: str,
        nivel: str = "BASICO",
        disponible: bool = True,
    ) -> None:
        """Crea una asesoría después de validar especialidad y nivel."""
        # Valida y guarda la especialidad (pasa por su setter).
        self.especialidad = especialidad
        # Valida y guarda el nivel del asesor (pasa por su setter).
        self.nivel = nivel
        # Llama al constructor de Servicio para validar nombre, tarifa y disponibilidad.
        super().__init__(nombre, tarifa_base, disponible)

    #ESPECIALIDAD

    # Getter: permite leer la especialidad desde afuera.
    @property
    def especialidad(self) -> str:
        """Devuelve la especialidad de la asesoría."""
        return self._especialidad

    # Setter: valida la especialidad cada vez que se asigna.
    @especialidad.setter
    def especialidad(self, valor: str) -> None:
        """Valida y guarda la especialidad."""
        # Si no se envió, es un parámetro faltante.
        if valor is None:
            raise ParametroFaltanteError("La especialidad de la asesoría es obligatoria.")
        # Debe ser texto.
        if not isinstance(valor, str):
            raise DatoInvalidoError("La especialidad de la asesoría debe ser texto.")
        # Quita espacios sobrantes y une espacios repetidos.
        texto = " ".join(valor.strip().split())
        # Si queda vacía, también es un parámetro faltante.
        if not texto:
            raise ParametroFaltanteError("La especialidad de la asesoría no puede estar vacía.")
        # Guarda la especialidad validada.
        self._especialidad = texto

    #NIVEL

    @property
    def nivel(self) -> str:
        """Devuelve el nivel del asesor."""
        return self._nivel

    @nivel.setter
    def nivel(self, valor: str) -> None:
        """Valida y guarda el nivel del asesor."""
        # Si no se envió, es un parámetro faltante.
        if valor is None:
            raise ParametroFaltanteError("El nivel del asesor es obligatorio.")
        # Debe ser texto.
        if not isinstance(valor, str):
            raise DatoInvalidoError("El nivel del asesor debe ser texto.")
        # Se normaliza a mayúsculas y sin espacios (ej. " experto " -> "EXPERTO").
        texto = valor.strip().upper()
        # Solo se aceptan los niveles definidos en FACTORES_NIVEL.
        if texto not in self.FACTORES_NIVEL:
            niveles = ", ".join(self.FACTORES_NIVEL)
            raise DatoInvalidoError(f"Nivel '{valor}' no válido. Use uno de: {niveles}.")
        # Guarda el nivel validado.
        self._nivel = texto

    #METODOS SOBRESCRITOS (POLIMORFISMO)

    # Sobrescribe validar(): revalida lo común y lo propio de la asesoría.
    def validar(self) -> bool:
        """Revalida los datos comunes, la especialidad y el nivel."""
        # Revalida nombre, tarifa y disponibilidad con la lógica de Servicio.
        super().validar()
        # Revalida los datos propios reasignándolos a sus setters.
        self.especialidad = self._especialidad
        self.nivel = self._nivel
        # Si nada falló, la asesoría es válida.
        return True

    # Sobrescribe calcular_costo(): cobra por hora según el nivel del asesor.
    # Los parámetros opcionales impuesto y descuento son la "sobrecarga" del método.
    def calcular_costo(
        self, duracion: Real, impuesto: Real = 0.0, descuento: Real = 0.0
    ) -> Real:
        """Calcula el costo de la asesoría: tarifa x horas x factor del nivel."""
        # No se puede cotizar una asesoría que no está disponible.
        if not self.disponible:
            raise ServicioNoDisponibleError(f"La asesoría '{self.nombre}' no está disponible.")
        # Valida que la duración sea numérica y positiva (método heredado de Servicio).
        duracion = self._validar_duracion(duracion)
        # Regla propia: una sesión no puede superar el máximo de horas.
        if duracion > self.MAX_HORAS:
            raise ReservaInvalidaError(
                f"Una asesoría no puede durar más de {self.MAX_HORAS} horas."
            )
        # Costo base: tarifa por hora, por horas, por el factor del nivel.
        costo = self.tarifa_base * duracion * self.FACTORES_NIVEL[self.nivel]
        # Aplica descuento e impuesto con la lógica común de Servicio.
        return self._aplicar_descuento_e_impuesto(costo, impuesto, descuento)

    # Sobrescribe describir(): texto propio de la asesoría.
    def describir(self) -> str:
        """Devuelve una descripción legible de la asesoría."""
        # Traduce la disponibilidad a texto.
        estado = "disponible" if self.disponible else "no disponible"
        # Arma la descripción con los datos de la asesoría.
        return (
            f"Asesoría #{self.id}: {self.nombre} | Especialidad: {self.especialidad} | "
            f"Nivel: {self.nivel} | Tarifa por hora: {self.tarifa_base} | {estado}"
        )

