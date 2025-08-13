# parqueo.py

from datetime import datetime
import time

# Importo los módulos con responsabilidades específicas
from impresion import Impresion
from vehiculo import Vehiculo
from registro import RegistroDeSalida
from espacios import EspaciosParqueo
from valet import Valet
from cola import ColaEspera
from cobro import Cobro
from historial import Historial

# Clase que maneja el parqueo, usa la configuración de la administración
class Parqueo:
    def __init__(self, configuracion):
        # Guarda la configuración del parqueo
        self.configuracion = configuracion

        # Instancias con responsabilidades separadas para mejor organización
        self.espacios = EspaciosParqueo(configuracion)
        self.valet = Valet()
        self.cola = ColaEspera()
        self.historial = Historial()

        # Diccionario de vehículos dentro: placa -> Vehiculo
        self.vehiculos_dentro = {}

    # Método para actualizar espacios
    def actualizar_espacios(self):
        self.espacios.actualizar_espacios()

    # Función para asignar espacio libre delegando a EspaciosParqueo
    def asignar_espacio_libre(self, tipo, placa):
        return self.espacios.asignar_espacio_libre(tipo, placa)

    # Función para liberar espacio delegando a EspaciosParqueo
    def liberar_espacio(self, placa, tipo): 
        # Primero intenta liberar en espacios fijos
        clave = self.espacios.liberar_espacio(placa, tipo)
        if clave is not None:
            return clave

        # Si no estaba en espacios fijos, intentar liberar en valet
        for clave_v, placa_v in self.valet.espacios_valet.items():
            if placa_v == placa:
                self.valet.espacios_valet[clave_v] = None
                self.valet.remover_por_placa(placa)

                # Si se libera espacio p1 o p2, llamar a mover_espera_a_valet para preguntar a cola
                if clave_v == 'p001' or clave_v == 'p002':
                    self.mover_espera_a_valet()

                return clave_v
        return None

    # Agregar a cola de espera delegando a ColaEspera
    def agregar_cola_espera(self, vehiculo):
        return self.cola.agregar_cola_espera(vehiculo)

    # Sacar primer vehículo de la cola delegando a ColaEspera
    def sacar_vehiculo_cola(self):
        return self.cola.sacar_vehiculo_cola()

    # Agregar a valet delegando a Valet
    def agregar_valet(self, vehiculo):
        return self.valet.agregar_valet(vehiculo)

    # Sacar vehículo del valet delegando a Valet (LIFO)
    def sacar_vehiculo_valet(self):
        return self.valet.sacar_vehiculo_valet()

    # Mostrar espacios delegando a EspaciosParqueo, Valet y Espera
    def mostrar_espacios_detallados(self):
        self.espacios.mostrar_espacios_detallados()
        self.valet.mostrar_valet()
        self.cola.mostrar_cola_espera()
        
    # Función para ingresar vehículo
    def meter_vehiculo(self, placa, tipo):
        # Verifica si el vehículo ya está dentro
        if placa in self.vehiculos_dentro:
            print("\nEste vehículo ya está dentro del parqueo.")
            time.sleep(1)
            return
        
        # Verifica si el tipo de vehículo es válido para este parqueo
        if tipo not in self.configuracion.tipos_vehiculo:
            print("\nEste tipo de vehículo no es aceptado.")
            time.sleep(1)
            return

        # Verifica si el vehículo ya está en la cola de espera
        for vehiculo in self.cola.cola_espera_autos:
            if vehiculo.placa == placa:
                print("\nEste vehículo ya está en la cola de espera.")
                time.sleep(1)
                return

        # Verifica si el vehículo ya está en valet
        for vehiculo in self.valet.valet_autos:
            if vehiculo.placa == placa:
                print("\nEste vehículo ya está en valet.")
                time.sleep(1)
                return

        # Crea una instancia del vehículo con placa y tipo
        vehiculo = Vehiculo(placa, tipo)

        if tipo == "moto":
            # Intenta asignar espacio para moto
            espacio = self.espacios.asignar_espacio_libre("moto", placa)
            if espacio is None:
                print("\nEl parqueo para motos está lleno. No hay cola de espera para motos.")
                time.sleep(1)
                return
            else:
                self.vehiculos_dentro[placa] = vehiculo
                Impresion.tiquet_ingreso(placa, tipo, vehiculo.hora_entrada, espacio)
                return

        if tipo == "auto":
            # Intenta asignar espacio para auto
            espacio = self.espacios.asignar_espacio_libre("auto", placa)
            if espacio is None:
                # No hay espacio para autos, revisa valet y cola de espera
                espacio_valet_disponible = None
                for clave, valor in self.valet.espacios_valet.items():
                    if valor is None:
                        espacio_valet_disponible = clave
                        break

                espacio_cola_disponible = None
                for clave, valor in self.cola.espacios_cola.items():
                    if valor is None:
                        espacio_cola_disponible = clave
                        break

                if espacio_valet_disponible is None and espacio_cola_disponible is None:
                    # No hay espacios en valet ni en cola
                    print("\nParqueo lleno, valet lleno y cola de espera llena. Intente más tarde.")
                    time.sleep(1)
                    return

                # Presenta opciones según disponibilidad
                print("\nEl parqueo está lleno.")
                opciones = []
                if espacio_valet_disponible is not None:
                    opciones.append("valet")
                if espacio_cola_disponible is not None:
                    opciones.append("espera")

                print("Opciones disponibles:")
                for i, opcion in enumerate(opciones, 1):
                    print(str(i) + ". Estacionar en " + opcion)

                # Pide la elección al usuario hasta que sea válida
                while True:
                    eleccion = input("Elija una opción (número): ").strip()
                    if eleccion.isdigit():
                        numero = int(eleccion)
                        if 1 <= numero <= len(opciones):
                            break
                    print("Opción inválida. Intente nuevamente.")

                seleccion = opciones[numero - 1]

                # Ejecuta la acción según selección
                if seleccion == "valet":
                    espacio_asignado = self.valet.agregar_valet(vehiculo)
                    print("\nVehículo agregado a valet en espacio " + espacio_asignado)
                    Impresion.tiquet_ingreso(placa, tipo, vehiculo.hora_entrada, espacio_asignado, "(Deja llaves)")
                    return

                if seleccion == "espera":
                    espacio_asignado = self.cola.agregar_cola_espera(vehiculo)
                    print("\nVehículo agregado a cola de espera en espacio " + espacio_asignado)
                    time.sleep(1)
                    return

            else:
                # Si hay espacio libre en parqueo normal
                self.vehiculos_dentro[placa] = vehiculo
                Impresion.tiquet_ingreso(placa, tipo, vehiculo.hora_entrada, espacio)
                return
    
    
    # Función para sacar vehículo (mantiene la lógica original, delegando a módulos)
    def sacar_vehiculo(self, placa):
        # Si está en parqueo normal
        if placa in self.vehiculos_dentro:
            vehiculo = self.vehiculos_dentro[placa]
            if vehiculo.tipo == "auto":
                ultimo = "a" + str(self.configuracion.cantidad_espacios_autos).zfill(3)
                penultimo = "a" + str(self.configuracion.cantidad_espacios_autos - 1).zfill(3)
                espacio_vehiculo = None
                for clave, valor in self.espacios.espacios_autos.items():
                    if valor == placa:
                        espacio_vehiculo = clave
                        break
                if espacio_vehiculo in [ultimo, penultimo]:
                    # Sacar p2 y p1 si existen
                    if self.valet.espacios_valet["p002"] is not None:
                        placa_p2 = self.valet.espacios_valet["p002"]
                        print("\n---------------------------------------------------------")
                        print("\nMoviendo vehículo placa", placa_p2, "de posición P2 a la calle")
                        print("---------------------------------------------------------")
                        time.sleep(1)
                        veh_p2 = self.valet.remover_por_placa(placa_p2)
                        self.valet.espacios_valet["p002"] = None
                    else:
                        veh_p2 = None

                    if self.valet.espacios_valet["p001"] is not None:
                        placa_p1 = self.valet.espacios_valet["p001"]
                        print("\n---------------------------------------------------------")
                        print("Moviendo vehículo placa", placa_p1, "de posición P1 a la calle")
                        print("---------------------------------------------------------")
                        time.sleep(1)
                        veh_p1 = self.valet.remover_por_placa(placa_p1)
                        self.valet.espacios_valet["p001"] = None
                    else:
                        veh_p1 = None

                    # Remover vehículo del parqueo y liberar espacio
                    self.vehiculos_dentro.pop(placa)
                    self.espacios.espacios_autos[espacio_vehiculo] = None

                    hora_salida = datetime.now()
                    total, horas_cobradas = Cobro.calcular(vehiculo.hora_entrada, hora_salida, vehiculo.tipo, self.configuracion)

                    # Delego tiquet salida a Impresion
                    Impresion.tiquet_salida(vehiculo.placa, vehiculo.tipo,
                                           vehiculo.hora_entrada, hora_salida,
                                           horas_cobradas, total)

                    # Mover veh_cola a espacio liberado por A
                    if self.cola.cola_espera_autos:
                        veh_cola = self.cola.sacar_vehiculo_cola()
                        print("\n---------------------------------------------------------")
                        print("\nVehículo con placa " + veh_cola.placa + " ingresó de espera a posición " + clave.upper())
                        print("---------------------------------------------------------")
                        time.sleep(1)
                        self.espacios.espacios_autos[espacio_vehiculo] = veh_cola.placa
                        self.vehiculos_dentro[veh_cola.placa] = veh_cola
                        Impresion.tiquet_ingreso(veh_cola.placa, veh_cola.tipo,
                                                 veh_cola.hora_entrada, espacio_vehiculo)
                        # Reordeno cola
                        self.cola.reordenar_espacios()
                        time.sleep(1)

                    # Reingreso de los de la calle a p1 y p2
                    if veh_p1 is not None:
                        self.valet.reingresar_en_clave(veh_p1, "p001")                        
                        print("\n---------------------------------------------------------")
                        print("Moviendo vehículo placa", veh_p1.placa, "ingresa nuevamente a P1")
                        print("---------------------------------------------------------")
                        time.sleep(1)
                    if veh_p2 is not None:
                        self.valet.reingresar_en_clave(veh_p2, "p002")
                        print("\n---------------------------------------------------------")
                        print("Moviendo vehículo placa", veh_p2.placa, "ingresa nuevamente a P2")
                        print("---------------------------------------------------------")
                        time.sleep(1)                    
                    return

            # Proceso normal si no estaba en últimos dos espacios
            self.vehiculos_dentro.pop(placa)
            espacio_liberado = self.liberar_espacio(placa, vehiculo.tipo)

            hora_salida = datetime.now()
            total, horas_cobradas = Cobro.calcular(vehiculo.hora_entrada, hora_salida, vehiculo.tipo, self.configuracion)

            registro = RegistroDeSalida(
                vehiculo.placa,
                vehiculo.tipo,
                vehiculo.hora_entrada,
                hora_salida,
                total
            )
            self.historial.agregar_registro(registro)

            # Delego tiquet salida a Impresion
            Impresion.tiquet_salida(vehiculo.placa, vehiculo.tipo,
                                   vehiculo.hora_entrada, hora_salida,
                                   horas_cobradas, total)

            # Al sacar vehículo de parqueo, si hay autos en espera, el primero pasa a parqueo
            if vehiculo.tipo == "auto":
                if self.cola.cola_espera_autos:
                    veh_cola = self.cola.sacar_vehiculo_cola()
                    self.cola.reordenar_espacios()

                    espacio_asignado = self.espacios.asignar_espacio_libre("auto", veh_cola.placa)
                    self.vehiculos_dentro[veh_cola.placa] = veh_cola
                    print("\n---------------------------------------------------------")
                    print("\nVehículo con placa " + veh_cola.placa + " ingresó de espera a posición " + clave.upper())
                    print("---------------------------------------------------------")
                    time.sleep(1)

                    Impresion.tiquet_ingreso(veh_cola.placa, veh_cola.tipo,
                                             veh_cola.hora_entrada, espacio_asignado)
            return

        # Ver si está en valet
        veh_valet = self.valet.remover_por_placa(placa)
        if veh_valet is not None:
            hora_salida = datetime.now()
            total, horas_cobradas = Cobro.calcular(veh_valet.hora_entrada, hora_salida, veh_valet.tipo, self.configuracion)

            # Agregar registro de salida al historial
            registro = RegistroDeSalida(
                veh_valet.placa,
                veh_valet.tipo,
                veh_valet.hora_entrada,
                hora_salida,
                total
            )
            self.historial.agregar_registro(registro)

            Impresion.tiquet_salida(veh_valet.placa, veh_valet.tipo, veh_valet.hora_entrada, hora_salida, horas_cobradas, total)
            time.sleep(1)
            self.mover_espera_a_valet()
            return

        # Ver si está en cola
        en_cola = False
        for v in self.cola.cola_espera_autos:
            if v.placa == placa:
                en_cola = True
                vehiculo = v
                break
        if en_cola:
            self.cola.cola_espera_autos.remove(vehiculo)
            for clave, placa_esp in self.cola.espacios_cola.items():
                if placa_esp == vehiculo.placa:
                    self.cola.espacios_cola[clave] = None
                    break
            print("\nVehículo con placa", placa, "fue retirado de la cola de espera.")
            print("---------------------------------------------------------")
            time.sleep(1)
            return

        print("\nEste vehículo no está en el parqueo, ni en valet, ni en la cola de espera.")
        time.sleep(1)

    # Recorro la cola y pregunto si quieren pasar a valet
    def mover_espera_a_valet(self):
        # Reviso si hay espacio en valet
        espacio_valet_disponible = None
        for clave, valor in self.valet.espacios_valet.items():
            if valor is None:
                espacio_valet_disponible = clave
                break

        if espacio_valet_disponible is None:
            return  # No hay espacios en valet

        # Si no hay vehículos en cola no hago nada
        if not self.cola.cola_espera_autos:
            return

        # Recorro la cola en orden preguntando
        for idx, vehiculo in enumerate(self.cola.cola_espera_autos):
            print("\nHay un espacio libre en valet.")
            print("El vehículo con placa " + vehiculo.placa + " está en posición " + str(idx + 1) + " de la cola.")
            print("¿Desea cambiar a valet? (si/no)")

            # Valido la respuesta del usuario
            while True:
                respuesta = input("Ingrese su respuesta: ").strip().lower()
                if respuesta in ["sí", "si", "no"]:
                    break
                print("Respuesta inválida. Por favor responda 'si' o 'no'.")

            # Si acepta pasar a valet
            if respuesta in ["sí", "si"]:
                espacio_asignado = self.valet.agregar_valet(vehiculo)
                if espacio_asignado is None:
                    print("No se pudo asignar el vehículo a valet. Intente luego.")
                    return

                # Quito el vehículo de la cola y libero su espacio
                self.cola.cola_espera_autos.pop(idx)
                for clave, placa in self.cola.espacios_cola.items():
                    if placa == vehiculo.placa:
                        self.cola.espacios_cola[clave] = None
                        break

                # Reordeno la cola después de la salida
                self.cola.reordenar_espacios()

                # Imprimo ticket
                print("\n---------------------------------------------------------")
                print("Vehículo con placa " + vehiculo.placa + " ingresó a valet en posición " + espacio_valet_disponible.upper())
                print("---------------------------------------------------------")
                time.sleep(1)
                Impresion.tiquet_ingreso(vehiculo.placa, vehiculo.tipo, vehiculo.hora_entrada, espacio_valet_disponible, "(Deja llaves)")
                return  # Solo muevo un vehículo

    # Mostrar espacios con placa o libres
    def mostrar_espacios(self):
        # Muestra la vista detallada de los espacios
        self.mostrar_espacios_detallados()

    # Mostrar cola de espera
    def mostrar_cola(self):
        self.cola.mostrar_cola_espera()


    # Consultar placa en parqueo o cola o valet
    def consultar_placa(self, placa):
        if placa in self.vehiculos_dentro:
            print("\nEl vehículo con placa", placa, "está en el parqueo.")
            for clave, val in self.espacios.espacios_autos.items():
                if val == placa:
                    print("Espacio:", clave)
                    time.sleep(1)
                    continue
            for clave, val in self.valet.espacios_valet.items():
                if val == placa:
                    print("Espacio (valet):", clave)
                    time.sleep(1)
                    continue
        else:
            for clave, val in self.valet.espacios_valet.items():
                if val == placa:
                    print("\nEl vehículo con placa", placa, "está en valet en espacio", clave)
                    time.sleep(1)
                    continue
            for clave, val in self.cola.espacios_cola.items():
                if val == placa:
                    print("\nEl vehículo con placa", placa, "está en la cola de espera en espacio", clave)
                    time.sleep(1)
                    continue
            print("\nEl vehículo con placa", placa, "no está en el parqueo, valet ni en la cola.")
            time.sleep(1)

    # Ver historial por placa (delegado a Historial e Impresion)
    def ver_historial_por_placa(self, placa):
        encontrados = self.historial.buscar_por_placa(placa)        
        if not encontrados:
            print("\nNo se encontraron registros.")
            return        
        Impresion.imprimir_historial(encontrados)
        
