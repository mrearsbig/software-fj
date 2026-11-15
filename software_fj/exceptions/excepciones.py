"""
Módulo de excepciones personalizadas del sistema Software FJ.

Define una jerarquía de errores propios del negocio para identificar
con precisión qué falló (datos, parámetros, servicios o reservas) y
permitir que el programa los capture, los registre en el log y siga
funcionando sin interrumpirse.
"""

# Excepción base: hereda de Exception, la clase de errores de Python.
# Todas las demás excepciones del sistema heredan de esta, por lo que
# capturar SoftwareFJError atrapa cualquier error propio del sistema.
class SoftwareFJError(Exception):
    """Error base de todas las excepciones del sistema Software FJ."""

    # Constructor: recibe el mensaje que describe el error.
    def __init__(self, mensaje="Ocurrio un error en el sistema Software FJ."):
        # Guarda el mensaje como atributo para poder consultarlo después.
        self.mensaje = mensaje
        # Llama al constructor de Exception para que Python muestre el mensaje.
        super().__init__(self.mensaje)

# Hereda de SoftwareFJError: es un tipo específico de error del sistema.
class DatoInvalidoError(SoftwareFJError):
    """Se lanza cuando un dato tiene un formato o valor incorrecto.

    Ejemplos: un documento con letras o un correo sin '@'.
    """

    # pass indica que no se agrega lógica nueva; basta con el nombre y la herencia.
    pass

# Hereda de SoftwareFJError: error por ausencia de un dato obligatorio.
class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un dato obligatorio o llega vacío.

    Ejemplos: un nombre vacío o un documento que no se envió.
    """

    pass

# Hereda de SoftwareFJError: error relacionado con los servicios.
class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando un servicio no existe o no se puede usar.

    Ejemplo: intentar reservar una sala que ya está ocupada.
    """

    pass

# Hereda de SoftwareFJError: error relacionado con las reservas.
class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva no se puede crear, confirmar o cancelar.

    Ejemplos: una duración negativa o cancelar una reserva ya cancelada.
    """

    pass

