"""
Módulo de la clase abstracta Entidad del sistema Software FJ.

Define el molde general que comparten todas las entidades del sistema
(por ejemplo, clientes, servicios y reservas): un identificador único,
una fecha de creación y la obligación de saber describirse y validarse.
"""

# Importa ABC (clase base para abstractas) y abstractmethod (marca métodos obligatorios).
from abc import ABC, abstractmethod

# Importa datetime para registrar la fecha y hora de creación de cada entidad.
from datetime import datetime


# Hereda de ABC: esto convierte a Entidad en una clase abstracta,
# es decir, no se puede crear un objeto Entidad directamente, solo de sus hijas.
class Entidad(ABC):
    """Clase abstracta base para todas las entidades del sistema Software FJ."""

    # Atributo de clase compartido: cuenta cuántas entidades se han creado
    # para asignar a cada una un identificador único y consecutivo.
    _contador = 0

    # Constructor: se ejecuta cada vez que se crea una entidad hija.
    def __init__(self):
        # Aumenta el contador global de entidades en uno.
        Entidad._contador += 1
        # Asigna el valor actual del contador como identificador privado de la entidad.
        self._id = Entidad._contador
        # Guarda la fecha y hora exacta en que se creó la entidad.
        self._fecha_creacion = datetime.now()

    # Propiedad de solo lectura: permite consultar el id pero no modificarlo desde afuera.
    @property
    def id(self):
        """Devuelve el identificador único de la entidad."""
        # Retorna el atributo privado _id.
        return self._id

    # Propiedad de solo lectura: permite consultar la fecha de creación sin modificarla.
    @property
    def fecha_creacion(self):
        """Devuelve la fecha y hora en que se creó la entidad."""
        # Retorna el atributo privado _fecha_creacion.
        return self._fecha_creacion

    # Método abstracto: toda clase hija está obligada a implementarlo.
    @abstractmethod
    def describir(self):
        """Devuelve un texto que describe la entidad."""
        # pass: aquí no hay lógica; cada clase hija define su propia descripción.
        pass

    # Método abstracto: toda clase hija está obligada a implementarlo.
    @abstractmethod
    def validar(self):
        """Verifica que los datos de la entidad sean correctos.

        Debe lanzar una excepción personalizada si algún dato es inválido.
        """
        # pass: cada clase hija define sus propias reglas de validación.
        pass

    # Método especial: define qué se muestra al imprimir la entidad con print().
    def __str__(self):
        # Reutiliza describir(), así cada hija se imprime con su propia descripción.
        return self.describir()

    

