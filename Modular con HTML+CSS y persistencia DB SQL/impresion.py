# impresion.py

from datetime import datetime
import time

# Esta clase es para las impresiones en consola como tickets, configuración, historial y movimientos
class Impresion:

    @staticmethod
    def mostrar_configuracion(cantidad_autos, cantidad_motos, tarifas, cobro_fraccionado):
        # Muestra en pantalla la configuración actual del parqueo
        print("\n----------- CONFIGURACIÓN DEL PARQUEO -----------")
        print("Cantidad de espacios para autos:", cantidad_autos)
        print("Cantidad de espacios para motos:", cantidad_motos)
        print("Tarifas por tipo:")
        for tipo in tarifas:
            print("-", tipo.upper(), "→ ₡", tarifas[tipo], "por hora")
        if cobro_fraccionado:
            print("Método de cobro: Fraccionado (media hora después de la primera)")
        else:
            print("Método de cobro: Solo horas completas")
        print("--------------------------------------------------")
        time.sleep(2)

    @staticmethod
    def tiquet_ingreso(placa, tipo, hora_entrada, espacio, extra=""):
        # Muestra el ticket de ingreso con los datos del vehículo y espacio asignado
        print("\n--------------------------------------------")
        print("        T I Q U E T   D E   I N G R E S O    ")
        print("--------------------------------------------")
        print("Placa:", placa.upper())
        print("Tipo de vehículo:", tipo.upper())
        print("Hora de entrada:", hora_entrada.strftime("%d/%m/%Y %H:%M:%S"))
        print("Espacio asignado:", espacio.upper(), extra)
        print("--------------------------------------------")
        time.sleep(2)

    @staticmethod
    def tiquet_salida(placa, tipo, hora_entrada, hora_salida, horas_cobradas, total):
        # Muestra el ticket de salida con datos del cobro y tiempos
        print("\n--------------------------------------------")
        print("         T I Q U E T   D E   S A L I D A     ")
        print("--------------------------------------------")
        print("Placa:", placa.upper())
        print("Tipo de vehículo:", tipo.upper())
        print("Hora de entrada:", hora_entrada.strftime("%d/%m/%Y %H:%M:%S"))
        print("Hora de salida :", hora_salida.strftime("%d/%m/%Y %H:%M:%S"))
        print("Tiempo cobrado :", horas_cobradas, "hora(s)")
        print("Total a pagar  : ₡", total)
        print("--------------------------------------------")
        time.sleep(2)

    @staticmethod
    def imprimir_movimiento(placa, origen, destino):
        # Muestra en pantalla el movimiento de un vehículo entre espacios
        print("\nMoviendo vehículo placa", placa.upper(), "de", origen.upper(), "a", destino.upper())

    @staticmethod
    def imprimir_historial(registros):
        # Muestra el historial completo de ingresos y salidas
        print("\n--------------------------------------------")
        print("  H I S T O R I A L   D E   I N G R E S O S ")
        print("--------------------------------------------")
        for item in registros:
            print("Placa:", item.placa.upper())
            print("Tipo:", item.tipo.upper())
            print("Entrada:", item.hora_entrada.strftime("%d/%m/%Y %H:%M:%S"))
            print("Salida :", item.hora_salida.strftime("%d/%m/%Y %H:%M:%S"))
            print("Total  : ₡", item.total_pagado)
            print("--------------------------------------------")
            time.sleep(1)
