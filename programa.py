import datetime as dt

clientes = {}
salas = {}
reservas = {}

HOY = dt.datetime.today().date()
FECHA_MINIMA = HOY + dt.timedelta(days=2)
TURNOS = ("Matutino","Vespertino","Nocturno")

class Cliente:
    def __init__(self,nombre,apellido):
        self.id_cliente = max(clientes.keys(), default=0) + 1
        self.nombre = nombre
        self.apellido = apellido
    def getNombres(self):
        return f"{self.apellido} {self.nombre}"

class Sala:
    def __init__(self,nombre,cupo):
        self.id_sala = max(salas.keys(),default=0) + 1 
        self.nombre = nombre
        self.cupo = cupo

class Reserva:
    def __init__(self,objeto_cliente,objeto_sala,fecha,turno,nombre_evento):
        self.folio = max(reservas.keys(), default=0) + 1
        self.objeto_cliente = objeto_cliente
        self.objeto_sala = objeto_sala
        self.fecha = fecha
        self.nombre_evento = nombre_evento
        self.turno = turno

# Funciones auxiliares
def obtener_clientes():
    titulo("Clientes registrados")
    print(f"{'Clave':<8} {'Apellidos':<20} {'Nombres':<15}")
    sep(70)                                                 # K = Key 0   V = Value 1
    for clave, cliente in sorted(clientes.items(), key=lambda kv: (kv[1].apellido, kv[1].nombre)):
        print(f"{clave:<8} {cliente.apellido:<20} {cliente.nombre:<15}")
    sep(70)

def obtener_salas(fecha_procesada):
    titulo2(f"Salas disponibles para {fecha_procesada}")
    print(f"{'Clave':<8} {'Sala':<20} {'Cupo':<15} {'Turno disponible':<20}")
    sep(90)
    for clave, sala in salas.items():
        libres = filtro(sala, fecha_procesada)
        if not libres:
            print(f"{clave:<8} {sala.nombre:<20} {'':<15} {'SALA OCUPADA':<20}")
            continue
        print(f"{clave:<8} {sala.nombre:<20} {sala.cupo:<15} {" | ".join(libres):<20}")
    sep(90)

def filtro(sala, fecha_procesada):
    ocupados = obtener_turnos_ocupados(sala, fecha_procesada)
    libres = []
    for turno in TURNOS:
        if turno not in ocupados:
            libres.append(turno)
    return libres

def obtener_turnos_ocupados(sala, fecha):
    turnos_ocupados = []
    for reserva in reservas.values():
        if reserva.objeto_sala.id_sala == sala.id_sala and reserva.fecha == fecha:
            turnos_ocupados.append(reserva.turno)
    return turnos_ocupados

def mostrar_reserva(nuevo_evento, cliente_elegido, sala, fecha_procesada, nombre_evento):
    titulo("Reservación registrada exitosamente")
    print(f"Folio:   {nuevo_evento.folio}")
    print(f"Cliente: {cliente_elegido.getNombres()}")
    print(f"Sala:    {sala.nombre} | Cupo: {sala.cupo}")
    print(f"Fecha:   {fecha_procesada}")
    print(f"Evento:  {nombre_evento}")
    print(f"Turno:   {nuevo_evento.turno}")

def agregar_reservacion_turno(cliente_elegido, sala, fecha_procesada, turno_elegido):
    while True:
        nombre_evento = input("Ingrese el nombre del evento: ").strip()
        if not nombre_evento:
            print("El evento debe tener un nombre si o si")
            continue
        nuevo_evento = Reserva(cliente_elegido, sala, fecha_procesada, turno_elegido, nombre_evento)
        reservas[nuevo_evento.folio] = nuevo_evento
        mostrar_reserva(nuevo_evento, cliente_elegido, sala, fecha_procesada, nombre_evento)
        return

def mostrar_reservacion_fechas(fecha_inicio_procesada,fecha_fin_procesada,filtro_fechas):
    titulo2(f"Reservaciones para {fecha_inicio_procesada} - {fecha_fin_procesada}")
    print(f"{'Folio':<8}{'Cliente':<19}{'Fecha':<15}{'Nombre del evento':<20}{'Sala':<20}{'Turno':<10}")
    sep(90)
    for folio,reserva in filtro_fechas.items():
        print(f"{folio:<8}{reserva.objeto_cliente.nombre:<19}{str(reserva.fecha):<15}{reserva.nombre_evento:<20}{reserva.objeto_sala.nombre:<20}{reserva.turno:<10}")
    sep(90)

def titulo(nombre):
    print("\n" + "="*70)
    texto = nombre.center(66)
    print("**" + texto + "**")
    print("="*70) 

def titulo2(nombre):
    print("\n" + "="*90)
    texto = nombre.center(86)
    print("**" + texto + "**")
    print("="*90)

def sep(cantidad):
    print("-"*cantidad)

def convertir(entrada):
    if not entrada.isdigit():
        return
    return int(entrada)

# Función para dar de alta clientes y salas
def altas():
    nombres_iniciales = [["Marcos Israel", "Suárez Luna"],["Kevin Eduardo", "Hernández López"], ["Brando Javier", "Solís Salazar"], ["Victor Manuel", "López López"], ["Elian Jesús", "García Sánchez"]]
    for nombre, apellido in nombres_iniciales:
        nCliente = Cliente(nombre, apellido)
        clientes[nCliente.id_cliente] = nCliente
    print("\nClientes iniciales cargados correctamente.")
    salas_iniciales = [["Oficina A", 100], ["Oficina B", 50], ["Oficina C",150], ["Oficina D",20], ["Oficina E", 200]]
    for sala, cupo in salas_iniciales:
        nSala = Sala(sala,cupo)
        salas[nSala.id_sala] = nSala
    print("Salas iniciales cargadas correctamente.\n")

# Función opción 1
def agregar_reservacion():
    if not clientes:
        print("Aún no hay clientes agregados para hacer una reservación.")
        return
    
    elif not salas:
        print("Aún no hay salas agregadas para hacer una reservación.")
        return
    
    while True:
        obtener_clientes()
        clave = input("Ingrese la clave del cliente para la reservación (o C para cancelar): ").upper().strip()
        if clave == "C":
            print("Operación cancelada, volviendo al menú...")
            return
        
        clave = convertir(clave)
        
        if clave not in clientes:
            print("\nNo existe ese cliente, favor de elegir el correcto")
            continue

        cliente_elegido = clientes[clave]
        while True:
            fecha_reservacion = input("Ingrese la fecha de reservación (DD-MM-YYYY) (debe ser 2 días posteriores a hoy): ")

            try:
                fecha_procesada = dt.datetime.strptime(fecha_reservacion, "%d-%m-%Y").date()
            except ValueError:
                print("La fecha proporcionada no es válida, favor de usar el formato correcto (DD-MM-YYYY)\n")
                continue

            if not fecha_procesada > FECHA_MINIMA:
                print("Esa fecha no cumple con los requisitos (2 días posteriores a hoy)\n")
                continue

            while True:
                obtener_salas(fecha_procesada)
                sala_elegida = input("Ingrese la clave de la sala que desea usar (o C para cancelar): ").upper()

                if sala_elegida == "C":
                    print("Operación cancelada, volviendo al menú...")
                    return
                sala_elegida = convertir(sala_elegida)

                if not sala_elegida in salas:
                    print("Sala no encontrada, favor de elegir la correcta.")
                    continue

                sala = salas[sala_elegida]
                libres = filtro(sala, fecha_procesada)
                if not libres:
                    print("Esa sala no tiene turnos libres ese día. Elige otra sala.\n")
                    continue

                while True: 
                    turno_elegido = input("Ingrese el turno para el evento (M,V,N): ").upper()
                    if turno_elegido not in ("MVN"):
                        print("No existe ese turno, favor de elegir el correcto (M,V,N)\n")
                        continue

                    if turno_elegido == "M":
                        turno_elegido = "Matutino"
                    elif turno_elegido == "V":
                        turno_elegido = "Vespertino"
                    elif turno_elegido == "N":
                        turno_elegido = "Nocturno"

                    ocupados = obtener_turnos_ocupados(sala, fecha_procesada)
                    if turno_elegido in ocupados:
                        print(f"El turno {turno_elegido} esta ocupado en la sala {sala.nombre} con fecha: {fecha_procesada}")
                        continue

                    if turno_elegido == "Matutino":
                        agregar_reservacion_turno(cliente_elegido, sala, fecha_procesada, turno_elegido)
                        return
                    elif turno_elegido == "Vespertino":
                        agregar_reservacion_turno(cliente_elegido, sala, fecha_procesada, turno_elegido)
                        return
                    elif turno_elegido == "Nocturno":
                        agregar_reservacion_turno(cliente_elegido, sala, fecha_procesada, turno_elegido)
                        return
                            
# Función opción 2
def editar_nombre_reservacion():
    if not reservas:
        print("No existen reservaciones aún para editar.")
        return
    
    while True: 
        fecha_inicio = input("Ingrese la fecha de inicio para la busqueda (DD-MM-YYYY) (o C para cancelar): ")
        if fecha_inicio.upper() == "C":
            print("Operación cancelada, volviendo al menú...")
            return
        
        fecha_fin = input("Ingrese la fecha fin de la busqueda (DD-MM-YYYY) (o C para Cancelar): ")
        if fecha_fin.upper() == "C":
            print("Operación cancelada, volviendo al menú...")
            return
        
        try:
            fecha_inicio_procesada = dt.datetime.strptime(fecha_inicio, "%d-%m-%Y").date()
            fecha_fin_procesada = dt.datetime.strptime(fecha_fin, "%d-%m-%Y").date()
        except ValueError:
            print("Una de las fechas o las dos no cumple con los requisitos (DD-MM-YYYY)")
            continue

        if fecha_inicio_procesada > fecha_fin_procesada:
            print("La fecha Inicial no puede ser mayor a la fecha Final.")
            continue

        filtro_fechas = {}
        for folio, reserva in reservas.items():
            if fecha_inicio_procesada <= reserva.fecha and reserva.fecha <= fecha_fin_procesada:
                filtro_fechas[folio] = reserva

        if not filtro_fechas:
            print("No hay reservaciones en ese rango.")
            continue

        while True:
            mostrar_reservacion_fechas(fecha_inicio_procesada,fecha_fin_procesada,filtro_fechas)
            editar_clave = input("Ingrese el folio del evento para editar su nombre: (o C para cancelar): ")
            if editar_clave.upper() == "C":
                print("Operación cancelada, volviendo al menú...")
                return
            
            editar_clave = convertir(editar_clave)

            if editar_clave not in filtro_fechas:
                print("\nNo existe ese folio, favor de elegir el correcto.")
                continue

            editar = reservas[editar_clave]
            while True:
                editar_nombre = input("Ingrese el nuevo nombre: ").strip()
                if not editar_nombre:
                    print("El nombre no puede quedar vacío.")
                else:
                    editar.nombre_evento = editar_nombre
                    print("El nombre del evento ha sido cambiado exitosamente.")
                    return
                
# Función opción 3
def consultar_reservaciones():
    if not reservas:
        print("Aún no hay reservaciones para ninguna fecha")
        return
    while True:
        seleccion_fecha = input("\nIngrese la fecha para ver las reservaciones (DD-MM-YYYY) (o C para cancelar): ")
        if seleccion_fecha.upper() == "C":
            print("Operación cancelada, volviendo al menú...")
            return
        try:
            seleccion_fecha_procesada = dt.datetime.strptime(seleccion_fecha, "%d-%m-%Y").date()
        except ValueError:
            print("La fecha proporcionada no es válida, favor de usar el formato correcto (DD-MM-YYYY)")
            continue

        filtro_fechas = {}
        for folio, reserva in reservas.items():
            if reserva.fecha == seleccion_fecha_procesada:
                filtro_fechas[folio] = reserva

        if not filtro_fechas:
            print("No existe ninguna reservación para esa fecha.")
            continue
        
        titulo2(f"Reservaciones para el día {seleccion_fecha_procesada}")
        print(f"{'Folio':<8}{'Cliente':<19}{'Nombre del evento':<20}{'Sala':<20}{'Turno':<10}")
        sep(90)
        for folio,reserva in filtro_fechas.items():
            print(f"{folio:<8}{reserva.objeto_cliente.nombre:<19}{reserva.nombre_evento:<20}{reserva.objeto_sala.nombre:<20}{reserva.turno:<10}")
        sep(90)
        return

# Función opción 4
def agregar_cliente():
    while True:
        nombres = input("\nIngrese los nombres de el cliente (o C para cancelar): ").title().strip()
        if nombres == "C":
            print("Operación cancelada, volviendo al menú...")
            return
        
        apellidos = input("Proporciona los apellidos de la persona (o C para cancelar): ").title().strip()
        if apellidos == "C":
            print("Operación cancelada, volviendo al menú...")
            return
        
        if not nombres or  not apellidos:
            print("No puede quedar vacios nombre/apellidos")
        else:
            print("\n")
            nCliente = Cliente(nombres,apellidos)
            clientes[nCliente.id_cliente] = nCliente
            print("#"*70)
            print(f"Cliente agregado exitosamente con nombre: {nCliente.nombre} y Apellidos {nCliente.apellido}")
            print(f"Clave: {nCliente.id_cliente}")
            print("#"*70)
            return
        
# Función opción 5
def agregar_sala():
    while True:
        nombre_sala = input("\nIngrese el nombre de la Sala (o C para cancelar): ").title().strip()
        if nombre_sala == "C":
            print("Operación cancelada, volviendo al menú...")
            return
        
        if not nombre_sala:
            print("No puede quedar vacío el nombre de la sala.")
            continue

        try:
            cupo_sala = int(input("Ingrese el cupo de la Sala (mayor a 1): "))
        except ValueError:
            print("No se puede quedar vacío y tiene que ser un número entero")
            continue

        if cupo_sala <=1:
            print("El cupo de la sala debe ser mayor a 1")
        else: 
            print("\n")
            nSala = Sala(nombre_sala, cupo_sala)
            salas[nSala.id_sala] = nSala
            print("#"*70)
            print(f"Sala agregada exitosamente con nombre: {nSala.nombre} y un cupo de: {nSala.cupo}")
            print(f"Clave: {nSala.id_sala}")
            print("#"*70)
            return
        
# Función menú
def menu():
    try: 
        while True:
            titulo("MENü PRINCIPAL")
            print("1. Registrar la reservación de una sala.")
            print("2. Editar el nombre del evento de una reservación ya hecha.")
            print("3. Consultar las reservaciones existentes para una fecha específica. ")
            print("4. Registrar a un nuevo cliente")
            print("5. Registrar una sala")
            print("6. Salir")
            try: 
                respuesta = int(input("Ingresa la opcíón: "))
            except ValueError:
                print("Error: Escribir solo números del 1-6")
            else:
                if respuesta == 1:
                    agregar_reservacion()
                elif respuesta == 2:
                    editar_nombre_reservacion()
                elif respuesta == 3:
                    consultar_reservaciones()
                elif respuesta == 4:
                    agregar_cliente()
                elif respuesta == 5:
                    agregar_sala()
                elif respuesta == 6:
                    titulo("Programa terminado")
                    break
                else:
                    print("Fuera de rango, elegir solo entre 1-6")
    except KeyboardInterrupt:
        print("\nCierre forzado...")

def alta_reservacion():
    cliente = clientes[1]
    sala = salas[4]
    reservaciones_iniciales = [[cliente,sala,dt.date(2025,12,12),"Matutino","Evento 1"]]
    for cliente,sala,fecha,turno,nombre in reservaciones_iniciales:
        nuevo_evento = Reserva(cliente,sala,fecha,turno,nombre)
        reservas[nuevo_evento.folio] = nuevo_evento
    print("Reservación cargada: ")
    for folio, evento in reservas.items():
        print(f"Folio: {folio} | Cliente: {evento.objeto_cliente.nombre} | Sala: {evento.objeto_sala.nombre} | "
          f"Fecha: {evento.fecha} | Turno: {evento.turno} | Nombre: {evento.nombre_evento}")
        

if __name__ == "__main__":
    #altas()
    #alta_reservacion()
    menu()