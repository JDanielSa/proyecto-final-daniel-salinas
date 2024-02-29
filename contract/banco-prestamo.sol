// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Banco {
    address payable public socioPrincipal;
    
    struct Prestamo {
        uint256 id;
        address prestatario;
        uint256 monto;
        uint256 plazo;
        uint256 tiempoSolicitud;
        uint256 tiempoLimite;
        bool aprobado;
        bool reembolsado;
        bool liquidado;
    }
    
    struct Cliente {
        bool activado;
        uint256 saldoGarantia;
        mapping (uint256 => Prestamo) prestamos;
        uint256[] prestamoIds; 
    }
    
    mapping(address => Cliente) private clientes;
    mapping(address => bool) private empleadosPrestamista;
        
    event SolicitudPrestamo(address indexed prestatario, uint256 monto, uint256 plazo);
    event PrestamoAprobado(address indexed prestatario, uint256 monto, uint256 tiempoLimite);
    event PrestamoReembolsado(address indexed prestatario, uint256 monto);
    event GarantiaLiquidada(address indexed prestatario, uint256 monto);

    modifier soloSocioPrincipal() {
        require(msg.sender == socioPrincipal, "No posee permisos para ejecutar esta accion");
        _;
    }
    modifier soloEmpleadoPrestamista() {
        require(empleadosPrestamista[msg.sender], "No es empleado");
        _;
    }
    modifier soloClienteRegistrado() {
        require(clientes[msg.sender].activado, "No es un cliente activo");
        _;
    }

    constructor() {
        socioPrincipal = payable(msg.sender);
        empleadosPrestamista[socioPrincipal] = true;
    }

    
    function altaPrestamista(address nuevoPrestamista) public soloSocioPrincipal {
    require(!empleadosPrestamista[nuevoPrestamista], "El prestamista ya esta dado de alta");

    empleadosPrestamista[nuevoPrestamista] = true;
    }

    function altaCliente(address nuevoCliente) public soloEmpleadoPrestamista {
    require(!clientes[nuevoCliente].activado, "El cliente ya esta dado de alta");

    Cliente storage structNuevoCliente = clientes[nuevoCliente];
    structNuevoCliente.saldoGarantia = 0;
    structNuevoCliente.activado = true;
    }

    function depositarGarantia() public payable soloClienteRegistrado {
    clientes[msg.sender].saldoGarantia += msg.value;
    }

    function solicitarPrestamo(uint256 monto_, uint256 plazo_) public soloClienteRegistrado returns (uint256) {
    // Comprobacion si el cliente tiene saldoGarantia suficiente
    require(clientes[msg.sender].saldoGarantia >= monto_, "Saldo de garantia insuficiente");

    // Se genra un nuevo ID
    uint256 nuevoId = clientes[msg.sender].prestamoIds.length + 1;

    // Se instacia el struct Prestamo
    Prestamo storage nuevoPrestamo = clientes[msg.sender].prestamos[nuevoId];

    // Se asignan los datos al préstamo
    nuevoPrestamo.id = nuevoId;
    nuevoPrestamo.prestatario = msg.sender;
    nuevoPrestamo.monto = monto_;
    nuevoPrestamo.plazo = plazo_;
    nuevoPrestamo.tiempoSolicitud = block.timestamp;
    nuevoPrestamo.tiempoLimite = 0;
    nuevoPrestamo.aprobado = false;
    nuevoPrestamo.reembolsado = false;
    nuevoPrestamo.liquidado = false;

    // Se añade el nuevoId al array prestamoIds
    clientes[msg.sender].prestamoIds.push(nuevoId);

    // Se emite el evento SolicitudPrestamo
    emit SolicitudPrestamo(msg.sender, monto_, plazo_);

    // Se devuelve el nuevoId como parámetro de salida
    return nuevoId;
    }

    function aprobarPrestamo(address prestatario_, uint256 id_) public soloEmpleadoPrestamista {
    // Se instancia una variable de tipo struct Cliente storage
    Cliente storage prestatario = clientes[prestatario_];

    // Se comprueba si el id del préstamo existe para el prestatario
    require(id_ > 0 && id_ <= prestatario.prestamoIds.length, "Id de prestamo no valido");

    // Se instancia una variable de tipo struct Prestamo storage
    Prestamo storage prestamo = prestatario.prestamos[id_];

    // Se comprueba si el préstamo no está aprobado, reembolsado ni liquidado
    require(!prestamo.aprobado, "El prestamo ya fue aprobado");
    require(!prestamo.reembolsado, "El prestamo ya fue reembolsado");
    require(!prestamo.liquidado, "El prestamo ya fue liquidado");

    // Se apruba el préstamo y establece el tiempo límite
    prestamo.aprobado = true;
    prestamo.tiempoLimite = block.timestamp + prestamo.plazo;

    // Se emite el evento PrestamoAprobado
    emit PrestamoAprobado(prestatario_, prestamo.monto, prestamo.tiempoLimite);
    }

    function reembolsarPrestamo(uint256 id_) public soloClienteRegistrado {
    // Se instancia una variable de tipo struct Cliente storage
    Cliente storage prestatario = clientes[msg.sender];

    // Se comprueba si el id del préstamo existe para el prestatario
    require(id_ > 0 && id_ <= prestatario.prestamoIds.length, "Id de prestamo no valido");

    // Se instancia una variable de tipo struct Prestamo storage
    Prestamo storage prestamo = prestatario.prestamos[id_];

    // Se comprueba las condiciones necesarias para reembolsar el préstamo
    require(prestamo.prestatario == msg.sender, "No tienes permisos para reembolsar este prestamo");
    require(prestamo.aprobado, "El prestamo no esta aprobado");
    require(!prestamo.reembolsado, "El prestamo ya esta reembolsado");
    require(!prestamo.liquidado, "El prestamo esta liquidado");
    require(prestamo.tiempoLimite >= block.timestamp, "El tiempo limite ha vencido");

    // Se trasfiere el monto al socioPrincipal del sistema
    socioPrincipal.transfer(prestamo.monto);

    // Se actualizan los campos del préstamo y del prestatario
    prestamo.reembolsado = true;
    prestatario.saldoGarantia -= prestamo.monto;

    // Se emite el evento PrestamoReembolsado
    emit PrestamoReembolsado(msg.sender, prestamo.monto);
    }
    
    function liquidarGarantia(address prestatario_, uint256 id_) public soloEmpleadoPrestamista {
    // Se instancia una variable de tipo struct Cliente storage
    Cliente storage prestatario = clientes[prestatario_];

    // Se comprueba si el id del préstamo existe para el prestatario
    require(id_ > 0 && id_ <= prestatario.prestamoIds.length, "Id de prestamo no valido");

    // Se instancia una variable de tipo struct Prestamo storage
    Prestamo storage prestamo = prestatario.prestamos[id_];

    // Se comprueba las condiciones necesarias para liquidar el préstamo
    require(prestamo.aprobado, "El prestamo no esta aprobado");
    require(!prestamo.reembolsado, "El prestamo ya fue reembolsado");
    require(!prestamo.liquidado, "El prestamo ya fue liquidado");
    require(prestamo.tiempoLimite < block.timestamp, "El tiempo limite no ha vencido");

    // Se trasfiere el monto al socioPrincipal del sistema
    socioPrincipal.transfer(prestamo.monto);

    // Se actualizan los campos del préstamo y del prestatario
    prestamo.liquidado = true;
    prestatario.saldoGarantia -= prestamo.monto;

    // Se emite el evento GarantiaLiquidada
    emit GarantiaLiquidada(prestatario_, prestamo.monto);
    }

    function obtenerPrestamosPorPrestatario(address prestatario_) public view returns (uint256[] memory) {
    // Se obtiene el array de prestamoIds del prestatario
    return clientes[prestatario_].prestamoIds;
    }

    function obtenerDetalleDePrestamo(address prestatario_, uint256 id_) public view returns (Prestamo memory) {
    // Se obtiene el struct Prestamo del prestatario con el id proporcionado
    return clientes[prestatario_].prestamos[id_];
    }
}