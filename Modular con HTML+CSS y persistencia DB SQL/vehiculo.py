# vehiculo.py

from datetime import datetime

# Esta clase es para los vehículo con su placa, tipo y hora de entrada, etc
class Vehiculo:
    def __init__(self, placa, tipo, marca=None, modelo=None, año=None, color=None):
        # Guardo la placa del vehículo
        self.placa = placa
        # Guardo el tipo del vehículo (auto, moto, etc)
        self.tipo = tipo
        # Guardo la fecha y hora de entrada del vehículo al parqueo
        self.hora_entrada = datetime.now()
        # Guardo la marca del vehículo (cadena o None)
        self.marca = marca
        # Guardo el modelo del vehículo (cadena o None)
        self.modelo = modelo
        # Guardo el año del vehículo (entero o None)
        self.año = año
        # Guardo el color del vehículo (cadena o None)
        self.color = color
    # Permito campos vacíos (practicidad clientes "genéricos")