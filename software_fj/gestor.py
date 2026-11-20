"""
Gestor central de clientes, servicios y reservas de Software FJ.

Mantiene colecciones privadas y registra las operaciones relevantes
mediante el logger compartido del proyecto.
"""

# Importa las excepciones personalizadas del proyecto.
from software_fj.exceptions.excepciones import DatoInvalidoError, ParametroFaltanteError

# Importa las entidades administradas por el gestor.
from software_fj.models.cliente import Cliente
from software_fj.models.reserva import Reserva
from software_fj.services.servicio import Servicio

# Importa el logger centralizado.
from software_fj.utils.logger import obtener_logger


class GestorSistema:
    """Administra los datos principales de Software FJ."""

    # Constructor: inicializa las listas privadas que mantendrán los datos.
    def __init__(self) -> None:
        """Crea un gestor con listas internas vacías."""
        # Lista privada de clientes registrados.
        self._clientes: list[Cliente] = []
        # Lista privada de servicios ofrecidos.
        self._servicios: list[Servicio] = []
        # Lista privada de reservas creadas.
        self._reservas: list[Reserva] = []
        # Logger compartido usado por todas las operaciones.
        self._logger = obtener_logger()

    # Registra un cliente y rechaza documentos repetidos.
    def registrar_cliente(self, cliente: Cliente) -> Cliente:
        """Registra un Cliente válido o lanza DatoInvalidoError si está duplicado."""
        # Rechaza un valor ausente con la excepción propia correspondiente.
        if cliente is None:
            raise ParametroFaltanteError("El cliente es obligatorio.")
        # Rechaza un objeto que no sea de tipo Cliente.
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("El objeto registrado debe ser un Cliente.")
        # Revalida el cliente antes de agregarlo a la colección.
        cliente.validar()
        # Busca si ya existe algún cliente con el mismo documento.
        if any(item.documento == cliente.documento for item in self._clientes):
            # Construye el mensaje del error de documento duplicado.
            mensaje = f"Ya existe un cliente con el documento {cliente.documento}."
            # Registra el intento rechazado.
            self._logger.error(mensaje)
            # Lanza la excepción propia del proyecto.
            raise DatoInvalidoError(mensaje)
        # Agrega una copia de referencia del cliente validado a la lista.
        self._clientes.append(cliente)
        # Registra el evento correcto.
        self._logger.info(f"Cliente registrado: documento {cliente.documento}.")
        # Devuelve el cliente registrado para facilitar su uso.
        return cliente

    # Registra un servicio después de validarlo.
    def registrar_servicio(self, servicio: Servicio) -> Servicio:
        """Registra un Servicio válido."""
        # Rechaza un valor ausente con la excepción propia correspondiente.
        if servicio is None:
            raise ParametroFaltanteError("El servicio es obligatorio.")
        # Rechaza un objeto que no sea de tipo Servicio.
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("El objeto registrado debe ser un Servicio.")
        # Revalida el servicio antes de almacenarlo.
        servicio.validar()
        # Agrega el servicio a la lista privada.
        self._servicios.append(servicio)
        # Registra el evento de registro.
        self._logger.info(f"Servicio registrado: {servicio.nombre}.")
        # Devuelve el servicio registrado.
        return servicio

    # Crea y agrega una reserva al gestor.
    def crear_reserva(
        self, cliente: Cliente, servicio: Servicio, duracion: float
    ) -> Reserva:
        """Crea una Reserva con los datos recibidos y la agrega a la colección."""
        # Construye la reserva; sus validaciones pueden lanzar errores propios.
        reserva = Reserva(cliente, servicio, duracion)
        # Agrega la reserva creada a la lista privada.
        self._reservas.append(reserva)
        # Registra el evento relevante.
        self._logger.info(
            f"Reserva creada: #{reserva.id} para el cliente {cliente.documento}."
        )
        # Devuelve la reserva creada.
        return reserva

    # Devuelve una copia de la lista de clientes.
    def obtener_clientes(self) -> list[Cliente]:
        """Devuelve una copia de los clientes registrados."""
        return list(self._clientes)

    # Devuelve una copia de la lista de servicios.
    def obtener_servicios(self) -> list[Servicio]:
        """Devuelve una copia de los servicios registrados."""
        return list(self._servicios)

    # Devuelve una copia de la lista de reservas.
    def obtener_reservas(self) -> list[Reserva]:
        """Devuelve una copia de las reservas registradas."""
        return list(self._reservas)

    # Alias en español que puede utilizarse para consultar colecciones.
    def consultar_clientes(self) -> list[Cliente]:
        """Alias de obtener_clientes()."""
        return self.obtener_clientes()

    # Alias en español que puede utilizarse para consultar servicios.
    def consultar_servicios(self) -> list[Servicio]:
        """Alias de obtener_servicios()."""
        return self.obtener_servicios()

    # Alias en español que puede utilizarse para consultar reservas.
    def consultar_reservas(self) -> list[Reserva]:
        """Alias de obtener_reservas()."""
        return self.obtener_reservas()
