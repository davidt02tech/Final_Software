import unittest
from datetime import datetime
from app import Cuenta, Operacion, buscar_cuenta_por_numero

class TestCuentas(unittest.TestCase):
    def setUp(self):
        # Configurar el estado inicial para las pruebas
        self.cuenta1 = Cuenta("21345", "Arnaldo", 200, ["123", "456"])
        self.cuenta2 = Cuenta("123", "Luisa", 400, ["456"])
        self.cuenta3 = Cuenta("456", "Andrea", 300, ["21345"])
        self.cuentas = [self.cuenta1, self.cuenta2, self.cuenta3]
        self.operaciones = []
        self.fecha_actual = datetime.now().strftime("%d/%m/%Y")

    def test_pagar_exitoso(self):
        # Prueba para verificar el pago exitoso
        self.assertTrue(self.cuenta1.pagar("456", 100))
        self.assertEqual(len(self.operaciones), 1)
        self.assertEqual(self.operaciones[0].remitente, "21345")
        self.assertEqual(self.operaciones[0].numero_destino, "456")
        self.assertEqual(self.operaciones[0].fecha, self.fecha_actual)
        self.assertEqual(self.operaciones[0].valor, 100)


    def test_pagar_saldo_insuficiente(self):
        # Prueba para verificar el pago con saldo insuficiente
        self.assertFalse(self.cuenta1.pagar("456", 300))
        self.assertEqual(len(self.operaciones), 0)  # No se debe agregar ninguna operación a la lista

    def test_pagar_destino_no_en_contactos(self):
        # Prueba para verificar el pago a un destino no presente en la lista de contactos
        self.assertFalse(self.cuenta1.pagar("123", 100))
        self.assertEqual(len(self.operaciones), 0)  # No se debe agregar ninguna operación a la lista

    def test_pagar_cuenta_no_encontrada(self):
        # Prueba para verificar el pago desde una cuenta no encontrada
        self.assertFalse(self.cuenta1.pagar("789", 100))
        self.assertEqual(len(self.operaciones), 0)  # No se debe agregar ninguna operación a la lista