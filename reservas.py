# reservas.py

from datetime import datetime, timedelta

# Clase simple que representa una reserva
class Reserva:
    def __init__(self, usuario_correo, placa, tipo, fecha_ingreso): 
        # fecha_ingreso -> datetime completo
        self.usuario_correo = usuario_correo.lower().strip()
        self.placa = placa.strip().upper()
        self.tipo = tipo
        self.fecha_ingreso = fecha_ingreso
        self.estado = "activa"  # activa, usada, cancelada

class ReservasManager:
    def __init__(self):
        # Lista de reservas en memoria
        self._reservas = []

    # Crear reserva: valida condiciones, devuelve (ok, mensaje/obj)
    def crear_reserva(self, usuario_correo, placa, tipo, fecha_ingreso, parqueo):
        usuario_correo = usuario_correo.lower().strip()
        placa = placa.strip().upper()

        # Validar fecha mínima: 1 hora desde ahora
        ahora = datetime.now()
        if fecha_ingreso < ahora + timedelta(hours=1):
            return False, "La fecha/hora de ingreso debe ser al menos 1 hora desde ahora."

        # Validar que la placa no esté ya en parqueo
        if placa in parqueo.vehiculos_dentro:
            return False, "La placa ya está en el parqueo."

        # Validar que no exista otra reserva activa para la misma placa
        for r in self._reservas:
            if r.placa == placa and r.estado == "activa":
                return False, "Ya existe una reserva activa para esa placa."

        # Crea Reserva
        reserva = Reserva(usuario_correo, placa, tipo, fecha_ingreso)
        self._reservas.append(reserva)
        return True, reserva

    # Buscar reserva activa por placa (devuelve primera activa o None)
    def buscar_activa_por_placa(self, placa):
        placa = placa.strip().upper()
        for r in self._reservas:
            if r.placa == placa and r.estado == "activa":
                return r
        return None

    # Buscar reservas activas por usuario (correo)
    def buscar_activas_por_usuario(self, correo):
        correo = correo.lower().strip()
        return [r for r in self._reservas if r.usuario_correo == correo and r.estado == "activa"]

    # Modificar fecha/hora de reserva por placa (solo fecha_ingreso)
    def modificar_fecha_por_placa(self, placa, nueva_fecha):
        r = self.buscar_activa_por_placa(placa)
        if not r:
            return False, "No existe reserva activa para esa placa."
        # validar mínimo 1 hora desde ahora
        from datetime import datetime, timedelta
        if nueva_fecha < datetime.now() + timedelta(hours=1):
            return False, "La nueva fecha/hora debe ser al menos 1 hora desde ahora."
        r.fecha_ingreso = nueva_fecha
        return True, r

    # Eliminar (cancelar) reserva por placa
    def eliminar_por_placa(self, placa):
        r = self.buscar_activa_por_placa(placa)
        if not r:
            return False, "No existe reserva activa para esa placa."
        r.estado = "cancelada"
        return True, "Reserva cancelada."

    # Marcar reserva usada cuando llega el vehículo
    def marcar_usada_por_placa(self, placa):
        r = self.buscar_activa_por_placa(placa)
        if not r:
            return False, "No existe reserva activa para esa placa."
        r.estado = "usada"
        return True, r

    # Opcional: listar reservas activas (debug)
    def listar_activas(self):
        return [r for r in self._reservas if r.estado == "activa"]
