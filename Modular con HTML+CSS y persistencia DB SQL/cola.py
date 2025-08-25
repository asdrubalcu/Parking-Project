# cola.py

import time

# Esta clase gestiona la cola de espera para autos y sus espacios (e001, e002, e003)
class ColaEspera:
    def __init__(self):
        # Lista que guarda instancias de Vehiculo en orden FIFO
        self.cola_espera_autos = []
        # Diccionario de espacios para la cola con claves e001..e003
        self.espacios_cola = {"e001": None, "e002": None, "e003": None}

    # Agregar a cola de espera autos, si hay espacio en cola, devuelve espacio asignado o None si llena
    def agregar_cola_espera(self, vehiculo):
        for clave in sorted(self.espacios_cola):
            if self.espacios_cola[clave] is None:
                self.espacios_cola[clave] = vehiculo.placa
                self.cola_espera_autos.append(vehiculo)
                return clave
        return None

    # Sacar primer vehículo de la cola, y liberar su espacio en la cola
    def sacar_vehiculo_cola(self):
        if not self.cola_espera_autos:
            return None
        vehiculo = self.cola_espera_autos.pop(0)
        for clave, placa in self.espacios_cola.items():
            if placa == vehiculo.placa:
                self.espacios_cola[clave] = None
                break
        return vehiculo

    # Reordenar los espacios de la cola según el orden actual de la lista
    def reordenar_espacios(self):
        placas_cola = [v.placa for v in self.cola_espera_autos]
        # Primero limpio todos los espacios
        for clave in self.espacios_cola:
            self.espacios_cola[clave] = None
        # Luego reasigno según el orden actual
        for i in range(len(placas_cola)):
            clave = "e" + str(i + 1).zfill(3)
            if clave in self.espacios_cola:
                self.espacios_cola[clave] = placas_cola[i]

    # Mostrar cola de espera con placa o libres
    def mostrar_cola_espera(self):
        print("\n----- Cola de Espera para Autos -----")
        for clave in sorted(self.espacios_cola):
            placa = self.espacios_cola[clave]
            if placa is None:
                print(clave + ": Libre")
            else:
                print(clave + ": " + placa)
        time.sleep(2)
