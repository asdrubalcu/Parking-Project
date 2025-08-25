# historial.py

# Esta clase tiene la lista de registros y permite buscar por placa
class Historial:
    def __init__(self):
        # Lista que guarda instancias de los Registro De Salida
        self.historial = []

    # Agrega un registro al historial
    def agregar_registro(self, registro):
        self.historial.append(registro)

    # Busca todos los registros que coinciden con una placa
    def buscar_por_placa(self, placa):
        encontrados = [r for r in self.historial if r.placa == placa]
        return encontrados

    # Devuelve todos los registros
    def todos(self):
        return self.historial
