# parqueo.py

from datetime import datetime
import time

# Importo los módulos con responsabilidades específicas
from impresion import Impresion
from vehiculo import Vehiculo
from registro import RegistroDeSalida
from espacios import EspaciosParqueo
from valet import Valet
from cola import ColaEspera
from cobro import Cobro
from historial import Historial

# Importo el gestor de BD
from db_manager import DbManager

# Clase que maneja el parqueo, usa la configuración de la administración
class Parqueo:
    def __init__(self, configuracion):
        # Guarda la configuración del parqueo
        self.configuracion = configuracion

        # Instancias con responsabilidades separadas para mejor organización
        self.espacios = EspaciosParqueo(configuracion)
        self.valet = Valet()
        self.cola = ColaEspera()
        self.historial = Historial()

        # Diccionario de vehículos dentro: placa -> Vehiculo
        self.vehiculos_dentro = {}

        # Diccionario para recordar atributos por placa: placa -> dict(tipo, marca, modelo, año, color)
        self.placas_conocidas = {}

        # Calle: posiciones temporales para mostrar el movimiento valet->calle y calle->valet
        self.calle = {"calle1": None, "calle2": None}
        self.calle_objs = {"calle1": None, "calle2": None}

        # Gestor de persistencia
        try:
            self.db = DbManager()
            # Cargo estado guardado si existe (sobrescribe estructuras internas)
            self.db.load_state(self)
        except Exception as e:
            # Si falla la BD, no interrumpo el programa; sigo en modo sin persistencia
            print("Advertencia: no se pudo conectar a la base de datos.Error:", e)
            self.db = None

    def actualizar_espacios(self):
        self.espacios.actualizar_espacios()
        if self.db:
            self.db.save_state(self)

    def asignar_espacio_libre(self, tipo, placa):
        clave = self.espacios.asignar_espacio_libre(tipo, placa)
        if self.db:
            self.db.save_state(self)
        return clave

    def liberar_espacio(self, placa, tipo):
        clave = self.espacios.liberar_espacio(placa, tipo)
        if clave is not None and self.db:
            self.db.save_state(self)
            try:
                self.mover_espera_a_valet(interactive=False)
                self.db.save_state(self)
            except:
                pass
        return None if clave is None else clave

    def agregar_cola_espera(self, vehiculo):
        clave = self.cola.agregar_cola_espera(vehiculo)
        if self.db:
            self.db.save_state(self)
        return clave

    def sacar_vehiculo_cola(self):
        v = self.cola.sacar_vehiculo_cola()
        if self.db:
            self.db.save_state(self)
        return v

    def agregar_valet(self, vehiculo):
        clave = self.valet.agregar_valet(vehiculo)
        if self.db:
            self.db.save_state(self)
        return clave

    def sacar_vehiculo_valet(self):
        v = self.valet.sacar_vehiculo_valet()
        if self.db:
            self.db.save_state(self)
        return v

    def mostrar_espacios_detallados(self):
        self.espacios.mostrar_espacios_detallados()
        self.valet.mostrar_valet()
        self.cola.mostrar_cola_espera()

    def _esta_en_parqueo(self, placa):
        return placa in self.vehiculos_dentro

    def _esta_en_valet(self, placa):
        for v in self.valet.valet_autos:
            if v.placa == placa:
                return True
        return False

    def _esta_en_cola(self, placa):
        for v in self.cola.cola_espera_autos:
            if v.placa == placa:
                return True
        return False

    def meter_vehiculo(self, placa, tipo, marca=None, modelo=None, anio=None, color=None):
        # No permito placas vacías
        if placa is None or placa.strip() == "":
            print("\nNo se puede procesar una placa vacía.")
            time.sleep(1)
            return

        # Si conozco la placa, uso los atributos guardados
        if placa in self.placas_conocidas:
            datos = self.placas_conocidas[placa]
            tipo = datos.get("tipo", tipo)
            marca = datos.get("marca", marca)
            modelo = datos.get("modelo", modelo)
            año = datos.get("año", año)
            color = datos.get("color", color)

        # Verificaciones
        if self._esta_en_parqueo(placa):
            print("\nEste vehículo ya está dentro del parqueo.")
            time.sleep(1)
            return
        if tipo not in self.configuracion.tipos_vehiculo:
            print("\nEste tipo de vehículo no es aceptado.")
            time.sleep(1)
            return
        if self._esta_en_cola(placa):
            print("\nEste vehículo ya está en la cola de espera.")
            time.sleep(1)
            return
        if self._esta_en_valet(placa):
            print("\nEste vehículo ya está en valet.")
            time.sleep(1)
            return

        vehiculo = Vehiculo(placa, tipo, marca, modelo, año, color)

        if tipo == "moto":
            espacio = self.espacios.asignar_espacio_libre("moto", placa)
            if espacio is None:
                print("\nEl parqueo para motos está lleno. No hay cola de espera para motos.")
                time.sleep(1)
                return
            else:
                self.vehiculos_dentro[placa] = vehiculo
                self.placas_conocidas[placa] = {"tipo": tipo, "marca": marca, "modelo": modelo, "año": año, "color": color}
                Impresion.tiquet_ingreso(placa, tipo, vehiculo.hora_entrada, espacio)
                if self.db:
                    self.db.save_state(self)
                return

        if tipo == "auto":
            espacio = self.espacios.asignar_espacio_libre("auto", placa)
            if espacio is None:
                espacio_valet_disponible = None
                for clave, valor in self.valet.espacios_valet.items():
                    if valor is None:
                        espacio_valet_disponible = clave
                        break
                espacio_cola_disponible = None
                for clave, valor in self.cola.espacios_cola.items():
                    if valor is None:
                        espacio_cola_disponible = clave
                        break
                if espacio_valet_disponible is None and espacio_cola_disponible is None:
                    print("\nParqueo lleno, valet lleno y cola de espera llena. Intente más tarde.")
                    time.sleep(1)
                    return
                #opcione cuando está lleno para autos valet o espera o salir
                opciones = []
                if espacio_valet_disponible is not None:
                    opciones.append("valet")
                if espacio_cola_disponible is not None:
                    opciones.append("espera")
                print("\nEl parqueo está lleno.")
                for i, opcion in enumerate(opciones, 1):
                    print(str(i) + ". Estacionar en " + opcion)
                print ("0. Dejar el parqueo.")
                while True:
                    eleccion = input("Elija una opción: ").strip()
                    if eleccion == "0":
                        return
                    if eleccion.isdigit():
                        numero = int(eleccion)
                        if 1 <= numero <= len(opciones):
                            break
                    print("Opción inválida. Intente nuevamente.")
                seleccion = opciones[numero - 1]

                if seleccion == "valet":
                    espacio_asignado = self.valet.agregar_valet(vehiculo)
                    if espacio_asignado is None:
                        print("\nNo se pudo asignar en valet.")
                        time.sleep(1)
                        return
                    self.placas_conocidas[placa] = {"tipo": tipo, "marca": marca, "modelo": modelo, "anio": anio, "color": color}
                    print("\nVehículo agregado a valet en espacio " + espacio_asignado)
                    Impresion.tiquet_ingreso(placa, tipo, vehiculo.hora_entrada, espacio_asignado, "(Deja llaves)")
                    if self.db:
                        self.db.save_state(self)
                    return

                if seleccion == "espera":
                    espacio_asignado = self.cola.agregar_cola_espera(vehiculo)
                    if espacio_asignado is None:
                        print("\nNo se pudo agregar a la cola de espera.")
                        time.sleep(1)
                        return
                    self.placas_conocidas[placa] = {"tipo": tipo, "marca": marca, "modelo": modelo, "anio": anio, "color": color}
                    print("\nVehículo agregado a cola de espera en espacio " + espacio_asignado)
                    time.sleep(1)
                    if self.db:
                        self.db.save_state(self)
                    return

            else:
                self.vehiculos_dentro[placa] = vehiculo
                self.placas_conocidas[placa] = {"tipo": tipo, "marca": marca, "modelo": modelo, "anio": anio, "color": color}
                Impresion.tiquet_ingreso(placa, tipo, vehiculo.hora_entrada, espacio)
                if self.db:
                    self.db.save_state(self)
                return

    def sacar_vehiculo(self, placa, web_mode=False):
        # Devuelve un dict con info y persiste historial en BD
        resultado = {
            "registro_salida": None,
            "ingreso_desde_cola": None,
            "calle_movimientos": []
        }

        if placa is None or placa.strip() == "":
            print("\nNo se puede procesar una placa vacía.")
            time.sleep(1)
            return resultado

        # Si está en parqueo normal
        if placa in self.vehiculos_dentro:
            vehiculo = self.vehiculos_dentro[placa]
            if vehiculo.tipo == "auto":
                ultimo = "a" + str(self.configuracion.cantidad_espacios_autos).zfill(3)
                penultimo = "a" + str(self.configuracion.cantidad_espacios_autos - 1).zfill(3)
                espacio_vehiculo = None
                for clave, valor in self.espacios.espacios_autos.items():
                    if valor == placa:
                        espacio_vehiculo = clave
                        break
                if espacio_vehiculo in [ultimo, penultimo]:
                    # mover P2 y P1 a la calle
                    if self.valet.espacios_valet["p002"] is not None:
                        placa_p2 = self.valet.espacios_valet["p002"]
                        veh_p2 = self.valet.remover_por_placa(placa_p2)
                        if veh_p2 is not None:
                            self.valet.espacios_valet["p002"] = None
                            self.calle["calle2"] = veh_p2.placa
                            self.calle_objs["calle2"] = {"veh": veh_p2, "orig": "p002"}
                            resultado["calle_movimientos"].append({"calle": "calle2", "placa": veh_p2.placa, "orig": "p002"})
                    else:
                        self.calle["calle2"] = None
                        self.calle_objs["calle2"] = None

                    if self.valet.espacios_valet["p001"] is not None:
                        placa_p1 = self.valet.espacios_valet["p001"]
                        veh_p1 = self.valet.remover_por_placa(placa_p1)
                        if veh_p1 is not None:
                            self.valet.espacios_valet["p001"] = None
                            self.calle["calle1"] = veh_p1.placa
                            self.calle_objs["calle1"] = {"veh": veh_p1, "orig": "p001"}
                            resultado["calle_movimientos"].append({"calle": "calle1", "placa": veh_p1.placa, "orig": "p001"})
                    else:
                        self.calle["calle1"] = None
                        self.calle_objs["calle1"] = None

                    # remover vehículo del parqueo
                    self.vehiculos_dentro.pop(placa)
                    self.espacios.espacios_autos[espacio_vehiculo] = None

                    hora_salida = datetime.now()
                    total, horas_cobradas = Cobro.calcular(vehiculo.hora_entrada, hora_salida, vehiculo.tipo, self.configuracion)

                    registro = RegistroDeSalida(
                        vehiculo.placa,
                        vehiculo.tipo,
                        vehiculo.hora_entrada,
                        hora_salida,
                        total
                    )
                    # Insertar registro en historial memoria y BD
                    self.historial.agregar_registro(registro)
                    if self.db:
                        self.db.insert_historial(registro)
                    resultado["registro_salida"] = registro

                    Impresion.tiquet_salida(vehiculo.placa, vehiculo.tipo,
                                           vehiculo.hora_entrada, hora_salida,
                                           horas_cobradas, total)

                    # Si hay cola, mover primer de cola al espacio liberado
                    if self.cola.cola_espera_autos:
                        veh_cola = self.cola.sacar_vehiculo_cola()
                        self.espacios.espacios_autos[espacio_vehiculo] = veh_cola.placa
                        self.vehiculos_dentro[veh_cola.placa] = veh_cola

                        # Imprimo ticket de ingreso y también lo devuelvo en resultado para WEB
                        Impresion.tiquet_ingreso(veh_cola.placa, veh_cola.tipo,
                                                 veh_cola.hora_entrada, espacio_vehiculo)
                        resultado["ingreso_desde_cola"] = {"vehiculo": veh_cola, "espacio": espacio_vehiculo}
                        self.cola.reordenar_espacios()

                    # Guardo estado
                    if self.db:
                        self.db.save_state(self)
                    return resultado

            # proceso normal si no estaba en últimos dos espacios de autos
            self.vehiculos_dentro.pop(placa)
            self.liberar_espacio(placa, vehiculo.tipo)

            hora_salida = datetime.now()
            total, horas_cobradas = Cobro.calcular(vehiculo.hora_entrada, hora_salida, vehiculo.tipo, self.configuracion)

            registro = RegistroDeSalida(
                vehiculo.placa,
                vehiculo.tipo,
                vehiculo.hora_entrada,
                hora_salida,
                total
            )
            self.historial.agregar_registro(registro)
            if self.db:
                self.db.insert_historial(registro)

            Impresion.tiquet_salida(vehiculo.placa, vehiculo.tipo,
                                   vehiculo.hora_entrada, hora_salida,
                                   horas_cobradas, total)

            if vehiculo.tipo == "auto":
                if self.cola.cola_espera_autos:
                    veh_cola = self.cola.sacar_vehiculo_cola()
                    self.cola.reordenar_espacios()

                    espacio_asignado = self.espacios.asignar_espacio_libre("auto", veh_cola.placa)
                    self.vehiculos_dentro[veh_cola.placa] = veh_cola

                    Impresion.tiquet_ingreso(veh_cola.placa, veh_cola.tipo,
                                             veh_cola.hora_entrada, espacio_asignado)
                    resultado["ingreso_desde_cola"] = {"vehiculo": veh_cola, "espacio": espacio_asignado}

            if self.db:
                self.db.save_state(self)
            return resultado

        # Si está en Valet le aplico salida directa
        veh_valet = self.valet.remover_por_placa(placa)
        if veh_valet is not None:
            hora_salida = datetime.now()
            total, horas_cobradas = Cobro.calcular(veh_valet.hora_entrada, hora_salida, veh_valet.tipo, self.configuracion)

            registro = RegistroDeSalida(
                veh_valet.placa,
                veh_valet.tipo,
                veh_valet.hora_entrada,
                hora_salida,
                total
            )
            self.historial.agregar_registro(registro)
            if self.db:
                self.db.insert_historial(registro)
            resultado["registro_salida"] = registro

            Impresion.tiquet_salida(veh_valet.placa, veh_valet.tipo, veh_valet.hora_entrada, hora_salida, horas_cobradas, total)
            time.sleep(0.2)

            # dejar P1/P2 en calle si aplica
            if self.db:
                self.db.save_state(self)
            return resultado

        # Si está en la cola
        en_cola = False
        for v in self.cola.cola_espera_autos:
            if v.placa == placa:
                en_cola = True
                vehiculo = v
                break
        if en_cola:
            self.cola.cola_espera_autos.remove(vehiculo)
            for clave, placa_esp in self.cola.espacios_cola.items():
                if placa_esp == vehiculo.placa:
                    self.cola.espacios_cola[clave] = None
                    break

            hora_salida = datetime.now()
            registro = RegistroDeSalida(
                vehiculo.placa,
                vehiculo.tipo,
                vehiculo.hora_entrada,
                hora_salida,
                0
            )
            self.historial.agregar_registro(registro)
            if self.db:
                self.db.insert_historial(registro)
                self.db.save_state(self)

            print("\nVehículo con placa", placa, "fue retirado de la cola de espera.")
            time.sleep(1)
            return resultado

        print("\nEste vehículo no está en el parqueo, ni en valet, ni en la cola de espera.")
        time.sleep(1)
        return resultado

    # Mover espera a valet, si el cliente lo elige uso este método
    def mover_espera_a_valet(self, interactive=True):
        espacio_valet_disponible = None
        for clave, valor in self.valet.espacios_valet.items():
            if valor is None:
                espacio_valet_disponible = clave
                break
        if espacio_valet_disponible is None:
            return [] if not interactive else None
        if not self.cola.cola_espera_autos:
            return [] if not interactive else None
        if interactive:
            for idx in range(len(self.cola.cola_espera_autos)):
                vehiculo = self.cola.cola_espera_autos[idx]
                print("\nHay un espacio libre en valet.")
                print("El vehículo con placa " + vehiculo.placa + " está en la posición " + str(idx + 1) + " de la cola.")
                print("¿Desea cambiar a valet? (si/no)")
                while True:
                    respuesta = input("Ingrese su respuesta: ").strip().lower()
                    if respuesta in ["sí", "si", "no"]:
                        break
                    print("Respuesta inválida. Por favor responda 'si' o 'no'.")
                if respuesta in ["sí", "si"]:
                    espacio_asignado = self.valet.agregar_valet(vehiculo)
                    if espacio_asignado is None:
                        print("No se pudo asignar el vehículo a valet. Intente luego.")
                        return
                    self.cola.cola_espera_autos.pop(idx)
                    for clave, placa in self.cola.espacios_cola.items():
                        if placa == vehiculo.placa:
                            self.cola.espacios_cola[clave] = None
                            break
                    self.cola.reordenar_espacios()
                    Impresion.tiquet_ingreso(
                        vehiculo.placa,
                        vehiculo.tipo,
                        vehiculo.hora_entrada,
                        espacio_asignado,
                        "(Deja llaves)"
                    )
                    if self.db:
                        self.db.save_state(self)
                    return
                else:
                    continue
            print("\nNingún vehículo aceptó el valet. No se hicieron cambios.")
            return
        else:
            pendientes = []
            for idx, veh in enumerate(self.cola.cola_espera_autos):
                pendientes.append({"pos": idx + 1, "placa": veh.placa, "tipo": veh.tipo})
            return pendientes

    def aceptar_espera_a_valet(self, placa):
        for idx, v in enumerate(self.cola.cola_espera_autos):
            if v.placa == placa:
                espacio_asignado = self.valet.agregar_valet(v)
                if espacio_asignado is None:
                    return None
                self.cola.cola_espera_autos.pop(idx)
                for clave, placa_esp in self.cola.espacios_cola.items():
                    if placa_esp == placa:
                        self.cola.espacios_cola[clave] = None
                        break
                self.cola.reordenar_espacios()
                if self.db:
                    self.db.save_state(self)
                return espacio_asignado
        return None

    # Reingresar los vehiculos que están en la calle hacia sus posiciones originales de valet
    def reingresar_calle(self):
        reingresos = []
        for clave_calle in ["calle1", "calle2"]:
            info = self.calle_objs.get(clave_calle)
            if info is None:
                continue
            veh = info.get("veh")
            orig = info.get("orig")
            ok = self.valet.reingresar_en_clave(veh, orig)
            if ok:
                reingresos.append({"placa": veh.placa, "orig": orig})
                self.calle[clave_calle] = None
                self.calle_objs[clave_calle] = None
        if self.db and reingresos:
            self.db.save_state(self)
        return reingresos

    def mostrar_espacios(self):
        self.mostrar_espacios_detallados()

    def mostrar_cola(self):
        self.cola.mostrar_cola_espera()

    def consultar_placa(self, placa):
        if placa is None or placa.strip() == "":
            print("\nNo se puede consultar una placa vacía.")
            time.sleep(1)
            return
        if placa in self.vehiculos_dentro:
            print("\nEl vehículo con placa", placa, "está en el parqueo.")
            for clave, val in self.espacios.espacios_autos.items():
                if val == placa:
                    print("Espacio:", clave)
                    time.sleep(1)
            for clave, val in self.valet.espacios_valet.items():
                if val == placa:
                    print("Espacio (valet):", clave)
                    time.sleep(1)
            return
        for clave, val in self.valet.espacios_valet.items():
            if val == placa:
                print("\nEl vehículo con placa", placa, "está en valet en espacio", clave)
                time.sleep(1)
                return
        for clave, val in self.cola.espacios_cola.items():
            if val == placa:
                print("\nEl vehículo con placa", placa, "está en la cola de espera en espacio", clave)
                time.sleep(1)
                return
        for clave, placa_calle in self.calle.items():
            if placa_calle == placa:
                print("\nEl vehículo con placa", placa, "está temporalmente en", clave)
                time.sleep(1)
                return
        print("\nEl vehículo con placa", placa, "no está en el parqueo, valet ni en la cola.")
        time.sleep(1)

    def ver_historial_por_placa(self, placa):
        if placa is None or placa.strip() == "":
            print("\nNo se puede consultar historial de una placa vacía.")
            time.sleep(1)
            return
        encontrados = self.historial.buscar_por_placa(placa)
        if not encontrados:
            print("\nNo se encontraron registros.")
            return
        Impresion.imprimir_historial(encontrados)
