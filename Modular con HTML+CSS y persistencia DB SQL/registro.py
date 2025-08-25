# registro.py

# Esta clase guarda los datos de cada salida de un vehículo del parqueo
class RegistroDeSalida:
    def __init__(self, placa, tipo, hora_entrada, hora_salida, total_pagado):
        # Guarda la placa del vehículo
        self.placa = placa
        # Guarda el tipo de vehículo (auto, moto, etc.)
        self.tipo = tipo
        # Guarda la fecha y hora de entrada del vehículo
        self.hora_entrada = hora_entrada
        # Guarda la fecha y hora de salida del vehículo
        self.hora_salida = hora_salida
        # Guarda el total que se pagó por el tiempo de parqueo
        self.total_pagado = total_pagado
