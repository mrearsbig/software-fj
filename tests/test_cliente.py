"""
Pruebas automáticas de la clase Cliente y de la clase abstracta Entidad.

Cada prueba verifica un caso válido o inválido. Para ejecutarlas, desde la
carpeta raíz del proyecto (software-fj):

    python -m unittest discover tests -v
"""

# Importa unittest, el módulo de pruebas que viene incluido en Python.
import unittest

# Importa la clase que se va a probar.
from software_fj.models.cliente import Cliente

# Importa la clase abstracta para comprobar que no se puede instanciar.
from software_fj.models.entidad import Entidad

# Importa las excepciones que se espera que lance Cliente.
from software_fj.exceptions.excepciones import (
    SoftwareFJError,
    DatoInvalidoError,
    ParametroFaltanteError,
)


# Datos de un cliente válido, reutilizados en todas las pruebas.
# Se pueden cambiar por otros datos, siempre que cumplan las reglas de Cliente:
# documento de 6 a 10 números, nombre solo con letras minimo y un espacio entre palabras,
# correo con @ y punto, y teléfono de 10 dígitos.
DATOS_VALIDOS = {
    "documento": "1234567890",
    "nombre": "Jesús Beltrán",
    "correo": "jesus@gmail.com",
    "telefono": "3001234567",
}


# Función auxiliar: crea un cliente con los datos válidos, cambiando solo los indicados.
def crear_cliente(**cambios):
    """Crea un Cliente partiendo de DATOS_VALIDOS y reemplazando los campos recibidos."""
    # Copia los datos válidos para no modificar el diccionario original.
    datos = dict(DATOS_VALIDOS)
    # Reemplaza solo los campos que la prueba quiere cambiar.
    datos.update(cambios)
    # Crea y devuelve el cliente (puede lanzar una excepción si algún dato es inválido).
    return Cliente(**datos)


# Grupo de pruebas de la clase abstracta Entidad.
class PruebasEntidad(unittest.TestCase):
    """Pruebas de la clase abstracta Entidad."""

    # Una clase abstracta no debe poder crearse directamente.
    def test_entidad_no_se_puede_instanciar(self):
        # assertRaises verifica que el bloque lance el error indicado.
        with self.assertRaises(TypeError):
            Entidad()


# Grupo de pruebas de casos válidos de Cliente.
class PruebasClienteValido(unittest.TestCase):
    """Casos en los que el cliente debe crearse correctamente."""

    # Un cliente con todos los datos correctos se crea sin errores.
    def test_crea_cliente_valido(self):
        cliente = crear_cliente()
        # Compara contra DATOS_VALIDOS: si cambian esos datos, la prueba se adapta sola.
        self.assertEqual(cliente.documento, DATOS_VALIDOS["documento"])
        self.assertEqual(cliente.nombre, DATOS_VALIDOS["nombre"])
        # El correo se guarda en minúsculas, por eso se compara con .lower().
        self.assertEqual(cliente.correo, DATOS_VALIDOS["correo"].lower())
        self.assertEqual(cliente.telefono, DATOS_VALIDOS["telefono"])

    # Los espacios sobrantes se eliminan y el correo se guarda en minúsculas.
    def test_limpia_espacios_y_normaliza_correo(self):
        cliente = crear_cliente(
            # Agrega espacios al inicio y al final del documento.
            documento=f"  {DATOS_VALIDOS['documento']}  ",
            # Agrega espacios afuera y repite los espacios internos del nombre.
            nombre=f"  {DATOS_VALIDOS['nombre'].replace(' ', '    ')} ",
            # Envía el correo en mayúsculas.
            correo=DATOS_VALIDOS["correo"].upper(),
        )
        self.assertEqual(cliente.documento, DATOS_VALIDOS["documento"])
        self.assertEqual(cliente.nombre, DATOS_VALIDOS["nombre"])
        self.assertEqual(cliente.correo, DATOS_VALIDOS["correo"].lower())

    # validar() devuelve True cuando todos los datos son correctos.
    def test_validar_devuelve_true(self):
        self.assertTrue(crear_cliente().validar())

    # describir() oculta el documento excepto los últimos 4 dígitos.
    def test_describir_oculta_documento(self):
        documento = DATOS_VALIDOS["documento"]
        # Calcula cómo debería verse el documento oculto, sin escribirlo a mano.
        oculto = "*" * (len(documento) - 4) + documento[-4:]
        descripcion = crear_cliente().describir()
        self.assertIn(oculto, descripcion)
        self.assertNotIn(documento, descripcion)

    # Cada cliente recibe un id distinto y mayor que el anterior.
    def test_ids_unicos_y_consecutivos(self):
        primero = crear_cliente()
        segundo = crear_cliente()
        self.assertEqual(segundo.id, primero.id + 1)

    # Un intento fallido no gasta un id.
    def test_cliente_fallido_no_gasta_id(self):
        primero = crear_cliente()
        # Intento inválido entre dos clientes válidos.
        with self.assertRaises(SoftwareFJError):
            crear_cliente(documento="abc")
        segundo = crear_cliente()
        self.assertEqual(segundo.id, primero.id + 1)


# Grupo de pruebas de datos inválidos: cada una debe lanzar la excepción correcta.
# Aquí los datos se escriben a propósito, porque cada uno prueba una regla específica.
class PruebasClienteInvalido(unittest.TestCase):
    """Casos en los que el cliente NO debe crearse."""

    # Documento con letras.
    def test_documento_con_letras(self):
        with self.assertRaises(DatoInvalidoError):
            crear_cliente(documento="12ab34")

    # Documento demasiado corto.
    def test_documento_muy_corto(self):
        with self.assertRaises(DatoInvalidoError):
            crear_cliente(documento="123")

    # Documento demasiado largo.
    def test_documento_muy_largo(self):
        with self.assertRaises(DatoInvalidoError):
            crear_cliente(documento="12345678901")

    # Documento enviado como número: verifica también el encadenamiento de excepciones.
    def test_documento_no_texto_encadena_error(self):
        with self.assertRaises(DatoInvalidoError) as contexto:
            crear_cliente(documento=12345678)
        # __cause__ guarda la excepción original gracias a "raise ... from error".
        self.assertIsInstance(contexto.exception.__cause__, AttributeError)

    # Nombre vacío o solo con espacios.
    def test_nombre_vacio(self):
        with self.assertRaises(ParametroFaltanteError):
            crear_cliente(nombre="   ")

    # Nombre no enviado (None).
    def test_nombre_faltante(self):
        with self.assertRaises(ParametroFaltanteError):
            crear_cliente(nombre=None)

    # Nombre con números.
    def test_nombre_con_numeros(self):
        with self.assertRaises(DatoInvalidoError):
            crear_cliente(nombre="Ana2")

    # Nombre demasiado corto.
    def test_nombre_muy_corto(self):
        with self.assertRaises(DatoInvalidoError):
            crear_cliente(nombre="Al")

    # Correo sin arroba.
    def test_correo_sin_arroba(self):
        with self.assertRaises(DatoInvalidoError):
            crear_cliente(correo="jesusgmail.com")

    # Correo sin dominio con punto.
    def test_correo_sin_punto_en_dominio(self):
        with self.assertRaises(DatoInvalidoError):
            crear_cliente(correo="jesus@gmail")

    # Teléfono con menos dígitos.
    def test_telefono_corto(self):
        with self.assertRaises(DatoInvalidoError):
            crear_cliente(telefono="300123")

    # Teléfono con letras.
    def test_telefono_con_letras(self):
        with self.assertRaises(DatoInvalidoError):
            crear_cliente(telefono="300abc4567")

    # La validación también se aplica al modificar un dato después de crear el cliente.
    def test_modificar_con_dato_invalido(self):
        cliente = crear_cliente()
        with self.assertRaises(DatoInvalidoError):
            cliente.correo = "correo-invalido"
        # El correo original se conserva porque el cambio fue rechazado.
        self.assertEqual(cliente.correo, DATOS_VALIDOS["correo"].lower())


# Permite ejecutar este archivo directamente con: python tests/test_cliente.py
if __name__ == "__main__":
    unittest.main()