# administracion.py
import time

# Clase que guarda la configuración del parqueo
class AdministracionParqueo:
    def __init__(self):
        # Inicializo valores por defecto que se pueden ajustar desde el menú
        self.cantidad_espacios_autos = 1
        self.cantidad_espacios_motos = 1
        self.tarifas = {"auto": 1000, "moto": 500}
        self.cobro_fraccionado = False  # False: para solo horas completas. True: para cobro fraccionado
        self.tipos_vehiculo = ["auto", "moto"]

    # Muestro la configuración actual
    def mostrar_configuracion(self):
        print("\n----------- CONFIGURACIÓN DEL PARQUEO -----------")
        print("Cantidad de espacios para autos:", self.cantidad_espacios_autos)
        print("Cantidad de espacios para motos:", self.cantidad_espacios_motos)
        print("Tarifas por tipo:")
        for tipo, tarifa in self.tarifas.items():
            print("-", tipo.upper(), "→ ₡", tarifa, "por hora")
        if self.cobro_fraccionado:
            print("Método de cobro: Fraccionado (media hora después de la primera)")
        else:
            print("Método de cobro: Solo horas completas")
        print("--------------------------------------------------")
        time.sleep(2)

    # Cambia la cantidad de espacios para autos
    def cambiar_espacios_autos(self, nuevo):
        self.cantidad_espacios_autos = max(0, int(nuevo))
        print("Actualizado número de espacios para autos a", self.cantidad_espacios_autos)
        time.sleep(1)

    # Cambia la cantidad de espacios para motos
    def cambiar_espacios_motos(self, nuevo):
        self.cantidad_espacios_motos = max(0, int(nuevo))
        print("Actualizado número de espacios para motos a", self.cantidad_espacios_motos)
        time.sleep(1)

    # Cambia la tarifa por tipo de vehículo solo motos o autos
    def cambiar_tarifa(self, tipo, nueva):
        if tipo in self.tarifas:
            self.tarifas[tipo] = int(nueva)
            print("Tarifa de", tipo, "actualizada a", self.tarifas[tipo])
        else:
            print("Tipo no válido para tarifa.")
        time.sleep(1)

    # Cambia el método de cobro (True = fraccionado, False = hora copleta)
    def cambiar_cobro(self, fraccionado):
        self.cobro_fraccionado = bool(fraccionado)
        print("Método de cobro actualizado.")
        time.sleep(1)
