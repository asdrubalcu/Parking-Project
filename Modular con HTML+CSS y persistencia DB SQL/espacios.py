# espacios.py

import time

# Esta clase gestiona los espacios del parqueo para autos y motos
class EspaciosParqueo:
    def __init__(self, configuracion):
        # Guarda la configuración del parqueo para conocer cantidades
        self.configuracion = configuracion
        # Diccionarios de espacios para autos y motos
        self.espacios_autos = {}
        self.espacios_motos = {}
        # Inicializa los espacios según la configuración dinámica
        self.actualizar_espacios()

    # Método para actualizar espacios según configuración actual
    def actualizar_espacios(self):
        # Guarda las placas que estaban ocupando espacios antes del cambio
        placas_autos = [placa for placa in self.espacios_autos.values() if placa is not None]
        placas_motos = [placa for placa in self.espacios_motos.values() if placa is not None]

        # Crea nuevos diccionarios con claves a001..aN y m001..mN
        self.espacios_autos = {}
        for i in range(self.configuracion.cantidad_espacios_autos):
            clave = "a" + str(i + 1).zfill(3)
            if i < len(placas_autos):
                self.espacios_autos[clave] = placas_autos[i]
            else:
                self.espacios_autos[clave] = None

        self.espacios_motos = {}
        for i in range(self.configuracion.cantidad_espacios_motos):
            clave = "m" + str(i + 1).zfill(3)
            if i < len(placas_motos):
                self.espacios_motos[clave] = placas_motos[i]
            else:
                self.espacios_motos[clave] = None

    # Buscar espacio libre según tipo y asignar placa, devuelve el código del espacio o None
    def asignar_espacio_libre(self, tipo, placa):
        if tipo == "auto":
            for clave in sorted(self.espacios_autos):
                if self.espacios_autos[clave] is None:
                    self.espacios_autos[clave] = placa
                    return clave
            return None
        elif tipo == "moto":
            for clave in sorted(self.espacios_motos):
                if self.espacios_motos[clave] is None:
                    self.espacios_motos[clave] = placa
                    return clave
            return None
        else:
            return None

    # Liberar espacio al sacar vehículo, recibe placa y tipo, devuelve código de espacio liberado
    def liberar_espacio(self, placa, tipo):
        if tipo == "auto":
            for clave, valor in self.espacios_autos.items():
                if valor == placa:
                    self.espacios_autos[clave] = None
                    return clave
        elif tipo == "moto":
            for clave, valor in self.espacios_motos.items():
                if valor == placa:
                    self.espacios_motos[clave] = None
                    return clave
        return None

    # Mostrar espacios con placa o libres
    def mostrar_espacios_detallados(self):
        print("\n----- Espacios para Autos -----")
        for clave in sorted(self.espacios_autos):
            ocupado = self.espacios_autos[clave]
            if ocupado is None:
                print(clave + ": Libre")
            else:
                print(clave + ": " + ocupado)
        time.sleep(2)

        print("\n----- Espacios para Motos -----")
        for clave in sorted(self.espacios_motos):
            ocupado = self.espacios_motos[clave]
            if ocupado is None:
                print(clave + ": Libre")
            else:
                print(clave + ": " + ocupado)
        time.sleep(2)
