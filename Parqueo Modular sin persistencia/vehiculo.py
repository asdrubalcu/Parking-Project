# vehiculo.py

from datetime import datetime

# Esta clase tiene responsabilidad el manejo de vehículo con su placa, tipo y hora de entrada
class Vehiculo:
    def __init__(self, placa, tipo):
        # Guarda la placa del vehículo
        self.placa = placa
        # Guarda el tipo del vehículo (auto, moto, etc.)
        self.tipo = tipo
        # Guarda la fecha y hora de entrada del vehículo al parqueo
        self.hora_entrada = datetime.now()
