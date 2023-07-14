from flask import Flask, request, jsonify
from datetime import datetime
import uuid
app = Flask(__name__)


class Cuenta:
    def __init__(self, numero, nombre, saldo, contactos):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos
    # : Muestra el saldo y la lista de operaciones, tanto de envío como de recepción de dinero
    def historial(self):
        # Obtener la lista de operaciones de la cuenta
        operaciones_cuenta = []
        for operacion in operaciones:
            if operacion.numero_destino == self.numero:
                operaciones_cuenta.append(operacion)
        return operaciones_cuenta
        
    

    def pagar(self, destino, valor):
        # Transfiere un valor a otro número (debe ser un contacto). La cuenta debe tener
        # saldo suficiente para hacer la transferencia
        if destino in self.contactos:
            if self.saldo >= valor:
                operacion = Operacion(self.numero, destino, datetime.now(), valor)
                operaciones.append(operacion)
                self.saldo -= valor
                destino_cuenta = buscar_cuenta_por_numero(destino)
                destino_cuenta.saldo += valor
                return True
            else:
                return False

class Operacion:
    def __init__(self, remitente, numero_destino, fecha, valor):
        self.remitente = remitente
        self.numero_destino = numero_destino
        self.fecha = fecha
        self.valor = valor

# Mock de Cuentas y Operaciones
cuentas = [
    Cuenta("21345", "Arnaldo", 200, ["123", "456"]),
    Cuenta("123", "Luisa", 400, ["456"]),
    Cuenta("456", "Andrea", 300, ["21345"])
]

operaciones = [
]

def buscar_cuenta_por_numero(numero):
    for cuenta in cuentas:
        if cuenta.numero == numero:
            return cuenta
    return None

def buscar_nombre_cuenta_por_numero(numero):
    for cuenta in cuentas:
        if cuenta.numero == numero:
            return cuenta.nombre
    return None

@app.route("/billetera/contactos", methods=["GET"])
def obtener_contactos():
    numero = request.args.get("minumero")
    cuenta = buscar_cuenta_por_numero(numero)
    if cuenta:
        contactos = cuenta.contactos
        contactos_dict = {}
        for contacto in contactos:
            contactos_dict[contacto] = buscar_nombre_cuenta_por_numero(contacto)
        return jsonify(contactos_dict)

@app.route("/billetera/pagar", methods=["POST"])
def pagar():
    numero = request.args.get('minumero')
    destino = request.args.get('numerodestino')
    valor = int(request.args.get('valor'))
    cuenta = buscar_cuenta_por_numero(numero)
    if cuenta:
        if cuenta.pagar(destino, valor):
            fecha_actual = datetime.now().strftime("%d/%m/%Y")
            return f"Pago realizado en {fecha_actual}"
        else:
            return "Saldo insuficiente"
    else:
        return "Cuenta no encontrada"

@app.route("/billetera/historial", methods=["GET"])
def historial():
    numero = request.args.get('minumero')
    cuenta = buscar_cuenta_por_numero(numero)
    if cuenta:
        operaciones_cuenta = cuenta.historial()
        operaciones_dict = {}
        operaciones_dict["Saldo de " +  cuenta.nombre] = cuenta.saldo
        operaciones_dict["Operaciones de " + cuenta.nombre] = {}
        for operacion in operaciones_cuenta:
            codigo_operacion = str(uuid.uuid4())
            if operacion.remitente == numero:
                operaciones_dict["Operaciones de " + cuenta.nombre][codigo_operacion] = f"Enviado a {buscar_nombre_cuenta_por_numero(operacion.numero_destino)} el valor de {operacion.valor}"
            else:
                operaciones_dict["Operaciones de " + cuenta.nombre][codigo_operacion] = f"Recibido de {buscar_nombre_cuenta_por_numero(operacion.remitente)} el valor de {operacion.valor}"
        
        return jsonify(operaciones_dict)


if __name__ == "__main__":
    app.run(debug=True)