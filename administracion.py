#administracion.py

from impresion import Impresion

# Esta clase guarda y gestiona la configuración del parqueo
class AdministracionParqueo:
    def __init__(self):
        # Define la cantidad máxima de espacios para autos
        self.cantidad_espacios_autos = 1

        # Define la cantidad máxima de espacios para motos
        self.cantidad_espacios_motos = 1

        # Define las tarifas por hora para cada tipo de vehículo
        self.tarifas = {
            "auto": 1000,
            "moto": 500
        }

        # Define los tipos de vehículos permitidos en el parqueo
        self.tipos_vehiculo = ["auto", "moto"]

        # Define el método de cobro
        # True indica que se cobra en fracciones de media hora después de la primera hora
        # False indica que se cobra solo por horas completas
        self.cobro_fraccionado = True

    def cambiar_espacios_autos(self, nueva_cantidad):
        # Cambia la cantidad máxima de espacios para autos
        self.cantidad_espacios_autos = nueva_cantidad

    def cambiar_espacios_motos(self, nueva_cantidad):
        # Cambia la cantidad máxima de espacios para motos
        self.cantidad_espacios_motos = nueva_cantidad

    def cambiar_tarifa(self, tipo, nueva_tarifa):
        # Cambia la tarifa por hora para el tipo de vehículo indicado
        self.tarifas[tipo] = nueva_tarifa

    def cambiar_cobro(self, usar_fraccionado):
        # Cambia el método de cobro a fraccionado o por horas completas
        self.cobro_fraccionado = usar_fraccionado

    def mostrar_configuracion(self):
        # Muestra la configuración actual del parqueo usando la clase Impresión
        Impresion.mostrar_configuracion(
            self.cantidad_espacios_autos,
            self.cantidad_espacios_motos,
            self.tarifas,
            self.cobro_fraccionado
        )
