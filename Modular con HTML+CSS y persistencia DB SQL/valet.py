# valet.py

import time

# Esta clase gestiona el valet PILA TIPO LIFO y dos espacios predefinidos p1 y p2
# Estos espacios se configura que SOLO estorban la salida a los dos últimos espacios de autos
# Al salir esos, se mueve Valet, último en entrar primero en salir
class Valet:
    def __init__(self):
        # Lista LIFO que guarda instancias de Vehiculo
        self.valet_autos = []
        # Diccionario de espacios p1 y p2 que guarda placas o None
        self.espacios_valet = {"p001": None, "p002": None}

    # Agregar a valet autos, si hay espacio, devuelve espacio asignado o None si lleno
    def agregar_valet(self, vehiculo):
        for clave in self.espacios_valet:
            if self.espacios_valet[clave] is None:
                self.espacios_valet[clave] = vehiculo.placa
                self.valet_autos.append(vehiculo)
                return clave
        return None

    # Sacar último vehículo ingresado al valet
    def sacar_vehiculo_valet(self):
        if not self.valet_autos:
            return None
        vehiculo = self.valet_autos.pop()  # LIFO: último en entrar, primero en salir
        for clave, placa in self.espacios_valet.items():
            if placa == vehiculo.placa:
                self.espacios_valet[clave] = None
                break
        return vehiculo

    # Remover de valet por placa y devolver la instancia del Vehiculo removido
    def remover_por_placa(self, placa):
        for i, v in enumerate(self.valet_autos):
            if v.placa == placa:
                vehiculo = self.valet_autos.pop(i)
                # Liberar espacio valet correspondiente
                for clave, placa_esp in self.espacios_valet.items():
                    if placa_esp == placa:
                        self.espacios_valet[clave] = None
                        break
                return vehiculo
        return None

    # Reingresar un vehículo en un espacio de valet específico (p1 o p2)
    def reingresar_en_clave(self, vehiculo, clave):
        # Asigna placa al espacio y agrega vehiculo a la pila LIFO
        if clave in self.espacios_valet and self.espacios_valet[clave] is None:
            self.espacios_valet[clave] = vehiculo.placa
            self.valet_autos.append(vehiculo)
            return True
        return False

    # Mostrar espacios valet
    def mostrar_valet(self):
        print("\n----- Espacios para Valet  -----")
        for clave in sorted(self.espacios_valet):
            ocupado = self.espacios_valet[clave]
            if ocupado is None:
                print(clave + ": Libre")
            else:
                print(clave + ": " + ocupado)
        time.sleep(2)
