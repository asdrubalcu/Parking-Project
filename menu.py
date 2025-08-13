# menu.py

import time
from administracion import AdministracionParqueo
from parqueo import Parqueo
from clientes import ClientesManager
from reservas import ReservasManager
from datetime import datetime

# Esta clase maneja los menús para la interacción por terminal con los usuarios
class Menu:

    @staticmethod
    def menu_parqueo():
        # Crea las instancias de configuración y managers para iniciar el sistema
        admin = AdministracionParqueo()
        clientes = ClientesManager()
        reservas = ReservasManager()

        # Paso los managers al parqueo para integrarlos
        parqueo = Parqueo(admin, clientes_manager=clientes, reservas_manager=reservas)

        while True:
            print("\n========== MENÚ PRINCIPAL ==========")
            print("1. Ingresar vehículo")
            print("2. Sacar vehículo")
            print("3. Ver espacios del parqueo")
            print("4. Ver cola de espera")
            print("5. Consultar vehículo por placa")
            print("6. Ver historial por placa")
            print("7. Administración del parqueo")
            print("8. Clientes")
            print("9. Reservas")
            print("10. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                placa = input("\nIngrese la placa: ").upper().strip()
                if placa == "":
                    print("Por favor digite una placa válida. Intente de nuevo.")
                    time.sleep(1)
                    continue

                # Validar si ya está dentro (uso directo del diccionario por eficiencia)
                if placa in parqueo.vehiculos_dentro:
                    print("\nEste vehículo ya está dentro del parqueo.")
                    time.sleep(1)
                    continue  # Volver al menú principal

                # Si no está, preguntar tipo
                print("\nIngrese el tipo de vehículo:\n1. Auto\n2. Moto\n")
                opc = input("Seleccione una opción: ")
                if opc == "1":
                    tipo = "auto"
                elif opc == "2":
                    tipo = "moto"
                else:
                    print("Opción no válida.")
                    time.sleep(1)
                    continue  # Volver al menú principal

                # Ingresar el vehículo
                parqueo.meter_vehiculo(placa, tipo)
                continue  # Volver al menú principal

            elif opcion == "2":
                placa = input("Ingrese la placa: ").upper().strip()
                if placa == "":
                    print("Por favor digite una placa válida.")
                    time.sleep(1)
                    continue
                parqueo.sacar_vehiculo(placa)
            elif opcion == "3":
                parqueo.mostrar_espacios()
            elif opcion == "4":
                parqueo.mostrar_cola()
            elif opcion == "5":
                placa = input("Ingrese la placa: ").upper().strip()
                if placa == "":
                    print("Por favor digite una placa válida.")
                    time.sleep(1)
                    continue
                parqueo.consultar_placa(placa)
            elif opcion == "6":
                placa = input("Ingrese la placa: ").upper().strip()
                if placa == "":
                    print("Por favor digite una placa válida.")
                    time.sleep(1)
                    continue
                parqueo.ver_historial_por_placa(placa)
            elif opcion == "7":
                Menu.menu_administracion(admin, parqueo)
            elif opcion == "8":
                Menu.menu_clientes(clientes)
            elif opcion == "9":
                Menu.menu_reservas(reservas, clientes, parqueo)
            elif opcion == "10":
                print("Saliendo del sistema...")
                time.sleep(1)
                break
            else:
                print("Opción no válida.")
                time.sleep(1)

    # Submenú administración (igual)
    @staticmethod
    def menu_administracion(admin, parqueo):
        while True:
            print("\n--- ADMINISTRACIÓN DEL PARQUEO ---")
            print("1. Ver configuración actual")
            print("2. Cambiar cantidad de espacios para autos")
            print("3. Cambiar cantidad de espacios para motos")
            print("4. Cambiar tarifa por tipo")
            print("5. Cambiar método de cobro")
            print("6. Volver al menú principal")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                admin.mostrar_configuracion()
            elif opcion == "2":
                try:
                    nuevo = int(input("Nueva cantidad de espacios para autos: "))
                    admin.cambiar_espacios_autos(nuevo)
                    parqueo.actualizar_espacios()
                except ValueError:
                    print("Valor inválido.")
            elif opcion == "3":
                try:
                    nuevo = int(input("Nueva cantidad de espacios para motos: "))
                    admin.cambiar_espacios_motos(nuevo)
                    parqueo.actualizar_espacios()
                except ValueError:
                    print("Valor inválido.")
            elif opcion == "4":
                tipo = input("\nTipo de vehículo (auto, moto): ").lower()
                try:
                    nueva_tarifa = int(input("Nueva tarifa por hora: "))
                    admin.cambiar_tarifa(tipo, nueva_tarifa)
                except ValueError:
                    print("Valor inválido.")
            elif opcion == "5":
                print("\n1. Cobro solo por horas completas")
                print("2. Cobro fraccionado (media hora después de la primera)")
                opc = input("Seleccione el método: ")
                admin.cambiar_cobro(opc == "2")
            elif opcion == "6":
                break
            else:
                print("Opción no válida.")

    # ---------------- Clientes ----------------
    @staticmethod
    def menu_clientes(clientes_mgr):
        while True:
            print("\n--- CLIENTES ---")
            print("1. Crear cliente")
            print("2. Consultar cliente por correo")
            print("3. Modificar cliente por correo")
            print("4. Eliminar cliente por correo")
            print("5. Volver")
            opc = input("Seleccione una opción: ")
            if opc == "1":
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                telefono = input("Teléfono: ")
                correo = input("Correo: ").lower().strip()
                cedula = input("Cédula: ").strip()
                ok, res = clientes_mgr.crear_cliente(nombre, apellido, telefono, correo, cedula)
                if not ok:
                    print("Error:", res)
                else:
                    print("Cliente creado:", res.nombre, res.apellido)
            elif opc == "2":
                correo = input("Correo: ").lower().strip()
                c = clientes_mgr.obtener_por_correo(correo)
                if not c:
                    print("Cliente no encontrado.")
                else:
                    print("Nombre:", c.nombre)
                    print("Apellido:", c.apellido)
                    print("Teléfono:", c.telefono)
                    print("Correo:", c.correo)
                    print("Cédula:", c.cedula)
            elif opc == "3":
                correo = input("Correo del cliente a modificar: ").lower().strip()
                c = clientes_mgr.obtener_por_correo(correo)
                if not c:
                    print("Cliente no encontrado.")
                    continue
                print("\n¿Qué desea modificar? (dejar vacío para no cambiar)")
                nombre = input("Nombre (" + c.nombre + "): ").strip() or None
                apellido = input("Apellido (" + c.apellido + "): ").strip() or None
                telefono = input("Teléfono (" + c.telefono + "): ").strip() or None
                cedula = input("Cédula (" + c.cedula + "): ").strip() or None
                ok, res = clientes_mgr.modificar_por_correo(correo, nombre=nombre, apellido=apellido, telefono=telefono, cedula=cedula)
                if not ok:
                    print("Error:", res)
                else:
                    print("Cliente modificado.")
            elif opc == "4":
                correo = input("Correo del cliente a eliminar: ").lower().strip()
                ok, res = clientes_mgr.eliminar_por_correo(correo)
                if not ok:
                    print("Error:", res)
                else:
                    print(res)
            elif opc == "5":
                break
            else:
                print("Opción no válida.")

    # ---------------- Reservas ----------------
    @staticmethod
    def menu_reservas(reservas_mgr, clientes_mgr, parqueo):
        while True:
            print("\n--- RESERVAS ---")
            print("1. Crear reserva")
            print("2. Consultar reservas activas por placa")
            print("3. Consultar reservas activas por usuario (correo)")
            print("4. Modificar reserva (por placa)")
            print("5. Eliminar reserva (por placa)")
            print("6. Volver")
            opc = input("Seleccione una opción: ")
            if opc == "1":
                correo = input("Correo del usuario: ").lower().strip()
                cliente = clientes_mgr.obtener_por_correo(correo)
                if not cliente:
                    print("El usuario no existe. Debe crearlo primero.")
                    crear = input("¿Desea crear el usuario ahora? (si/no): ").strip().lower()
                    if crear in ["si", "sí"]:
                        nombre = input("Nombre: ")
                        apellido = input("Apellido: ")
                        telefono = input("Teléfono: ")
                        cedula = input("Cédula: ")
                        ok, res = clientes_mgr.crear_cliente(nombre, apellido, telefono, correo, cedula)
                        if not ok:
                            print("Error creando usuario:", res)
                            continue
                        else:
                            print("Usuario creado.")
                    else:
                        continue

                placa = input("Placa a reservar: ").upper().strip()
                if placa == "":
                    print("Placa inválida.")
                    continue
                # validar que no haya reserva ni esté en parqueo
                if parqueo and placa in parqueo.vehiculos_dentro:
                    print("La placa ya está en el parqueo.")
                    continue
                tipo = input("Tipo (auto/moto): ").lower().strip()
                if tipo not in ["auto", "moto"]:
                    print("Tipo inválido.")
                    continue
                fecha_str = input("Fecha y hora ingreso (YYYY-MM-DD HH:MM): ")
                try:
                    fecha_ingreso = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
                except Exception as e:
                    print("Formato inválido.")
                    continue
                ok, res = reservas_mgr.crear_reserva(correo, placa, tipo, fecha_ingreso, parqueo)
                if not ok:
                    print("Error:", res)
                else:
                    print("Reserva creada para", placa, "en", fecha_ingreso)
            elif opc == "2":
                placa = input("Placa: ").upper().strip()
                r = reservas_mgr.buscar_activa_por_placa(placa)
                if not r:
                    print("No hay reserva activa para esa placa.")
                else:
                    print("Reserva -> Usuario:", r.usuario_correo, "Placa:", r.placa, "Fecha:", r.fecha_ingreso, "Estado:", r.estado)
            elif opc == "3":
                correo = input("Correo: ").lower().strip()
                lista = reservas_mgr.buscar_activas_por_usuario(correo)
                if not lista:
                    print("No hay reservas activas para ese usuario.")
                else:
                    for r in lista:
                        print("Placa:", r.placa, "Fecha:", r.fecha_ingreso, "Estado:", r.estado)
            elif opc == "4":
                placa = input("Placa de la reserva a modificar: ").upper().strip()
                r = reservas_mgr.buscar_activa_por_placa(placa)
                if not r:
                    print("No existe reserva activa para esa placa.")
                    continue
                fecha_str = input("Nueva fecha y hora ingreso (YYYY-MM-DD HH:MM): ")
                try:
                    nueva_fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
                except:
                    print("Formato inválido.")
                    continue
                ok, res = reservas_mgr.modificar_fecha_por_placa(placa, nueva_fecha)
                if not ok:
                    print("Error:", res)
                else:
                    print("Reserva modificada.")
            elif opc == "5":
                placa = input("Placa de la reserva a eliminar: ").upper().strip()
                ok, res = reservas_mgr.eliminar_por_placa(placa)
                if not ok:
                    print("Error:", res)
                else:
                    print(res)
            elif opc == "6":
                break
            else:
                print("Opción no válida.")