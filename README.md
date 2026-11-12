# Software FJ

Sistema de gestión de clientes, servicios y reservas desarrollado en Python.

## Estructura inicial

```text
software-fj/
├── software_fj/
│   ├── models/          # Entidades y clases del dominio
│   ├── services/        # Lógica de gestión de servicios y reservas
│   └── exceptions/      # Excepciones personalizadas
├── tests/               # Pruebas del proyecto
├── docs/                # Documentación adicional
├── logs/                # Registros generados durante la ejecución
├── main.py              # Punto de entrada de la aplicación
├── CONTRIBUTING.md      # Convenciones y reglas de colaboración
└── README.md
```

## Requisitos principales

- Implementar clientes, servicios especializados y reservas.
- Validar los datos recibidos y las operaciones permitidas.
- Definir excepciones personalizadas.
- Registrar errores y eventos relevantes.
- Incluir pruebas y una demostración de al menos diez operaciones.

La información se manejará mediante objetos y listas en memoria. No se
utilizarán bases de datos; los archivos se reservarán para registrar eventos y
errores.
