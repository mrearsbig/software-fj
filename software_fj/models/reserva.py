"""
Módulo de la clase Reserva del sistema Software FJ.

Una reserva une a un cliente con un servicio por una duración determinada
y controla su ciclo de vida mediante estados:

    PENDIENTE -> CONFIRMADA -> PROCESADA
    PENDIENTE o CONFIRMADA -> CANCELADA

Cada cambio de estado se valida; si la operación no está permitida, se lanza
una excepción personalizada y la reserva conserva su estado anterior.
"""
# Importa Real para aceptar cualquier tipo numérico (int o float) en la duración.
from numbers import Real

# Importa Optional para indicar que el descuento puede omitirse (None).
from typing import Optional

# Importa las excepciones personalizadas que usa esta clase.
from software_fj.exceptions.excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    SoftwareFJError,
)

# Importa la clase Cliente para verificar que la reserva reciba un cliente válido.
from software_fj.models.cliente import Cliente

# Importa la clase abstracta de la que hereda Reserva.
from software_fj.models.entidad import Entidad

# Importa la clase abstracta Servicio para aceptar cualquier servicio (polimorfismo).
from software_fj.services.servicio import Servicio

# Hereda de Entidad: la reserva recibe id, fecha de creación y debe implementar
# describir() y validar().
class Reserva(Entidad):
    """Reserva que integra cliente, servicio, duración y estado."""

    # Estados posibles de una reserva, definidos como constantes de clase.
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    PROCESADA = "PROCESADA"

    # Constructor: recibe el cliente, el servicio y la duración de la reserva.
    def __init__(self, cliente, servicio, duracion):
        # Valida que el cliente exista y sea un objeto Cliente.
        self._cliente = self._validar_cliente(cliente)
        # Valida que el servicio exista, sea un Servicio y esté disponible.
        self._servicio = self._validar_servicio(servicio)
        # Valida que la duración sea numérica y positiva.
        self._duracion = self._validar_duracion(duracion)
        # Toda reserva nueva inicia en estado PENDIENTE.
        self._estado = self.PENDIENTE
        # El costo se calcula al confirmar; mientras tanto no existe.
        self._costo = None
        # Lista interna con el historial de cambios de estado de la reserva.
        self._historial = [self.PENDIENTE]
        # Cuenta cuántas veces se intentó procesar la reserva (exitosas o no).
        self._intentos_procesamiento = 0
        # Se llama al final para que el id solo se asigne a reservas válidas.
        super().__init__()

#VALIDACIONES INTERNAS:

    # Método estático: no necesita datos de la reserva, solo el valor recibido.
    @staticmethod
    def _validar_cliente(cliente):
        """Verifica que el cliente exista y sea un objeto Cliente."""
        # Si no se envió cliente, es un parámetro faltante.
        if cliente is None:
            raise ParametroFaltanteError("La reserva necesita un cliente.")
        # isinstance verifica que el objeto sea de tipo Cliente.
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("El cliente de la reserva debe ser un objeto Cliente.")
        # Devuelve el cliente validado.
        return cliente

    @staticmethod
    def _validar_servicio(servicio):
        """Verifica que el servicio exista, sea un Servicio y esté disponible."""
        # Si no se envió servicio, es un parámetro faltante.
        if servicio is None:
            raise ParametroFaltanteError("La reserva necesita un servicio.")
        # Acepta cualquier clase hija de Servicio (sala, equipo, asesoría...).
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("El servicio de la reserva debe ser un objeto Servicio.")
        # No se puede reservar un servicio marcado como no disponible.
        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' no está disponible para reservar."
            )
        # Devuelve el servicio validado.
        return servicio

    @staticmethod
    def _validar_duracion(duracion):
        """Verifica que la duración sea un número mayor que cero."""
        # Si no se envió duración, es un parámetro faltante.
        if duracion is None:
            raise ParametroFaltanteError("La duración de la reserva es obligatoria.")
        # Se rechaza bool porque en Python True y False también cuentan como números.
        if isinstance(duracion, bool) or not isinstance(duracion, Real):
            raise DatoInvalidoError("La duración de la reserva debe ser numérica.")
        # La duración debe ser positiva.
        if duracion <= 0:
            raise DatoInvalidoError("La duración de la reserva debe ser mayor que cero.")
        # Devuelve la duración validada.
        return duracion

    # Cambia el estado y lo registra en el historial (uso interno).
    def _cambiar_estado(self, nuevo_estado):
        """Actualiza el estado de la reserva y lo agrega al historial."""
        # Guarda el nuevo estado.
        self._estado = nuevo_estado
        # Agrega el nuevo estado a la lista interna del historial.
        self._historial.append(nuevo_estado)


#PROPIEDADES DE SOLO LECTURA.

    @property
    def cliente(self):
        """Devuelve el cliente de la reserva."""
        return self._cliente

    @property
    def servicio(self):
        """Devuelve el servicio reservado."""
        return self._servicio

    @property
    def duracion(self):
        """Devuelve la duración de la reserva."""
        return self._duracion

    @property
    def estado(self):
        """Devuelve el estado actual de la reserva."""
        return self._estado

    @property
    def costo(self):
        """Devuelve el costo calculado al confirmar (None si aún no se confirma)."""
        return self._costo

    @property
    def historial(self):
        """Devuelve una copia del historial de estados para que no se modifique desde afuera."""
        return list(self._historial)

    @property
    def intentos_procesamiento(self):
        """Devuelve cuántas veces se intentó procesar la reserva."""
        return self._intentos_procesamiento

    #OPERACIONES DE LA RESERVA 

    def confirmar(self, impuesto: Real = 0.0, descuento: Optional[Real] = None):
        """Confirma la reserva y calcula su costo con el servicio asociado.

        Solo se puede confirmar una reserva PENDIENTE. Si el servicio no permite
        calcular el costo (no disponible, duración excesiva, descuento inválido...),
        se lanza ReservaInvalidaError encadenada al error original. 
        Si no se envía descuento (None), cada servicio decide su descuento por
        defecto; por ejemplo, el alquiler de equipos aplica su descuento automático.
        """
        # Regla de estado: solo una reserva pendiente puede confirmarse.
        if self._estado != self.PENDIENTE:
            raise ReservaInvalidaError(
                f"No se puede confirmar la reserva #{self.id}: su estado es {self._estado}."
            )
        try:
            # Polimorfismo: cada servicio calcula el costo a su manera.
            costo = self._servicio.calcular_costo(
                self._duracion, impuesto=impuesto, descuento=descuento
            )
        except SoftwareFJError as error:
            # Encadenamiento: se informa que la reserva falló y se conserva la causa real.
            raise ReservaInvalidaError(
                f"No se pudo confirmar la reserva #{self.id}: {error}"
            ) from error
        else:
            # else: solo se ejecuta si el cálculo del costo no lanzó ninguna excepción.
            self._costo = costo
            self._cambiar_estado(self.CONFIRMADA)
        # Devuelve el costo calculado para que quien confirme pueda mostrarlo.
        return self._costo

    def cancelar(self):
        """Cancela la reserva si está PENDIENTE o CONFIRMADA."""
        # Una reserva ya cancelada o procesada no se puede cancelar.
        if self._estado in (self.CANCELADA, self.PROCESADA):
            raise ReservaInvalidaError(
                f"No se puede cancelar la reserva #{self.id}: su estado es {self._estado}."
            )
        # Cambia el estado a CANCELADA y lo registra en el historial.
        self._cambiar_estado(self.CANCELADA)

    def procesar(self):
        """Procesa (ejecuta) una reserva CONFIRMADA.

        Antes de procesar revalida al cliente y al servicio. Usa try/except/else/finally:
        el bloque finally cuenta el intento aunque el procesamiento falle.
        """
        try:
            # Regla de estado: solo una reserva confirmada puede procesarse.
            if self._estado != self.CONFIRMADA:
                raise ReservaInvalidaError(
                    f"No se puede procesar la reserva #{self.id}: su estado es {self._estado}."
                )
            # Revalida los datos del cliente por si cambiaron después de crear la reserva.
            self._cliente.validar()
            # Revalida los datos del servicio.
            self._servicio.validar()
            # Verifica que el servicio siga disponible al momento de procesar.
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self._servicio.nombre}' dejó de estar disponible."
                )
        except ReservaInvalidaError:
            # Si el error ya es de reserva, se vuelve a lanzar tal cual.
            raise
        except SoftwareFJError as error:
            # Cualquier otro error del sistema se encadena como error de reserva.
            raise ReservaInvalidaError(
                f"No se pudo procesar la reserva #{self.id}: {error}"
            ) from error
        else:
            # else: solo si todas las validaciones pasaron, la reserva queda procesada.
            self._cambiar_estado(self.PROCESADA)
        finally:
            # finally: se ejecuta siempre, haya error o no, para contar el intento.
            self._intentos_procesamiento += 1

#METODOS OBLIGATORIOS DE ENTIDAD

    def validar(self):
        """Revalida cliente, servicio, duración y estado de la reserva."""
        # Reutiliza las validaciones internas sobre los datos actuales.
        self._validar_cliente(self._cliente)
        self._validar_duracion(self._duracion)
        # El servicio se revalida sin exigir disponibilidad, porque una reserva
        # cancelada o procesada puede tener un servicio que ya no esté disponible.
        if not isinstance(self._servicio, Servicio):
            raise DatoInvalidoError("El servicio de la reserva debe ser un objeto Servicio.")
        # Verifica que el estado sea uno de los permitidos.
        if self._estado not in (self.PENDIENTE, self.CONFIRMADA, self.CANCELADA, self.PROCESADA):
            raise ReservaInvalidaError(f"Estado de reserva desconocido: {self._estado}.")
        # Si nada falló, la reserva es válida.
        return True

    def describir(self):
        """Devuelve una descripción legible de la reserva."""
        # Si aún no hay costo, se indica como pendiente de cálculo.
        costo = f"{self._costo:,.2f}" if self._costo is not None else "sin calcular"
        # Arma la descripción con datos del cliente, el servicio y el estado.
        return (
            f"Reserva #{self.id}: {self._cliente.nombre} | Servicio: {self._servicio.nombre} | "
            f"Duración: {self._duracion} | Estado: {self._estado} | Costo: {costo}"
        )

