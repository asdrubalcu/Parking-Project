# clientes.py

# Cada cliente: nombre, apellido, telefono, correo (único), cedula (único)

class Cliente:
    def __init__(self, nombre, apellido, telefono, correo, cedula):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo = correo.lower()
        self.cedula = cedula

class ClientesManager:
    def __init__(self):
        # Almaceno por correo para búsquedas rápidas
        self._clientes_por_correo = {}
        # Índice por cédula para evitar duplicados
        self._cedulas = set()

    # Crear cliente: valida correo y cédula únicos
    def crear_cliente(self, nombre, apellido, telefono, correo, cedula):
        correo = correo.lower().strip()
        if correo in self._clientes_por_correo:
            return False, "Ya existe un usuario con ese correo registrado."
        if cedula in self._cedulas:
            return False, "Ya existe un usuario con esa cédula registrada."
        cliente = Cliente(nombre.strip(), apellido.strip(), telefono.strip(), correo, cedula.strip())
        self._clientes_por_correo[correo] = cliente
        self._cedulas.add(cedula)
        return True, cliente

    # Consultar por correo (devuelve cliente o None)
    def obtener_por_correo(self, correo):
        return self._clientes_por_correo.get(correo.lower().strip())

    # Modificar campos (todo menos correo). Devuelve (ok, mensaje)
    def modificar_por_correo(self, correo, nombre=None, apellido=None, telefono=None, cedula=None):
        correo = correo.lower().strip()
        c = self._clientes_por_correo.get(correo)
        if not c:
            return False, "Cliente no encontrado."
        # Si cambia la cédula, validar no duplicada
        if cedula and cedula != c.cedula:
            if cedula in self._cedulas:
                return False, "La cédula ya está registrada a otro cliente."
            # actualizar conjunto
            self._cedulas.remove(c.cedula)
            self._cedulas.add(cedula)
            c.cedula = cedula
        if nombre:
            c.nombre = nombre.strip()
        if apellido:
            c.apellido = apellido.strip()
        if telefono:
            c.telefono = telefono.strip()
        return True, c

    # Eliminar cliente por correo
    def eliminar_por_correo(self, correo):
        correo = correo.lower().strip()
        c = self._clientes_por_correo.pop(correo, None)
        if not c:
            return False, "Cliente no encontrado."
        if c.cedula in self._cedulas:
            self._cedulas.remove(c.cedula)
        return True, "Cliente eliminado."

    # Listar todos (útil para debug)
    def listar_todos(self):
        return list(self._clientes_por_correo.values())
