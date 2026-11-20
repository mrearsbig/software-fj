# Software FJ

Sistema de gestión de clientes, servicios y reservas desarrollado en Python.
El proyecto implementa un modelo de dominio orientado a objetos, con
validaciones, cálculo de costos, excepciones propias y ciclo de vida para las
reservas.

## Funcionalidades

- Gestión de clientes con validación de documento, nombre, correo y teléfono.
- Servicios especializados:
  - **Asesorías**, con niveles básico, avanzado y experto.
  - **Salas**, con capacidad y límite de 12 horas por reserva.
  - **Alquiler de equipos**, con unidades y descuento automático del 10 % para
    alquileres de 7 días o más.
- Cálculo de costos con descuentos e impuestos configurables.
- Flujo de reservas:
  `PENDIENTE → CONFIRMADA → PROCESADA`.
- Cancelación de reservas pendientes o confirmadas.
- Historial de estados e intentos de procesamiento.
- Excepciones personalizadas para datos inválidos, parámetros faltantes,
  servicios no disponibles y reservas inválidas.
- Datos gestionados en memoria, sin base de datos.

## Requisitos

- Python 3
- No se necesitan dependencias externas para ejecutar el proyecto o sus
  pruebas.

## Instalación

Clona el repositorio y entra en su directorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd software-fj
```

Opcionalmente, crea y activa un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate       # macOS/Linux
# .venv\Scripts\activate        # Windows
```

## Uso básico

El dominio puede utilizarse directamente desde Python:

```python
from software_fj.models.cliente import Cliente
from software_fj.models.reserva import Reserva
from software_fj.services.sala import ReservaSala

cliente = Cliente(
    documento="1234567890",
    nombre="Ana Ruiz",
    correo="ana@example.com",
    telefono="3001234567",
)
sala = ReservaSala(
    nombre="Sala principal",
    tarifa_base=100_000,
    capacidad=20,
)

reserva = Reserva(cliente, sala, duracion=2)
costo = reserva.confirmar(impuesto=0.19)
reserva.procesar()

print(reserva.describir())
print(f"Costo: ${costo:,.2f}")
```

Una reserva nueva comienza en estado `PENDIENTE`. Solo puede procesarse
después de confirmarse; si una operación no está permitida, se lanza una
excepción de `software_fj.exceptions.excepciones`.

## Ejecutar las pruebas

Desde la raíz del proyecto:

```bash
python3 -m unittest discover tests -v
```

Las pruebas cubren validaciones, polimorfismo, cálculo de costos, descuentos,
excepciones y las transiciones del ciclo de vida de una reserva.

## Estructura del proyecto

```text
software-fj/
├── software_fj/
│   ├── models/          # Entidades Cliente, Entidad y Reserva
│   ├── services/        # Servicio, asesorías, salas y equipos
│   └── exceptions/      # Jerarquía de excepciones del dominio
├── tests/               # Pruebas automatizadas con unittest
├── docs/                # Documentación adicional
├── logs/                # Registros generados durante la ejecución
├── main.py              # Punto de entrada de la aplicación
├── CONTRIBUTING.md      # Convenciones de colaboración
├── LICENSE              # Licencia MIT
└── README.md
```

## Reglas de validación destacadas

- Los datos obligatorios no pueden ser `None` ni quedar vacíos.
- Los documentos deben tener entre 6 y 10 dígitos.
- Los teléfonos deben tener exactamente 10 dígitos.
- Las tarifas, duraciones, capacidades y unidades deben ser positivas.
- Los descuentos e impuestos deben estar entre `0` y `1`.
- No se puede reservar un servicio marcado como no disponible.

## Contribuir

Consulta [CONTRIBUTING.md](CONTRIBUTING.md) para conocer las convenciones de
nombres, responsabilidades por carpeta y reglas de trabajo.

## Licencia

Este proyecto se distribuye bajo la [Licencia MIT](LICENSE).
