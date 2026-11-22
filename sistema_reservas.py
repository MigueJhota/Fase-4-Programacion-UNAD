
"""
UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
Curso: Programacion
Fase 4 - Componente practico - Practicas simuladas

Proyecto:
Sistema Integral de Gestion de Clientes,
Servicios y Reservas

Empresa ficticia: Software FJ

El programa utiliza:
- Programacion orientada a objetos
- Herencia y clases abstractas
- Encapsulamiento
- Polimorfismo
- Sobrecarga simulada
- Excepciones personalizadas
- Registro de eventos y errores
- Pruebas de funcionamiento

No utiliza bases de datos.
"""

from abc import ABC, abstractmethod
from datetime import datetime


# ==========================================
# 1. EXCEPCIONES PERSONALIZADAS
# ==========================================

class ErrorSistema(Exception):
    """Excepcion general del sistema."""
    pass


class ErrorCliente(ErrorSistema):
    """Error relacionado con los clientes."""
    pass


class ErrorServicio(ErrorSistema):
    """Error relacionado con los servicios."""
    pass


class ErrorReserva(ErrorSistema):
    """Error relacionado con las reservas."""
    pass


# ==========================================
# 2. REGISTRO DE EVENTOS Y ERRORES
# ==========================================

def registrar_evento(mensaje, tipo="INFO"):
    """
    Guarda los eventos en un archivo de texto.
    El argumento tipo permite simular sobrecarga.
    """

    fecha = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    linea = f"[{fecha}] [{tipo}] {mensaje}"

    try:
        with open(
            "registro_sistema.txt",
            "a",
            encoding="utf-8"
        ) as archivo:
            archivo.write(linea + "\n")

    except OSError as error:
        print("No se pudo guardar el registro:", error)


# ==========================================
# 3. CLASE ABSTRACTA ENTIDAD
# ==========================================

class Entidad(ABC):

    def __init__(self, identificador):

        if not isinstance(identificador, int):
            raise ValueError(
                "El identificador debe ser numerico."
            )

        if identificador <= 0:
            raise ValueError(
                "El identificador debe ser positivo."
            )

        self._identificador = identificador

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def mostrar_informacion(self):
        pass


# ==========================================
# 4. CLASE CLIENTE
# ==========================================

class Cliente(Entidad):

    def __init__(self, identificador, nombre, correo):

        try:
            super().__init__(identificador)

            if not isinstance(nombre, str):
                raise ValueError(
                    "El nombre debe ser texto."
                )

            if not nombre.strip():
                raise ValueError(
                    "El nombre no puede estar vacio."
                )

            if not isinstance(correo, str):
                raise ValueError(
                    "El correo debe ser texto."
                )

            partes = correo.split("@")

            if (
                len(partes) != 2
                or not partes[0]
                or "." not in partes[1]
                or partes[1].startswith(".")
                or partes[1].endswith(".")
                or " " in correo
            ):
                raise ValueError(
                    "El correo electronico no es valido."
                )

            self.__nombre = nombre.strip()
            self.__correo = correo.strip()

        except ValueError as error:
            raise ErrorCliente(
                f"No se pudo crear el cliente: {error}"
            ) from error

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    def mostrar_informacion(self):
        return (
            f"Cliente {self.identificador}: "
            f"{self.__nombre} - {self.__correo}"
        )


# ==========================================
# 5. CLASE ABSTRACTA SERVICIO
# ==========================================

class Servicio(Entidad, ABC):

    def __init__(
        self,
        identificador,
        nombre,
        precio_base
    ):

        try:
            super().__init__(identificador)

            if not isinstance(nombre, str):
                raise ValueError(
                    "El nombre del servicio debe ser texto."
                )

            if not nombre.strip():
                raise ValueError(
                    "El servicio debe tener un nombre."
                )

            if (
                isinstance(precio_base, bool)
                or not isinstance(
                    precio_base, (int, float)
                )
                or precio_base <= 0
            ):
                raise ValueError(
                    "El precio debe ser mayor que cero."
                )

            self._nombre = nombre
            self._precio_base = precio_base

        except ValueError as error:
            raise ErrorServicio(
                f"Servicio invalido: {error}"
            ) from error

    @property
    def nombre(self):
        return self._nombre

    @abstractmethod
    def calcular_costo(self, cantidad=1):
        pass

    def mostrar_informacion(self):
        return (
            f"Servicio {self.identificador}: "
            f"{self._nombre} - "
            f"Tarifa base: ${self._precio_base:.2f}"
        )


# ==========================================
# 6. SERVICIO DE RESERVA DE SALAS
# ==========================================

class ReservaSala(Servicio):

    def __init__(
        self,
        identificador,
        nombre,
        precio_hora,
        capacidad
    ):

        super().__init__(
            identificador,
            nombre,
            precio_hora
        )

        if (
            not isinstance(capacidad, int)
            or isinstance(capacidad, bool)
            or capacidad <= 0
        ):
            raise ErrorServicio(
                "La capacidad debe ser positiva."
            )

        self.__capacidad = capacidad

    def calcular_costo(self, cantidad=1):

        validar_cantidad(cantidad)

        return self._precio_base * cantidad

    def mostrar_informacion(self):
        return (
            super().mostrar_informacion()
            + f" | Capacidad: {self.__capacidad}"
            + " personas"
        )


# ==========================================
# 7. SERVICIO DE ALQUILER DE EQUIPOS
# ==========================================

class AlquilerEquipo(Servicio):

    def __init__(
        self,
        identificador,
        nombre,
        precio_dia,
        tipo_equipo
    ):

        super().__init__(
            identificador,
            nombre,
            precio_dia
        )

        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ErrorServicio(
                "Debe indicar el tipo de equipo."
            )

        self.__tipo_equipo = tipo_equipo

    def calcular_costo(self, cantidad=1):

        validar_cantidad(cantidad)

        return self._precio_base * cantidad

    def mostrar_informacion(self):
        return (
            super().mostrar_informacion()
            + f" | Equipo: {self.__tipo_equipo}"
        )


# ==========================================
# 8. SERVICIO DE CONSULTORIA
# ==========================================

class ConsultoriaEspecializada(Servicio):

    def __init__(
        self,
        identificador,
        nombre,
        precio_hora,
        especialidad
    ):

        super().__init__(
            identificador,
            nombre,
            precio_hora
        )

        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ErrorServicio(
                "Debe indicar una especialidad."
            )

        self.__especialidad = especialidad

    def calcular_costo(self, cantidad=1):

        validar_cantidad(cantidad)

        return self._precio_base * cantidad

    def mostrar_informacion(self):
        return (
            super().mostrar_informacion()
            + f" | Especialidad: {self.__especialidad}"
        )


# ==========================================
# 9. VALIDACION DE CANTIDADES
# ==========================================

def validar_cantidad(cantidad):

    if (
        isinstance(cantidad, bool)
        or not isinstance(cantidad, (int, float))
        or cantidad <= 0
    ):
        raise ErrorServicio(
            "La cantidad debe ser mayor que cero."
        )


# ==========================================
# 10. CLASE RESERVA
# ==========================================

class Reserva(Entidad):

    def __init__(
        self,
        identificador,
        cliente,
        servicio,
        cantidad=1
    ):

        try:
            super().__init__(identificador)

        except ValueError as error:
            raise ErrorReserva(
                f"Identificador invalido: {error}"
            ) from error

        if not isinstance(cliente, Cliente):
            raise ErrorReserva(
                "La reserva requiere un cliente valido."
            )

        if not isinstance(servicio, Servicio):
            raise ErrorReserva(
                "La reserva requiere un servicio valido."
            )

        try:
            validar_cantidad(cantidad)

        except ErrorServicio as error:
            raise ErrorReserva(
                f"Cantidad invalida: {error}"
            ) from error

        self.__cliente = cliente
        self.__servicio = servicio
        self.__cantidad = cantidad
        self.__estado = "PENDIENTE"

    @property
    def estado(self):
        return self.__estado

    def confirmar(self):

        if self.__estado != "PENDIENTE":
            raise ErrorReserva(
                "Solo se confirman reservas pendientes."
            )

        self.__estado = "CONFIRMADA"

        registrar_evento(
            f"Reserva {self.identificador} confirmada."
        )

    def cancelar(self):

        if self.__estado == "CANCELADA":
            raise ErrorReserva(
                "La reserva ya esta cancelada."
            )

        if self.__estado == "PROCESADA":
            raise ErrorReserva(
                "No se puede cancelar una reserva procesada."
            )

        self.__estado = "CANCELADA"

        registrar_evento(
            f"Reserva {self.identificador} cancelada."
        )

    def procesar(self):

        if self.__estado != "CONFIRMADA":
            raise ErrorReserva(
                "Solo se procesan reservas confirmadas."
            )

        costo = self.__servicio.calcular_costo(
            self.__cantidad
        )

        self.__estado = "PROCESADA"

        registrar_evento(
            f"Reserva {self.identificador} procesada. "
            f"Total: ${costo:.2f}"
        )

        return costo

    def mostrar_informacion(self):

        return (
            f"Reserva {self.identificador} | "
            f"Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | "
            f"Cantidad: {self.__cantidad} | "
            f"Estado: {self.__estado}"
        )


# ==========================================
# 11. SISTEMA DE GESTION
# ==========================================

class SistemaGestion:

    def __init__(self):

        self.clientes = {}
        self.servicios = {}
        self.reservas = {}

    def agregar_cliente(self, cliente):

        if not isinstance(cliente, Cliente):
            raise ErrorCliente(
                "El objeto no es un cliente valido."
            )

        if cliente.identificador in self.clientes:
            raise ErrorCliente(
                "Ya existe un cliente con ese ID."
            )

        self.clientes[cliente.identificador] = cliente

        registrar_evento(
            f"Cliente registrado: {cliente.nombre}"
        )

    def agregar_servicio(self, servicio):

        if not isinstance(servicio, Servicio):
            raise ErrorServicio(
                "El objeto no es un servicio valido."
            )

        if servicio.identificador in self.servicios:
            raise ErrorServicio(
                "Ya existe un servicio con ese ID."
            )

        self.servicios[servicio.identificador] = servicio

        registrar_evento(
            f"Servicio registrado: {servicio.nombre}"
        )

    def agregar_reserva(self, reserva):

        if not isinstance(reserva, Reserva):
            raise ErrorReserva(
                "El objeto no es una reserva valida."
            )

        if reserva.identificador in self.reservas:
            raise ErrorReserva(
                "Ya existe una reserva con ese ID."
            )

        self.reservas[reserva.identificador] = reserva

        registrar_evento(
            f"Reserva creada: {reserva.identificador}"
        )

    def mostrar_clientes(self):

        print("\nCLIENTES REGISTRADOS:")

        for cliente in self.clientes.values():
            print(cliente.mostrar_informacion())

    def mostrar_servicios(self):

        print("\nSERVICIOS DISPONIBLES:")

        for servicio in self.servicios.values():
            print(servicio.mostrar_informacion())

    def mostrar_reservas(self):

        print("\nRESERVAS REGISTRADAS:")

        for reserva in self.reservas.values():
            print(reserva.mostrar_informacion())


# ==========================================
# 12. FUNCION PARA EJECUTAR PRUEBAS
# ==========================================

def ejecutar_prueba(numero, descripcion, funcion):

    print("\n" + "-" * 55)
    print(f"PRUEBA {numero}: {descripcion}")
    print("-" * 55)

    try:
        resultado = funcion()

    except ErrorSistema as error:

        print("ERROR CONTROLADO:", error)

        registrar_evento(
            f"Prueba {numero}: {error}",
            "ERROR"
        )

    except ValueError as error:

        print("ERROR DE VALOR:", error)

        registrar_evento(
            f"Prueba {numero}: {error}",
            "ERROR"
        )

    except Exception as error:

        print("ERROR INESPERADO:", error)

        registrar_evento(
            f"Prueba {numero}: {error}",
            "ERROR"
        )

    else:

        print("Operacion ejecutada correctamente.")

        if resultado is not None:
            print("Resultado:", resultado)

        registrar_evento(
            f"Prueba {numero} completada.",
            "EXITO"
        )

    finally:

        print(f"Fin de la prueba {numero}.")


# ==========================================
# 13. SIMULACION DE OPERACIONES
# ==========================================

def main():

    print("=" * 60)
    print(" UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA")
    print(" FASE 4 - PROGRAMACION")
    print(" SISTEMA INTEGRAL DE GESTION - SOFTWARE FJ")
    print("=" * 60)

    registrar_evento(
        "Inicio de la simulacion del sistema."
    )

    sistema = SistemaGestion()

    # --------------------------------------
    # PRUEBA 1: Cliente valido
    # --------------------------------------

    def prueba_1():
        cliente = Cliente(
            1,
            "Carlos Perez",
            "carlos@gmail.com"
        )
        sistema.agregar_cliente(cliente)
        return cliente.mostrar_informacion()

    ejecutar_prueba(
        1,
        "Registrar cliente valido",
        prueba_1
    )

    # --------------------------------------
    # PRUEBA 2: Otro cliente valido
    # --------------------------------------

    def prueba_2():
        cliente = Cliente(
            2,
            "Ana Gomez",
            "ana@gmail.com"
        )
        sistema.agregar_cliente(cliente)
        return cliente.mostrar_informacion()

    ejecutar_prueba(
        2,
        "Registrar segundo cliente",
        prueba_2
    )

    # --------------------------------------
    # PRUEBA 3: Nombre vacio
    # --------------------------------------

    ejecutar_prueba(
        3,
        "Intentar registrar nombre vacio",
        lambda: Cliente(
            3,
            "",
            "prueba@gmail.com"
        )
    )

    # --------------------------------------
    # PRUEBA 4: Correo incorrecto
    # --------------------------------------

    ejecutar_prueba(
        4,
        "Intentar registrar correo invalido",
        lambda: Cliente(
            4,
            "Pedro",
            "correo_incorrecto"
        )
    )

    # --------------------------------------
    # PRUEBA 5: Cliente duplicado
    # --------------------------------------

    ejecutar_prueba(
        5,
        "Intentar registrar cliente duplicado",
        lambda: sistema.agregar_cliente(
            Cliente(
                1,
                "Otro Cliente",
                "otro@gmail.com"
            )
        )
    )

    # --------------------------------------
    # PRUEBA 6: Reserva de sala
    # --------------------------------------

    def prueba_6():
        servicio = ReservaSala(
            101,
            "Sala de reuniones",
            50,
            20
        )
        sistema.agregar_servicio(servicio)
        return servicio.mostrar_informacion()

    ejecutar_prueba(
        6,
        "Registrar servicio de salas",
        prueba_6
    )

    # --------------------------------------
    # PRUEBA 7: Alquiler de equipos
    # --------------------------------------

    def prueba_7():
        servicio = AlquilerEquipo(
            102,
            "Alquiler de computadores",
            80,
            "Computador portatil"
        )
        sistema.agregar_servicio(servicio)
        return servicio.mostrar_informacion()

    ejecutar_prueba(
        7,
        "Registrar alquiler de equipos",
        prueba_7
    )

    # --------------------------------------
    # PRUEBA 8: Consultoria
    # --------------------------------------

    def prueba_8():
        servicio = ConsultoriaEspecializada(
            103,
            "Consultoria tecnologica",
            120,
            "Desarrollo de software"
        )
        sistema.agregar_servicio(servicio)
        return servicio.mostrar_informacion()

    ejecutar_prueba(
        8,
        "Registrar consultoria especializada",
        prueba_8
    )

    # --------------------------------------
    # PRUEBA 9: Servicio con precio invalido
    # --------------------------------------

    ejecutar_prueba(
        9,
        "Intentar registrar servicio con precio negativo",
        lambda: ReservaSala(
            104,
            "Sala incorrecta",
            -50,
            10
        )
    )

    # --------------------------------------
    # PRUEBA 10: Crear reserva valida
    # --------------------------------------

    def prueba_10():
        reserva = Reserva(
            201,
            sistema.clientes[1],
            sistema.servicios[101],
            3
        )
        sistema.agregar_reserva(reserva)
        return reserva.mostrar_informacion()

    ejecutar_prueba(
        10,
        "Crear reserva de sala por tres horas",
        prueba_10
    )

    # --------------------------------------
    # PRUEBA 11: Confirmar reserva
    # --------------------------------------

    ejecutar_prueba(
        11,
        "Confirmar reserva 201",
        lambda: sistema.reservas[201].confirmar()
    )

    # --------------------------------------
    # PRUEBA 12: Procesar reserva
    # --------------------------------------

    ejecutar_prueba(
        12,
        "Procesar reserva confirmada",
        lambda: sistema.reservas[201].procesar()
    )

    # --------------------------------------
    # PRUEBA 13: Procesar nuevamente
    # --------------------------------------

    ejecutar_prueba(
        13,
        "Intentar procesar reserva ya procesada",
        lambda: sistema.reservas[201].procesar()
    )

    # --------------------------------------
    # PRUEBA 14: Crear reserva de equipo
    # --------------------------------------

    def prueba_14():
        reserva = Reserva(
            202,
            sistema.clientes[2],
            sistema.servicios[102],
            2
        )
        sistema.agregar_reserva(reserva)
        return reserva.mostrar_informacion()

    ejecutar_prueba(
        14,
        "Crear reserva de alquiler de equipos",
        prueba_14
    )

    # --------------------------------------
    # PRUEBA 15: Cancelar reserva
    # --------------------------------------

    ejecutar_prueba(
        15,
        "Cancelar reserva pendiente",
        lambda: sistema.reservas[202].cancelar()
    )

    # --------------------------------------
    # PRUEBA 16: Confirmar cancelada
    # --------------------------------------

    ejecutar_prueba(
        16,
        "Intentar confirmar reserva cancelada",
        lambda: sistema.reservas[202].confirmar()
    )

    # --------------------------------------
    # PRUEBA 17: Cantidad invalida
    # --------------------------------------

    ejecutar_prueba(
        17,
        "Intentar crear reserva con cantidad negativa",
        lambda: Reserva(
            203,
            sistema.clientes[1],
            sistema.servicios[103],
            -2
        )
    )

    # --------------------------------------
    # PRUEBA 18: Polimorfismo
    # --------------------------------------

    def prueba_18():

        print("Calculo polimorfico de servicios:")

        for servicio in sistema.servicios.values():

            costo = servicio.calcular_costo(2)

            print(
                f"{servicio.nombre}: "
                f"2 unidades = ${costo:.2f}"
            )

    ejecutar_prueba(
        18,
        "Demostrar polimorfismo",
        prueba_18
    )

    # --------------------------------------
    # PRUEBA 19: Sobrecarga simulada
    # --------------------------------------

    def prueba_19():

        servicio = sistema.servicios[101]

        costo_normal = servicio.calcular_costo()

        costo_tres = servicio.calcular_costo(3)

        print(
            f"Sin argumento: ${costo_normal:.2f}"
        )

        print(
            f"Con tres unidades: ${costo_tres:.2f}"
        )

    ejecutar_prueba(
        19,
        "Demostrar sobrecarga simulada",
        prueba_19
    )

    # --------------------------------------
    # PRUEBA 20: Reserva de consultoria
    # --------------------------------------

    def prueba_20():

        reserva = Reserva(
            204,
            sistema.clientes[2],
            sistema.servicios[103],
            4
        )

        sistema.agregar_reserva(reserva)

        reserva.confirmar()

        costo = reserva.procesar()

        return f"Consultoria procesada: ${costo:.2f}"

    ejecutar_prueba(
        20,
        "Crear, confirmar y procesar consultoria",
        prueba_20
    )

    # ======================================
    # 14. REPORTE FINAL
    # ======================================

    print("\n" + "=" * 60)
    print(" REPORTE FINAL DEL SISTEMA")
    print("=" * 60)

    sistema.mostrar_clientes()
    sistema.mostrar_servicios()
    sistema.mostrar_reservas()

    print("\nRESUMEN:")

    print(
        "Clientes registrados:",
        len(sistema.clientes)
    )

    print(
        "Servicios registrados:",
        len(sistema.servicios)
    )

    print(
        "Reservas registradas:",
        len(sistema.reservas)
    )

    print("Operaciones simuladas: 20")

    print("\nArchivo de registro:")
    print("registro_sistema.txt")

    registrar_evento(
        "Simulacion finalizada correctamente."
    )

    print("\nPROGRAMA FINALIZADO CORRECTAMENTE")
    print("=" * 60)


# ==========================================
# 15. INICIO DEL PROGRAMA
# ==========================================

if __name__ == "__main__":
    main()
