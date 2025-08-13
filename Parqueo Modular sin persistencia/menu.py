# menu.py

import time
from administracion import AdministracionParqueo
from parqueo import Parqueo


# Menús para la interacción por terminal con los usuarios
class Menu:

    @staticmethod
    def menu_parqueo():
        # Creo las instancias de configuración y parqueo para iniciar el sistema
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
                else:
                    # Se valida si la placa ya está en en el parqueo
                    if placa in parqueo.vehiculos_dentro:
                        print("\nEste vehículo ya está dentro del parqueo.")
                        time.sleep(1)
                        continue  # Volver al menú principal            
                        
                    # Si no está, pregunta por tipo
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
                    # Si tipo es válido, Ingresa el vehículo
                    parqueo.meter_vehiculo(placa, tipo)
                    continue  # Volver al menú principal

            elif opcion == "2":
                placa = input("Ingrese la placa: ").upper().strip()
                parqueo.sacar_vehiculo(placa)# Método salida de vehículo de parqueo
            elif opcion == "3":
                parqueo.mostrar_espacios()# Método para mostrar todos los espacios del parqueo matriz
            elif opcion == "4":
                parqueo.mostrar_cola()# Método para mostrar solo cola de espera
            elif opcion == "5":
                placa = input("Ingrese la placa: ").upper().strip() # Método consulta o búsqueda por placa
                parqueo.consultar_placa(placa)
            elif opcion == "6":
                placa = input("Ingrese la placa: ").upper().strip()# Método Historial movimientos por placa
                parqueo.ver_historial_por_placa(placa)
            elif opcion == "7":
                Menu.menu_administracion(admin, parqueo) # Método para configuración de valores parqueo
            elif opcion == "8":
                print("Saliendo del sistema...")
                time.sleep(2)
                break
            else:
                print("Opción no válida.")

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
                admin.mostrar_configuracion()# Método que muestra configuración
            elif opcion == "2":
                nuevo = int(input("Nueva cantidad de espacios para autos: "))
                admin.cambiar_espacios_autos(nuevo)# Método modificar cantidad espacios para autos
                parqueo.actualizar_espacios()# Método para refrescar valores de espacio para la lógica de asignación
            elif opcion == "3":
                nuevo = int(input("Nueva cantidad de espacios para motos: "))
                admin.cambiar_espacios_motos(nuevo)# Método modificar cantidad espacios para motos
                parqueo.actualizar_espacios()# Método para refrescar valores de espacio para la lógica de asignación
            elif opcion == "4":
                tipo = input("\nTipo de vehículo (auto, moto): ").lower()
                nueva_tarifa = int(input("Nueva tarifa por hora: "))
                admin.cambiar_tarifa(tipo, nueva_tarifa)
            elif opcion == "5":
                print("\n1. Cobro solo por horas completas")
                print("2. Cobro fraccionado (media hora después de la primera)")
                opc = input("Seleccione el método: ")
                admin.cambiar_cobro(opc == "2")# Método para cambiar el modo de cobro del parqueo.
            elif opcion == "6":
                break
            else:
                print("Opción no válida.")
