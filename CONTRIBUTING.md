# Guía de contribución

## Convenciones de nombres

- Archivos y carpetas: `snake_case`.
- Clases: `PascalCase`.
- Funciones, métodos y variables: `snake_case`.
- Constantes: `MAYUSCULAS_CON_GUION_BAJO`.
- Mantener una responsabilidad clara por archivo.
- Usar nombres descriptivos y evitar abreviaturas innecesarias.

## Responsabilidades por carpeta

| Carpeta | Responsabilidad |
|---|---|
| `software_fj/models/` | Clases y entidades del dominio. |
| `software_fj/services/` | Lógica de gestión y operaciones del sistema. |
| `software_fj/exceptions/` | Excepciones personalizadas. |
| `tests/` | Pruebas automatizadas. |
| `docs/` | Documentación adicional. |
| `logs/` | Registros generados durante la ejecución. |

## Reglas de trabajo

- Coordinar antes de modificar archivos que utilicen otros integrantes.
- No guardar información en bases de datos; el proyecto utiliza objetos y
  listas en memoria.
- No subir archivos de logs, credenciales ni configuraciones locales.
- Probar los cambios antes de integrarlos.
- Mantener los cambios relacionados con una sola tarea.
- Usar mensajes de commit claros y descriptivos.
