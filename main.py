"""
Programa principal de demostración de Software FJ.

Ejecuta operaciones válidas e inválidas sin detenerse ante los errores.
"""

# Importa las excepciones propias que pueden detener una operación individual.
from software_fj.exceptions.excepciones import SoftwareFJError

# Importa el gestor central del sistema.
from software_fj.gestor import GestorSistema

# Importa las clases del dominio utilizadas en la simulación.
from software_fj.models.cliente import Cliente
from software_fj.services.asesoria import Asesoria
from software_fj.services.equipo import AlquilerEquipo
from software_fj.services.sala import ReservaSala

# Importa el logger centralizado.
from software_fj.utils.logger import obtener_logger


def main() -> None:
    """Ejecuta al menos once operaciones y muestra un resumen final."""
    # Crea el gestor que conservará clientes, servicios y reservas.
    gestor = GestorSistema()
    # Obtiene el logger compartido para mensajes de operaciones.
    logger = obtener_logger()
    # Cuenta las operaciones que terminan con error.
    operaciones_fallidas = 0
    # Conserva referencias de objetos creados en operaciones anteriores.
    cliente_valido = None
    sala_valida = None

    print("1. Registrar cliente válido")
    try:
        # Crea un cliente con datos válidos.
        cliente_valido = Cliente("1234567890", "Ana Ruiz", "ana@gmail.com", "3001234567")
        # Lo registra en el gestor.
        gestor.registrar_cliente(cliente_valido)
        # Informa el resultado exitoso.
        print("OK:", cliente_valido.nombre)
    except SoftwareFJError as error:
        operaciones_fallidas += 1
        logger.error(error.mensaje)
        print("ERROR:", error.mensaje)
    except Exception as error:
        operaciones_fallidas += 1
        logger.error(f"Error inesperado: {error}")
        print("ERROR inesperado:", error)
    finally:
        logger.info("Fin de la operación 1.")

    print("2. Registrar cliente con correo inválido")
    try:
        # El constructor falla al validar el formato del correo.
        Cliente("9876543210", "Luis Perez", "correo-sin-arroba", "3012345678")
    except SoftwareFJError as error:
        operaciones_fallidas += 1
        logger.error(error.mensaje)
        print("ERROR:", error.mensaje)
    except Exception as error:
        operaciones_fallidas += 1
        logger.error(f"Error inesperado: {error}")
        print("ERROR inesperado:", error)
    finally:
        logger.info("Fin de la operación 2.")

    print("3. Intentar registrar documento duplicado")
    try:
        # Usa el mismo documento del cliente creado en la operación 1.
        duplicado = Cliente("1234567890", "Pedro Gomez", "pedro@gmail.com", "3023456789")
        gestor.registrar_cliente(duplicado)
    except SoftwareFJError as error:
        operaciones_fallidas += 1
        logger.error(error.mensaje)
        print("ERROR:", error.mensaje)
    except Exception as error:
        operaciones_fallidas += 1
        logger.error(f"Error inesperado: {error}")
        print("ERROR inesperado:", error)
    finally:
        logger.info("Fin de la operación 3.")

    print("4. Registrar sala válida")
    try:
        # Crea una sala disponible y la registra.
        sala_valida = ReservaSala("Sala Bogotá", 100000, 12)
        gestor.registrar_servicio(sala_valida)
        print("OK:", sala_valida.describir())
    except SoftwareFJError as error:
        operaciones_fallidas += 1
        logger.error(error.mensaje)
        print("ERROR:", error.mensaje)
    except Exception as error:
        operaciones_fallidas += 1
        logger.error(f"Error inesperado: {error}")
        print("ERROR inesperado:", error)
    finally:
        logger.info("Fin de la operación 4.")

    print("5. Crear sala con capacidad cero")
    try:
        # El setter de capacidad rechaza el valor cero.
        ReservaSala("Sala inválida", 50000, 0)
    except SoftwareFJError as error:
        operaciones_fallidas += 1
        logger.error(error.mensaje)
        print("ERROR:", error.mensaje)
    except Exception as error:
        operaciones_fallidas += 1
        logger.error(f"Error inesperado: {error}")
        print("ERROR inesperado:", error)
    finally:
        logger.info("Fin de la operación 5.")

    print("6. Registrar equipo válido")
    try:
        # Crea y registra un alquiler de equipos disponible.
        equipo = AlquilerEquipo("Videobeam", 50000, 2)
        gestor.registrar_servicio(equipo)
        print("OK:", equipo.describir())
    except SoftwareFJError as error:
        operaciones_fallidas += 1
        logger.error(error.mensaje)
        print("ERROR:", error.mensaje)
    except Exception as error:
        operaciones_fallidas += 1
        logger.error(f"Error inesperado: {error}")
        print("ERROR inesperado:", error)
    finally:
        logger.info("Fin de la operación 6.")

    print("7. Registrar asesoría válida")
    try:
        # Crea y registra una asesoría disponible.
        asesoria = Asesoria("Mentoría técnica", 80000, "Ingeniería", "EXPERTO")
        gestor.registrar_servicio(asesoria)
        print("OK:", asesoria.describir())
    except SoftwareFJError as error:
        operaciones_fallidas += 1
        logger.error(error.mensaje)
        print("ERROR:", error.mensaje)
    except Exception as error:
        operaciones_fallidas += 1
        logger.error(f"Error inesperado: {error}")
        print("ERROR inesperado:", error)
    finally:
        logger.info("Fin de la operación 7.")

    print("8. Crear, confirmar y procesar reserva exitosa")
    try:
        # Verifica que existan el cliente y la sala creados antes.
        if cliente_valido is None or sala_valida is None:
            raise SoftwareFJError("No existen los datos necesarios para esta reserva.")
        reserva = gestor.crear_reserva(cliente_valido, sala_valida, 2)
        costo = reserva.confirmar(impuesto=0.19)
        reserva.procesar()
        print("OK:", reserva.describir(), "Costo:", costo)
    except SoftwareFJError as error:
        operaciones_fallidas += 1
        logger.error(error.mensaje)
        print("ERROR:", error.mensaje)
    except Exception as error:
        operaciones_fallidas += 1
        logger.error(f"Error inesperado: {error}")
        print("ERROR inesperado:", error)
    finally:
        logger.info("Fin de la operación 8.")

    print("9. Reservar sala por más de 12 horas")
    try:
        # Confirma una sala fuera del límite permitido.
        if cliente_valido is None or sala_valida is None:
            raise SoftwareFJError("No existen los datos necesarios para esta reserva.")
        reserva_larga = gestor.crear_reserva(cliente_valido, sala_valida, 13)
        reserva_larga.confirmar()
    except SoftwareFJError as error:
        operaciones_fallidas += 1
        logger.error(error.mensaje)
        print("ERROR:", error.mensaje)
    except Exception as error:
        operaciones_fallidas += 1
        logger.error(f"Error inesperado: {error}")
        print("ERROR inesperado:", error)
    finally:
        logger.info("Fin de la operación 9.")

    print("10. Reservar servicio no disponible")
    try:
        # Crea una sala marcada como no disponible.
        sala_inactiva = ReservaSala("Sala cerrada", 60000, 8, disponible=False)
        if cliente_valido is None:
            raise SoftwareFJError("No existe el cliente necesario para esta reserva.")
        gestor.crear_reserva(cliente_valido, sala_inactiva, 2)
    except SoftwareFJError as error:
        operaciones_fallidas += 1
        logger.error(error.mensaje)
        print("ERROR:", error.mensaje)
    except Exception as error:
        operaciones_fallidas += 1
        logger.error(f"Error inesperado: {error}")
        print("ERROR inesperado:", error)
    finally:
        logger.info("Fin de la operación 10.")

    print("11. Cancelar reserva e intentar procesarla")
    try:
        # Crea una nueva reserva, la cancela y luego intenta procesarla.
        if cliente_valido is None or sala_valida is None:
            raise SoftwareFJError("No existen los datos necesarios para esta reserva.")
        reserva_cancelada = gestor.crear_reserva(cliente_valido, sala_valida, 3)
        reserva_cancelada.cancelar()
        reserva_cancelada.procesar()
    except SoftwareFJError as error:
        operaciones_fallidas += 1
        logger.error(error.mensaje)
        print("ERROR:", error.mensaje)
    except Exception as error:
        operaciones_fallidas += 1
        logger.error(f"Error inesperado: {error}")
        print("ERROR inesperado:", error)
    finally:
        logger.info("Fin de la operación 11.")

    print("12. Alquiler de equipo por 7 días con descuento automático")
    try:
        # Crea el equipo y confirma por siete días sin descuento explícito.
        equipo_largo = AlquilerEquipo("Portátil", 100000, 1)
        gestor.registrar_servicio(equipo_largo)
        if cliente_valido is None:
            raise SoftwareFJError("No existe el cliente necesario para esta reserva.")
        reserva_equipo = gestor.crear_reserva(
            cliente_valido, equipo_largo, AlquilerEquipo.DIAS_PARA_DESCUENTO
        )
        costo_equipo = reserva_equipo.confirmar()
        print("OK: costo con descuento automático =", costo_equipo)
    except SoftwareFJError as error:
        operaciones_fallidas += 1
        logger.error(error.mensaje)
        print("ERROR:", error.mensaje)
    except Exception as error:
        operaciones_fallidas += 1
        logger.error(f"Error inesperado: {error}")
        print("ERROR inesperado:", error)
    finally:
        logger.info("Fin de la operación 12.")

    # Imprime el resumen solicitado al finalizar todas las operaciones.
    print("\nResumen:")
    print("Clientes registrados:", len(gestor.obtener_clientes()))
    print("Servicios registrados:", len(gestor.obtener_servicios()))
    print("Reservas registradas:", len(gestor.obtener_reservas()))
    print("Operaciones fallidas:", operaciones_fallidas)
    # Registra el resumen final en el log.
    logger.info(
        "Resumen final: "
        f"{len(gestor.obtener_clientes())} clientes, "
        f"{len(gestor.obtener_servicios())} servicios, "
        f"{len(gestor.obtener_reservas())} reservas, "
        f"{operaciones_fallidas} operaciones fallidas."
    )


# Permite ejecutar este archivo directamente con python main.py.
if __name__ == "__main__":
    main()
