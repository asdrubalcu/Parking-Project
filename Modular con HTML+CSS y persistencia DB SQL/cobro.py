# cobro.py

# Clase para calcular el cobro según tarifa y configuración en parqueo modificable
class Cobro:
    @staticmethod
    def calcular(hora_entrada, hora_salida, tipo, configuracion):
        # Calculo el monto total y las horas a cobrar
        tiempo = hora_salida - hora_entrada
        minutos = tiempo.total_seconds() // 60
        tarifa_base = configuracion.tarifas.get(tipo, 500)

        if minutos <= 60:
            total = tarifa_base
            horas_cobradas = 1
        else:
            minutos_restantes = minutos - 60
            if configuracion.cobro_fraccionado:
                medias_horas = int(minutos_restantes // 30)
                if minutos_restantes % 30 > 0:
                    medias_horas += 1
                total = tarifa_base + (medias_horas * (tarifa_base // 2))
                horas_cobradas = 1 + (medias_horas * 0.5)
            else:
                horas = int(minutos // 60)
                if minutos % 60 > 0:
                    horas += 1
                total = horas * tarifa_base
                horas_cobradas = horas

        return total, horas_cobradas
