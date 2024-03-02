# Importar el módulo para interactuar con el contrato inteligente
import PrestamoDeFi as pd

# Función para dar de alta un prestamista
def dar_alta_prestamista():
    nuevo_prestamista_address = input("Introduce la dirección del nuevo prestamista: ")
    resultado = pd.alta_prestamista(nuevo_prestamista_address)
    print(resultado)

# Función para dar de alta un cliente
def dar_alta_cliente():
    nuevo_cliente_address = input("Introduce la dirección del nuevo cliente: ")
    prestamista_address = input("Introduce la dirección del prestamista que registra al cliente: ")
    prestamista_private_key = input("Introduce la clave privada del prestamista: ")
    resultado = pd.alta_cliente(nuevo_cliente_address, prestamista_address, prestamista_private_key)
    print(resultado)

# Función para depositar garantía
def depositar_garantia():
    direccion_cliente = input("Introduce la dirección del cliente: ")
    valor = float(input("Introduce el monto de la garantía a depositar: "))
    clave_privada_cliente = input("Introduce la clave privada del cliente: ")
    resultado = pd.depositar_garantia(direccion_cliente, valor, clave_privada_cliente)
    print(resultado)

# Función para solicitar un préstamo
def solicitar_prestamo():
    direccion_cliente = input("Introduce la dirección del cliente: ")
    monto = float(input("Introduce el monto del préstamo solicitado: "))
    plazo = int(input("Introduce el plazo del préstamo en segundos: "))
    clave_privada_cliente = input("Introduce la clave privada del cliente: ")
    resultado = pd.solicitar_prestamo(direccion_cliente, monto, plazo, clave_privada_cliente)
    print(resultado)

# Función para aprobar un préstamo
def aprobar_prestamo():
    prestatario_address = input("Introduce la dirección del prestatario: ")
    prestamo_id = int(input("Introduce el ID del préstamo a aprobar: "))
    prestamista_address = input("Introduce la dirección del prestamista: ")
    prestamista_private_key = input("Introduce la clave privada del prestamista: ")
    resultado = pd.aprobar_prestamo(prestatario_address, prestamo_id, prestamista_address, prestamista_private_key)
    print(resultado)

# Función para reembolsar un préstamo
def reembolsar_prestamo():
    prestamo_id = int(input("Introduce el ID del préstamo a reembolsar: "))
    cliente_address = input("Introduce la dirección del cliente: ")
    cliente_private_key = input("Introduce la clave privada del cliente: ")
    resultado = pd.reembolsar_prestamo(prestamo_id, cliente_address, cliente_private_key)
    print(resultado)

# Función para liquidar garantía
def liquidar_garantia():
    prestamo_id = int(input("Introduce el ID del préstamo cuya garantía será liquidada: "))
    prestamista_address = input("Introduce la dirección del prestamista: ")
    prestamista_private_key = input("Introduce la clave privada del prestamista: ")
    resultado = pd.liquidar_garantia(prestamo_id, prestamista_address, prestamista_private_key)
    print(resultado)

# Función para obtener préstamos por prestatario
def obtener_prestamos_por_prestatario():
    prestatario_address = input("Introduce la dirección del prestatario: ")
    resultado = pd.obtener_prestamos_por_prestatario(prestatario_address)
    print(resultado)

# Función para obtener detalle de préstamo
def obtener_detalle_de_prestamo():
    prestatario_address = input("Introduce la dirección del prestatario: ")
    prestamo_id = int(input("Introduce el ID del préstamo: "))
    resultado = pd.obtener_detalle_de_prestamo(prestatario_address, prestamo_id)
    print(resultado)

# Menú principal
def mostrar_menu():
    while True:
        print("\nMenú de Interacción con el Contrato:")
        print("1. Dar de alta un prestamista")
        print("2. Dar de alta un cliente")
        print("3. Depositar garantía")
        print("4. Solicitar un préstamo")
        print("5. Aprobar un préstamo")
        print("6. Reembolsar un préstamo")
        print("7. Liquidar garantía")
        print("8. Obtener préstamos por prestatario")
        print("9. Obtener detalle de préstamo")
        print("0. Salir")

        opcion = input("Elige una opción: ")

        if opcion == '1':
            dar_alta_prestamista()
        elif opcion == '2':
            dar_alta_cliente()
        elif opcion == '3':
            depositar_garantia()
        elif opcion == '4':
            solicitar_prestamo()
        elif opcion == '5':
            aprobar_prestamo()
        elif opcion == '6':
            reembolsar_prestamo()
        elif opcion == '7':
            liquidar_garantia()
        elif opcion == '8':
            obtener_prestamos_por_prestatario()
        elif opcion == '9':
            obtener_detalle_de_prestamo()
        elif opcion == '0':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, elige una opción del menú.")

if __name__ == "__main__":
    mostrar_menu()
