# menu.py

import time
from administracion import AdministracionParqueo
from parqueo import Parqueo


# Esta clase maneja los menús para la interacción con los usuarios
class Menu:

    @staticmethod
    def menu_parqueo():
        # Crea las instancias de configuración y parqueo para iniciar el sistema
        admin = AdministracionParqueo()
        parqueo = Parqueo(admin)

        while True:
            print("\n========== MENÚ PRINCIPAL ==========")
            print("1. Ingresar vehículo")
            print("2. Sacar vehículo")
            print("3. Ver espacios del parqueo")
            print("4. Ver cola de espera")
            print("5. Consultar vehículo por placa")
            print("6. Ver historial por placa")
            print("7. Administración del parqueo")
            print("8. Salir")
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

                # Si ya conozco la placa, omito preguntar el tipo y uso los atributos recordados
                if placa in parqueo.placas_conocidas:
                    datos = parqueo.placas_conocidas[placa]
                    tipo = datos.get("tipo")
                    print("\nHe reconocido la placa y usaré los datos guardados: tipo " + tipo + ".")
                    time.sleep(1)
                    marca = datos.get("marca")
                    modelo = datos.get("modelo")
                    año = datos.get("año")
                    color = datos.get("color")
                else:
                    # Si no está, preguntar tipo y atributos
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

                    # Pregunto los nuevos atributos
                    marca = input("Ingrese la marca del vehículo: ").strip() or None
                    modelo = input("Ingrese el modelo del vehículo: ").strip() or None
                    año_input = input("Ingrese el año del vehículo: ").strip()
                    try:
                        año = int(año_input) if año_input != "" else None
                    except ValueError:
                        año = None
                    color = input("Ingrese el color del vehículo: ").strip() or None

                # Ingresar el vehículo con todos los atributos
                parqueo.meter_vehiculo(placa, tipo, marca, modelo, año, color)
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
                print("Saliendo del sistema...")
                time.sleep(1)
                break
            else:
                print("Opción no válida.")
                time.sleep(1)

    @staticmethod
    def menu_administracion(admin, parqueo):
        # Muestra el submenú para modificar la configuración del parqueo
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
                print("\n1. Auto")
                print("2. Moto")
                print("0. Salir")
                opc = input("Seleccione el método: ") or "1"
                if opc == "1":
                    tipo = "auto"
                elif opc == "2":
                    tipo = "moto"
                elif opc == "0":
                    return
                else:
                    print("Esta opción no es válida.")
                    return    
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
