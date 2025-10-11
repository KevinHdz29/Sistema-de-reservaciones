import datetime as dt
import sys
import json
import csv
import openpyxl
from openpyxl.styles import Font,Alignment,Border,Side

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


def obtener_clientes():
    titulo("Clientes registrados")
    print(f"{'Clave':<8} {'Apellidos':<20} {'Nombres':<15}")
    sep(70)                                                 
    for clave, cliente in sorted(clientes.items(), key=lambda kv: (kv[1].apellido, kv[1].nombre)):
        print(f"{clave:<8} {cliente.apellido:<20} {cliente.nombre:<15}")
    sep(70)

def obtener_salas(fecha):
    titulo2(f"Salas disponibles para {formato(fecha)}")
    print(f"{'Clave':<8} {'Sala':<20} {'Cupo':<15} {'Turno disponible':<20}")
    sep(90)
    for clave, sala in salas.items():
        libres = filtro(sala, fecha)
        if not libres:
            print(f"{clave:<8} {sala.nombre:<20} {'':<15} {'SALA OCUPADA':<20}")
            continue
        print(f"{clave:<8} {sala.nombre:<20} {sala.cupo:<15} {' | '.join(libres):<20}")
    sep(90)

def filtro(sala, fecha):
    ocupados = obtener_turnos_ocupados(sala, fecha)
    libres = [turno for turno in TURNOS if turno not in ocupados]
    return libres

def obtener_turnos_ocupados(sala, fecha):
    turnos_ocupados = []
    for reserva in reservas.values():
        if reserva.objeto_sala.id_sala == sala.id_sala and reserva.fecha == fecha:
            turnos_ocupados.append(reserva.turno)
    return turnos_ocupados

def agregar_reservacion_turno(cliente, sala, fecha, turno_elegido):
    nombre_evento = entrada("Ingrese el nombre del evento")
    if nombre_evento is None:
        return
    nuevo_evento = Reserva(cliente, sala, fecha, turno_elegido, nombre_evento)
    reservas[nuevo_evento.folio] = nuevo_evento
    mostrar_reserva(nuevo_evento, cliente, sala, fecha, nombre_evento)
    return
    
def mostrar_reserva(nuevo_evento, cliente, sala, fecha, nombre_evento):
    titulo("Reservación registrada exitosamente")
    print(f"Folio:   {nuevo_evento.folio}")
    print(f"Cliente: {cliente.getNombres()}")
    print(f"Sala:    {sala.nombre} | Cupo: {sala.cupo}")
    print(f"Fecha:   {formato(fecha)}")
    print(f"Evento:  {nombre_evento}")
    print(f"Turno:   {nuevo_evento.turno}")

def mostrar_reservacion_fechas(fecha_inicio, fecha_fin, filtro_fechas):
    titulo2(f"Reservaciones para {formato(fecha_inicio)} - {formato(fecha_fin)}")
    print(f"{'Folio':<8}{'Cliente':<19}{'Fecha':<15}{'Nombre del evento':<20}{'Sala':<20}{'Turno':<10}")
    sep(90)
    for folio,reserva in filtro_fechas.items():
        print(f"{folio:<8}{reserva.objeto_cliente.getNombres():<19}{formato(reserva.fecha):<15}{reserva.nombre_evento:<20}{reserva.objeto_sala.nombre:<20}{reserva.turno:<10}")
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

def sep2(cantidad):
    print("#"*cantidad)

def salto():
    print("\n")

def formato(fecha):
    return dt.datetime.strftime(fecha,"%d-%m-%Y")

def entrada(texto, c="C", tipo=str):
    while True:
        valor = input(f"{texto} o {c} para cancelar: ").strip().title()
        if valor == c:
            print("Operación cancelada... Volviendo al menú.\n")
            return None
        if not valor:
            print("No puede quedar vacío.\n")
            continue
        if tipo is str:
            if valor.isdigit():
                print("No se permite escribir solo números.\n")
                continue
            return valor
        elif tipo is int:
            if not valor.isdigit():
                print("Debe ingresar un número entero.\n")
                valor = -1
            return int(valor)
        elif tipo is dt.date:
            try:
                return dt.datetime.strptime(valor, "%d-%m-%Y").date()
            except ValueError:
                print("La fecha proporcionada no es válida, favor de usar el formato correcto (DD-MM-YYYY)\n")
                continue


def agregar_reservacion():
    if not clientes and not salas:
        print("Aún no hay clientes ni salas agregados para hacer una reservación.")
        return
    if not clientes:
        print("Aún no hay clientes para hacer una reservación")
        return
    if not salas:
        print("Aún no hay salas para hacer una reservación")
        return
    
    while True:
        obtener_clientes()
        clave = entrada("Ingrese la clave del cliente para la reservación", tipo=int)
        if clave is None:
            return

        if clave not in clientes:
            print("\nNo existe ese cliente, favor de elegir el correcto")
            continue

        cliente_elegido = clientes[clave]
        break
    while True:
        fecha_reservacion = entrada("Ingrese la fecha de reservación (DD-MM-YYYY) (debe ser al menos 2 días posterior a hoy)", tipo=dt.date)
        if fecha_reservacion is None:
            return

        if fecha_reservacion < FECHA_MINIMA:
            print("Esa fecha no cumple con los requisitos (2 días posteriores a hoy) \n ")
            continue
        break
    while True:
        obtener_salas(fecha_reservacion)
        sala_elegida = entrada("Ingrese la clave de la sala que desea usar", tipo=int)
        if sala_elegida is None:
            return
        if sala_elegida not in salas:
            print("\nSala no encontrada, favor de elegir la correcta.")
            continue

        sala = salas[sala_elegida]
        libres = filtro(sala, fecha_reservacion)
        if not libres:
            print("Esa sala no tiene turnos libres ese día. Elige otra sala.")
            continue
        break 
    while True: 
        turno_elegido = entrada("Ingrese el turno para el evento (M,V,N)")
        if turno_elegido is None:
            return
        if turno_elegido not in ("M", "V", "N", "Matutino", "Vespertino", "Nocturno"):
            print("No existe ese turno, favor de elegir el correcto (M,V,N)\n")
            continue

        if turno_elegido == "M":
            turno_elegido = "Matutino"
        if turno_elegido == "V":
            turno_elegido = "Vespertino"
        if turno_elegido == "N":
            turno_elegido = "Nocturno"

        ocupados = obtener_turnos_ocupados(sala, fecha_reservacion)
        if turno_elegido in ocupados:
            print(f"El turno {turno_elegido} está ocupado en la sala {sala.nombre} con fecha: {formato(fecha_reservacion)}")
            continue

        agregar_reservacion_turno(cliente_elegido, sala, fecha_reservacion, turno_elegido)
        return        


def editar_nombre_reservacion():
    if not reservas:
        print("No existen reservaciones aún para editar.")
        return
    while True:
        fecha_inicio = entrada("Ingrese la fecha de inicio para la búsqueda (DD-MM-YYYY)", tipo=dt.date)
        if fecha_inicio is None:
            return
        fecha_fin = entrada("Ingrese la fecha fin de la búsqueda (DD-MM-YYYY)", tipo=dt.date)
        if fecha_fin is None:
            return
        if fecha_inicio > fecha_fin:
            print("La fecha inicial no puede ser mayor a la fecha final.")
            continue
        break
    filtro_fechas = {folio:reserva for folio,reserva in reservas.items() if fecha_inicio <= reserva.fecha and fecha_fin >= reserva.fecha}
    if not filtro_fechas:
        print("\nNo hay reservaciones en ese rango. Volviendo al menú...")
        return
    while True:
        mostrar_reservacion_fechas(fecha_inicio,fecha_fin,filtro_fechas)
        editar = entrada("Ingrese el folio del evento para editar su nombre", tipo=int)
        if editar is None:
            return
        if editar not in filtro_fechas:
            print("No existe ese folio, favor de elegir el correcto")
            continue
        reserva_editar = reservas[editar]
        break
    while True:
        editar_nombre = entrada("Ingrese el nuevo nombre")
        if editar_nombre is None:
            return
        reserva_editar.nombre_evento = editar_nombre
        print("El nombre del evento ha sido cambiado exitosamente.")
        return


def consultar_reservaciones():
    if not reservas:
        print("Aún no hay reservaciones para ninguna fecha")
        return
    while True:
        seleccion_fecha = entrada("Ingrese la fecha para ver las reservaciones (DD-MM-YYYY)", tipo=dt.date)
        if seleccion_fecha is None:
            return
        filtro_fechas = [reserva for reserva in reservas.values() if reserva.fecha == seleccion_fecha]
        if not filtro_fechas:
            print("No existe ninguna reservación para esa fecha\n")
            continue
        titulo2(f"Reservaciones para el día {formato(seleccion_fecha)}")
        print(f"{'Folio':<8}{'Cliente':<19}{'Nombre del evento':<20}{'Sala':<20}{'Turno':<10}")
        sep(90)
        for reserva in filtro_fechas:
            print(f"{reserva.folio:<8}{reserva.objeto_cliente.getNombres():<19}{reserva.nombre_evento:<20}{reserva.objeto_sala.nombre:<20}{reserva.turno:<10}")
        sep(90)
        
        while True:
            exportar = entrada("¿Desea exportar el reporte? (S/N)")
            if exportar is None:
                return
            if exportar not in ("SN"):
                print("No existe esa opción, favor de elegir la correcta (S/N)\n")
                continue
            if exportar == "N":
                print("Volviendo a buscar...\n")
                break
            while True:
                titulo("Exportación de reporte")
                print("1. JSON")
                print("2. CSV")
                print("3. EXCEL")
                opcion = entrada("¿En qué tipo de archivo desea guardar el reporte?", tipo=int)
                if opcion is None:
                    return
                if opcion == 1:
                    exportar_json(filtro_fechas,seleccion_fecha)
                    titulo("Reporte JSON generado exitosamente")
                    return
                if opcion == 2:
                    exportar_csv(filtro_fechas,seleccion_fecha)
                    titulo("Reporte CSV generado exitosamente")
                    return
                if opcion == 3:
                    exportar_excel(filtro_fechas,seleccion_fecha)
                    return
                else:
                    print("\nNo válido, elija entre 1-3.")
                    continue


def agregar_cliente():
    nombres = entrada("Ingrese el nombre del cliente")
    if nombres is None:
        return
    apellidos = entrada("Ingrese el apellido del cliente")
    if apellidos is None:
        return
    nCliente = Cliente(nombres,apellidos)
    clientes[nCliente.id_cliente] = nCliente
    titulo("Cliente agregado exitosamente")
    print(f"Nombre: {nCliente.nombre} Apellido: {nCliente.apellido}")
    print(f"Clave: {nCliente.id_cliente}")
    sep(70)
    salto()
    return
        

def agregar_sala():
    nombre_sala = entrada("Ingrese el nombre de la sala")
    if nombre_sala is None:
        return
    while True:
        cupo_sala = entrada("Ingrese el cupo de la sala (mayor que 1)", tipo=int)
        if cupo_sala is None:
            return 
        if cupo_sala <2:
            print("La sala debe ser mayor que 1")
            continue
        nSala = Sala(nombre_sala, cupo_sala)
        salas[nSala.id_sala] = nSala
        titulo("Sala agregada exitosamente")
        print(f"Nombre de la Sala:  {nSala.nombre} Cupo: {nSala.cupo}")
        print(f"Clave: {nSala.id_sala}")
        sep(70)
        salto()
        return
        

def salir():
    while True:
        fin = input("¿Desea salir del programa? (S/N): ").title().strip()
        if fin not in ("S","N") or not fin:
            print("No es válido, favor de usar (S/N)\n")
            continue
        if fin == "N":
            print("Regresando al menú...\n")
            return
        if fin == "S":
            guardar()
            titulo("Programa terminado...")
            sys.exit()


def menu():
    try: 
        while True:
            titulo("MENÚ PRINCIPAL")
            print("1. Registrar la reservación de una sala.")
            print("2. Editar el nombre del evento de una reservación ya hecha.")
            print("3. Consultar las reservaciones existentes para una fecha específica. ")
            print("4. Registrar a un nuevo cliente")
            print("5. Registrar una sala")
            print("6. Salir")
            try: 
                respuesta = int(input("Ingrese la opción: "))
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
                    salir()
                else:
                    print("Fuera de rango, elegir solo entre 1-6")
    except KeyboardInterrupt:
        titulo("Cierre forzado...")


def cargar():
    try:
        with open("datos.json", "r") as archivo:
            datos = json.load(archivo) 
    except FileNotFoundError:
        print("\nNo hay archivo existente. Se procederá a trabajar en un archivo nuevo.")
    else:
        for cliente in datos["clientes"].values():
            nCliente = Cliente(cliente["nombre"], cliente["apellido"])
            nCliente.id_cliente = cliente["id_cliente"]
            clientes[nCliente.id_cliente] = nCliente

        for sala in datos["salas"].values():
            nSala = Sala(sala["nombre"], sala["cupo"])
            nSala.id_sala = sala["id_sala"]
            salas[nSala.id_sala] = nSala

        for reserva in datos["reservas"].values():
            cliente_id = reserva["objeto_cliente"]["id_cliente"]
            sala_id = reserva["objeto_sala"]["id_sala"]
            objeto_cliente = clientes[cliente_id]
            objeto_sala = salas[sala_id]
            fecha = dt.datetime.strptime(reserva["fecha"], "%d-%m-%Y").date()
            turno = reserva["turno"]
            nombre_evento = reserva["nombre_evento"]
            nReserva = Reserva(objeto_cliente, objeto_sala, fecha, turno, nombre_evento)
            nReserva.folio = reserva["folio"]
            reservas[nReserva.folio] = nReserva


def guardar():
    clientes_json = {}
    for clave,cliente in clientes.items():
        clientes_json[clave]={
            "id_cliente":cliente.id_cliente,
            "nombre":cliente.nombre,
            "apellido":cliente.apellido}
        
    salas_json = {}
    for clave,sala in salas.items():
        salas_json[clave] = {
            "id_sala":sala.id_sala,
            "nombre":sala.nombre,
            "cupo":sala.cupo}
        
    reservas_json = {}
    for folio, reserva in reservas.items():
        reservas_json[folio]={
            "folio":reserva.folio, 
            "objeto_cliente":{
                "id_cliente":reserva.objeto_cliente.id_cliente,
                "nombre":reserva.objeto_cliente.nombre,
                "apellido": reserva.objeto_cliente.apellido},
            "objeto_sala": {
                "id_sala": reserva.objeto_sala.id_sala,
                "nombre": reserva.objeto_sala.nombre,
                "cupo": reserva.objeto_sala.cupo},
            "fecha": reserva.fecha.strftime("%d-%m-%Y"),
            "turno": reserva.turno,
            "nombre_evento": reserva.nombre_evento}
    datos = {}
    datos["clientes"] = clientes_json
    datos["salas"] = salas_json
    datos["reservas"] = reservas_json
    with open("datos.json", "w") as archivo:
        json.dump(datos, archivo, indent=4)


def exportar_json(filtro_fechas,fecha):
    datos = []
    for reserva in filtro_fechas:
        datos.append({"folio": reserva.folio,
                      "cliente": reserva.objeto_cliente.getNombres(),
                      "sala": reserva.objeto_sala.nombre,
                      "cupo_sala": reserva.objeto_sala.cupo,
                      "fecha": reserva.fecha.strftime("%d-%m-%Y"),
                      "evento": reserva.nombre_evento,
                      "turno": reserva.turno})
    with open(f"Reporte-{formato(fecha)}.json", "w") as archivo:
        json.dump(datos, archivo, indent=2)



def exportar_csv(filtro_fechas,fecha):
    with open(f"Reporte-{formato(fecha)}.csv", "w", encoding="latin1", newline="") as archivo:
        grabador = csv.writer(archivo, delimiter="\t")
        grabador.writerow(("Folio", "Nombre_Cliente", "Sala", "Cupo_Sala", "Fecha", "Evento", "Turno"))
        for reserva in filtro_fechas:
            grabador.writerow([reserva.folio,
                               reserva.objeto_cliente.getNombres(),
                               reserva.objeto_sala.nombre,
                               reserva.objeto_sala.cupo,
                               reserva.fecha.strftime("%d-%m-%Y"),
                               reserva.nombre_evento,
                               reserva.turno])
        
        
def exportar_excel(filtro_fechas,fecha):
    libro = openpyxl.Workbook()
    hoja = libro["Sheet"]
    hoja.title = "Reservaciones"

    negritas = Font(bold=True)
    centrado = Alignment(horizontal="center", vertical="center")
    borde_grueso = Border(bottom=Side(border_style="thick", color="00078C"))
    

    celdaA1 = hoja["A1"]
    celdaA1.value = "Reporte de Reservaciones"
    celdaA1.font = Font(bold=True, size=16)
    celdaA1.alignment = centrado

    for columna in range(1,8):
        celda = hoja.cell(row=1, column=columna)
        celda.border = borde_grueso

    encabezados = {1:"Folio", 2:"Cliente", 3:"Sala", 4:"Cupo", 5:"Fecha", 6:"Evento", 7:"Turno"}
    for columna,texto in encabezados.items(): 
        celdaA2 = hoja.cell(row=2, column=columna, value=texto) 
        celdaA2.alignment = centrado
        celdaA2.font = negritas
        celdaA2.border = borde_grueso

    for fila,reserva in enumerate(filtro_fechas, start=3):
        hoja.cell(row=fila, column=1, value=reserva.folio).alignment = centrado
        hoja.cell(row=fila, column=2, value=reserva.objeto_cliente.getNombres()).alignment = centrado
        hoja.cell(row=fila, column=3, value=reserva.objeto_sala.nombre).alignment = centrado
        hoja.cell(row=fila, column=4, value=reserva.objeto_sala.cupo).alignment = centrado
        hoja.cell(row=fila, column=5, value=reserva.fecha.strftime("%d-%m-%Y")).alignment = centrado
        hoja.cell(row=fila, column=6, value=reserva.nombre_evento).alignment = centrado
        hoja.cell(row=fila, column=7, value=reserva.turno).alignment = centrado
    
    for columna in hoja.columns:
        letra = columna[0].column_letter 
        longitudes = []
        for celda in columna:
            if celda.row == 1:
                continue
            longitudes.append(len(str(celda.value)))
        hoja.column_dimensions[letra].width = max(longitudes) + 2

    hoja.merge_cells("A1:G1")

    try:
        libro.save(f"Reporte-{formato(fecha)}.xlsx")
    except PermissionError:
        print("\nEl archivo está abierto, no se puede sobrescribir.")
    else:
        titulo("Reporte EXCEL generado exitosamente.")


if __name__ == "__main__":
    cargar()
    menu()