from web3 import Web3

from web3.exceptions import Web3Exception

# Intentar conectarse a la red de Ganache

try:
    
    ganache_url = "http://localhost:7545"
    
    w3 = Web3(Web3.HTTPProvider(ganache_url))
    
    if not w3.is_connected():
        
        print("No se pudo conectar a Ganache. Asegúrate de que Ganache esté en funcionamiento.")
    
    exit()

except Exception as e:

    print(f"Error al intentar conectar con Ganache: {e}")
    
    exit()

print("Conectado a Ganache")

# Direccion del contrato inteligente desplegado
contract_address = "0xD5566f96683EA5b3a5b22E59B81FD6A314C34B18" #

# Direccion del socio principal
socio_principal_address = "0x857CF9b70bC9f0a8AE0CB55FE28F8058dcC5815E"

# Clave privada del socio principal (necesaria para firmar transacciones)
socio_principal_private_key = "0xf6a20bcf17f23964480c1f4eb1464b1aea6290362b63c272692ac9f27d4e540f" #


contract_abi = json.loads ([{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"}],"name":"GarantiaLiquidada","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"tiempoLimite","type":"uint256"}],"name":"PrestamoAprobado","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"}],"name":"PrestamoReembolsado","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"plazo","type":"uint256"}],"name":"SolicitudPrestamo","type":"event"},{"inputs":[{"internalType":"address","name":"nuevoCliente","type":"address"}],"name":"altaCliente","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"nuevoPrestamista","type":"address"}],"name":"altaPrestamista","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"},{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"aprobarPrestamo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"depositarGarantia","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"},{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"liquidarGarantia","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"},{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"obtenerDetalleDePrestamo","outputs":[{"components":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"address","name":"prestatario","type":"address"},{"internalType":"uint256","name":"monto","type":"uint256"},{"internalType":"uint256","name":"plazo","type":"uint256"},{"internalType":"uint256","name":"tiempoSolicitud","type":"uint256"},{"internalType":"uint256","name":"tiempoLimite","type":"uint256"},{"internalType":"bool","name":"aprobado","type":"bool"},{"internalType":"bool","name":"reembolsado","type":"bool"},{"internalType":"bool","name":"liquidado","type":"bool"}],"internalType":"struct Banco.Prestamo","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"}],"name":"obtenerPrestamosPorPrestatario","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"reembolsarPrestamo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"socioPrincipal","outputs":[{"internalType":"address payable","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"monto_","type":"uint256"},{"internalType":"uint256","name":"plazo_","type":"uint256"}],"name":"solicitarPrestamo","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}])
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# 5.1 Función: alta_prestamista
def alta_prestamista(nuevo_prestamista_address):
    try:
        nonce = w3.eth.getTransactionCount(socio_principal_address)
        tx = contract.functions.altaPrestamista(nuevo_prestamista_address).buildTransaction({
            'chainId': 5777,  # Ganache chain ID
            'gas': 300000,
            'gasPrice': w3.toWei('1', 'gwei'),
            'nonce': nonce,
        })
        signed_tx = w3.eth.account.signTransaction(tx, private_key=socio_principal_private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        return "Prestamista agregado exitosamente" if receipt.status == 1 else "Error al agregar prestamista"
    except Exception as e:
        return f"Error al intentar agregar prestamista: {e}"

# 5.2 Función: alta_cliente
def alta_cliente(nuevo_cliente_address, prestamista_address, prestamista_private_key):
    try:
        nonce = w3.eth.getTransactionCount(prestamista_address)
        tx = contract.functions.altaCliente(nuevo_cliente_address).buildTransaction({
            'chainId': 5777,  # Ganache chain ID
            'gas': 300000,
            'gasPrice': w3.toWei('1', 'gwei'),
            'nonce': nonce,
        })
        signed_tx = w3.eth.account.signTransaction(tx, private_key=prestamista_private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        return "Cliente registrado exitosamente" if receipt.status == 1 else "Error al registrar cliente"
    except Exception as e:
        return f"Error al intentar registrar cliente: {e}"

# 5.3 Función: depositar_garantia
def depositar_garantia(direccion_cliente, valor, clave_privada_cliente):
    try:
        nonce = w3.eth.getTransactionCount(direccion_cliente)
        tx = contract.functions.depositarGarantia().buildTransaction({
            'chainId': 5777,  # Ganache chain ID
            'gas': 300000,
            'gasPrice': w3.toWei('1', 'gwei'),
            'nonce': nonce,
            'value': valor,
        })
        signed_tx = w3.eth.account.signTransaction(tx, private_key=clave_privada_cliente)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        return "Garantía depositada exitosamente" if receipt.status == 1 else "Error al depositar garantía"
    except Exception as e:
        return f"Error al intentar depositar garantía: {e}"

# 5.4 Función: solicitar_prestamo
def solicitar_prestamo(direccion_cliente, monto, plazo, clave_privada_cliente):
    try:
        # Verificar si el cliente tiene suficiente garantía
        saldo_garantia = contract.functions.clientes(direccion_cliente).call()['saldoGarantia']
        if saldo_garantia < monto:
            return "Saldo de garantía insuficiente"
        
        # Preparar la transacción para solicitar el préstamo
        nonce = w3.eth.getTransactionCount(direccion_cliente)
        tx = contract.functions.solicitarPrestamo(monto, plazo).buildTransaction({
            'chainId': 5777,  # Ganache chain ID
            'gas': 300000,
            'gasPrice': w3.toWei('1', 'gwei'),
            'nonce': nonce,
        })
        
        # Firmar la transacción con la clave privada del cliente
        signed_tx = w3.eth.account.signTransaction(tx, private_key=clave_privada_cliente)
        
        # Enviar la transacción
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        
        # Esperar la confirmación de la transacción
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        
        # Obtener el ID del préstamo solicitado
        nuevo_id_prestamo = contract.events.SolicitudPrestamo().processReceipt(receipt)[0]['args']['monto']
        
        return f"Solicitud de préstamo exitosa. ID del préstamo: {nuevo_id_prestamo}"
    except Exception as e:
        return f"Error al intentar solicitar préstamo: {e}"

# 5.5 Función: aprobar_prestamo
def aprobar_prestamo(prestatario_address, prestamo_id, prestamista_address, prestamista_private_key):
    try:
        # Comprobar si el préstamo y el prestatario son válidos
        prestamo_info = contract.functions.obtenerDetalleDePrestamo(prestatario_address, prestamo_id).call()
        if prestamo_info['id'] == 0:
            return "El préstamo no existe"
        elif prestamo_info['aprobado']:
            return "El préstamo ya está aprobado"
        
        # Preparar la transacción para aprobar el préstamo
        nonce = w3.eth.getTransactionCount(prestamista_address)
        tx = contract.functions.aprobarPrestamo(prestatario_address, prestamo_id).buildTransaction({
            'chainId': 5777,  # Ganache chain ID
            'gas': 300000,
            'gasPrice': w3.toWei('1', 'gwei'),
            'nonce': nonce,
        })
        
        # Firmar la transacción con la clave privada del prestamista
        signed_tx = w3.eth.account.signTransaction(tx, private_key=prestamista_private_key)
        
        # Enviar la transacción
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        
        # Esperar la confirmación de la transacción
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        
        return "Préstamo aprobado exitosamente" if receipt.status == 1 else "Error al aprobar préstamo"
    except Exception as e:
        return f"Error al intentar aprobar préstamo: {e}"

# 5.6 Función: reembolsar_prestamo
def reembolsar_prestamo(prestamo_id, cliente_address, cliente_private_key):
    try:
        # Obtener detalles del préstamo
        prestamo_info = contract.functions.obtenerDetalleDePrestamo(cliente_address, prestamo_id).call()
        
        # Verificar si el préstamo es válido y si el cliente es el prestatario
        if prestamo_info['id'] == 0:
            return "El préstamo no existe"
        elif not prestamo_info['aprobado']:
            return "El préstamo no está aprobado"
        elif prestamo_info['reembolsado']:
            return "El préstamo ya ha sido reembolsado"
        elif prestamo_info['prestatario'] != cliente_address:
            return "No tienes permisos para reembolsar este préstamo"
        
        # Preparar la transacción para reembolsar el préstamo
        nonce = w3.eth.getTransactionCount(cliente_address)
        tx = contract.functions.reembolsarPrestamo(prestamo_id).buildTransaction({
            'chainId': 5777,  # Ganache chain ID
            'gas': 300000,
            'gasPrice': w3.toWei('1', 'gwei'),
            'nonce': nonce,
        })
        
        # Firmar la transacción con la clave privada del cliente
        signed_tx = w3.eth.account.signTransaction(tx, private_key=cliente_private_key)
        
        # Enviar la transacción
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        
        # Esperar la confirmación de la transacción
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        
        return "Préstamo reembolsado exitosamente" if receipt.status == 1 else "Error al reembolsar préstamo"
    except Exception as e:
        return f"Error al intentar reembolsar préstamo: {e}"

# 5.7 Función: liquidar_garantia
def liquidar_garantia(prestamo_id, prestamista_address, prestamista_private_key):
    try:
        # Obtener detalles del préstamo
        prestamo_info = contract.functions.obtenerDetalleDePrestamo(prestamista_address, prestamo_id).call()
        
        # Verificar si el préstamo está aprobado, no reembolsado y ha vencido el plazo
        if prestamo_info['id'] == 0:
            return "El préstamo no existe"
        elif not prestamo_info['aprobado']:
            return "El préstamo no está aprobado"
        elif prestamo_info['reembolsado']:
            return "El préstamo ya ha sido reembolsado"
        elif prestamo_info['liquidado']:
            return "La garantía ya ha sido liquidada"
        elif prestamo_info['tiempoLimite'] >= w3.eth.getBlock('latest')['timestamp']:
            return "El plazo del préstamo no ha vencido"
        
        # Preparar la transacción para liquidar la garantía
        nonce = w3.eth.getTransactionCount(prestamista_address)
        tx = contract.functions.liquidarGarantia(prestamista_address, prestamo_id).buildTransaction({
            'chainId': 5777,  # Ganache chain ID
            'gas': 300000,
            'gasPrice': w3.toWei('1', 'gwei'),
            'nonce': nonce,
        })
        
        # Firmar la transacción con la clave privada del prestamista
        signed_tx = w3.eth.account.signTransaction(tx, private_key=prestamista_private_key)
        
        # Enviar la transacción
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        
        # Esperar la confirmación de la transacción
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        
        return "Garantía liquidada exitosamente" if receipt.status == 1 else "Error al liquidar garantía"
    except Exception as e:
        return f"Error al intentar liquidar garantía: {e}"

# 5.8 Función: obtener_prestamos_por_prestatario
def obtener_prestamos_por_prestatario(prestatario_address):
    try:
        # Llamar a la función del contrato para obtener los préstamos del prestatario
        prestamo_ids = contract.functions.obtenerPrestamosPorPrestatario(prestatario_address).call()
        return prestamo_ids
    except Exception as e:
        return f"Error al intentar obtener préstamos por prestatario: {e}"

# 5.9 Función: obtener_detalle_de_prestamo
def obtener_detalle_de_prestamo(prestatario_address, prestamo_id):
    try:
        # Llamar a la función del contrato para obtener los detalles del préstamo
        detalle_prestamo = contract.functions.obtenerDetalleDePrestamo(prestatario_address, prestamo_id).call()
        return detalle_prestamo
    except Exception as e:
        return f"Error al intentar obtener detalle de préstamo: {e}"
