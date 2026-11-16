"""
Módulo de la clase Cliente del sistema Software FJ.

Representa a un cliente de la empresa con sus datos personales
encapsulados (documento, nombre, correo y teléfono). Cada dato se
valida al asignarse; si no cumple las reglas, se lanza una excepción
personalizada y el cliente no se crea.
"""

# Importa el módulo re (expresiones regulares) para validar el formato del correo.
import re

# Importa las excepciones personalizadas que lanza esta clase.
from software_fj.exceptions.excepciones import DatoInvalidoError, ParametroFaltanteError

# Importa la clase abstracta de la que hereda Cliente.
from software_fj.models.entidad import Entidad


# Hereda de Entidad: Cliente recibe el id, la fecha de creación y la obligación
# de implementar describir() y validar().
class Cliente(Entidad):
    """Cliente de Software FJ con validaciones robustas y datos encapsulados."""

    # Reglas de validación como constantes de clase: se ajustan en un solo lugar.
    LONGITUD_MIN_DOCUMENTO = 6     # Mínimo de dígitos del documento.
    LONGITUD_MAX_DOCUMENTO = 10    # Máximo de dígitos del documento.
    LONGITUD_MIN_NOMBRE = 3        # Mínimo de caracteres del nombre.
    LONGITUD_TELEFONO = 10         # Dígitos exactos de un celular colombiano.
    # Patrón del correo: texto, una @, dominio y al menos un punto (ej. usuario@dominio.com).
    PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")

    # Constructor: recibe los cuatro datos personales del cliente.
    def __init__(self, documento, nombre, correo, telefono):
        # Cada asignación pasa por su setter, que valida el dato antes de guardarlo.
        self.documento = documento
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        # Se llama al constructor de Entidad al final para que el id solo se
        # asigne si todos los datos fueron válidos (no se gastan ids en clientes fallidos).
        super().__init__()

    # Método auxiliar estático: limpia un texto y revisa que exista y no esté vacío.
    @staticmethod
    def _limpiar_texto(valor, campo):
        """Valida que el valor exista y sea texto; devuelve el texto sin espacios sobrantes."""
        # Si el dato no se envió (None), es un parámetro faltante.
        if valor is None:
            raise ParametroFaltanteError(f"El campo '{campo}' es obligatorio.")
        try:
            # Intenta quitar espacios al inicio y al final; solo los textos tienen strip().
            texto = valor.strip()
        except AttributeError as error:
            # Encadenamiento de excepciones: si el valor no es texto (ej. un número),
            # Python lanza AttributeError; se convierte en DatoInvalidoError conservando
            # el error original como causa con "from error".
            raise DatoInvalidoError(
                f"El campo '{campo}' debe ser texto, se recibió {type(valor).__name__}."
            ) from error
        # Si después de limpiar no queda nada (ej. "   "), se considera vacío.
        if texto == "":
            raise ParametroFaltanteError(f"El campo '{campo}' no puede estar vacío.")
        # Devuelve el texto limpio para que el setter lo siga validando.
        return texto


    #DOCUMENTO


    # Getter: permite leer el documento desde afuera.
    @property
    def documento(self):
        """Devuelve el documento del cliente."""
        return self._documento

    # Setter: se ejecuta cada vez que se asigna un documento, incluso después de creado.
    @documento.setter
    def documento(self, valor):
        # Limpia el dato y verifica que exista.
        texto = self._limpiar_texto(valor, "documento")
        # Regla 1: solo números.
        if not texto.isdigit():
            raise DatoInvalidoError(f"El documento '{texto}' solo debe contener números.")
        # Regla 2: longitud entre el mínimo y el máximo permitidos.
        if not self.LONGITUD_MIN_DOCUMENTO <= len(texto) <= self.LONGITUD_MAX_DOCUMENTO:
            raise DatoInvalidoError(
                f"El documento debe tener entre {self.LONGITUD_MIN_DOCUMENTO} y "
                f"{self.LONGITUD_MAX_DOCUMENTO} dígitos; tiene {len(texto)}."
            )
        # Si pasó todas las reglas, se guarda en el atributo privado.
        self._documento = texto

    #NOMBRE

    @property
    def nombre(self):
        """Devuelve el nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        # Limpia el dato y une espacios repetidos (ej. "Ana    Ruiz" -> "Ana Ruiz").
        texto = " ".join(self._limpiar_texto(valor, "nombre").split())
        # Regla 1: solo letras (incluye tildes y ñ) y espacios.
        if not all(caracter.isalpha() or caracter == " " for caracter in texto):
            raise DatoInvalidoError(f"El nombre '{texto}' solo debe contener letras y espacios.")
        # Regla 2: longitud mínima.
        if len(texto) < self.LONGITUD_MIN_NOMBRE:
            raise DatoInvalidoError(
                f"El nombre debe tener al menos {self.LONGITUD_MIN_NOMBRE} caracteres."
            )
        # Guarda el nombre validado.
        self._nombre = texto


    #CORREO

    @property
    def correo(self):
        """Devuelve el correo del cliente."""
        return self._correo

    @correo.setter
    def correo(self, valor):
        # Limpia el dato y lo pasa a minúsculas para guardarlo de forma uniforme.
        texto = self._limpiar_texto(valor, "correo").lower()
        # Regla: debe coincidir completo con el patrón de correo.
        if not self.PATRON_CORREO.fullmatch(texto):
            raise DatoInvalidoError(f"El correo '{texto}' no tiene un formato válido.")
        # Guarda el correo validado.
        self._correo = texto

    #TELEFONO 
    
    @property
    def telefono(self):
        """Devuelve el teléfono del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        # Limpia el dato y verifica que exista.
        texto = self._limpiar_texto(valor, "telefono")
        # Regla: solo números y exactamente la longitud definida.
        if not texto.isdigit() or len(texto) != self.LONGITUD_TELEFONO:
            raise DatoInvalidoError(
                f"El teléfono '{texto}' debe tener exactamente {self.LONGITUD_TELEFONO} dígitos."
            )
        # Guarda el teléfono validado.
        self._telefono = texto

    #METODOS OBLIGATORIOS DE ENTIDAD

    # Implementación de validar(): vuelve a revisar todos los datos actuales.
    def validar(self):
        """Revalida todos los datos del cliente; lanza una excepción si alguno es inválido."""
        # Reasignar cada valor obliga a pasar otra vez por su setter con todas las reglas.
        self.documento = self._documento
        self.nombre = self._nombre
        self.correo = self._correo
        self.telefono = self._telefono
        # Si ninguna regla lanzó excepción, el cliente es válido.
        return True

    # Implementación de describir(): texto legible del cliente.
    def describir(self):
        """Devuelve una descripción del cliente con el documento parcialmente oculto."""
        # Protege el dato personal: solo muestra los últimos 4 dígitos del documento.
        documento_oculto = "*" * (len(self._documento) - 4) + self._documento[-4:]
        # Arma y devuelve la descripción usando el id heredado de Entidad.
        return (
            f"Cliente #{self.id}: {self._nombre} | Documento: {documento_oculto} | "
            f"Correo: {self._correo} | Teléfono: {self._telefono}"
        )