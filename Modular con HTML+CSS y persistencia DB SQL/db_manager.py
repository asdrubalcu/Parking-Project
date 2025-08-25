# db_manager.py


from conexionDB import ConexionDB
from vehiculo import Vehiculo

class DbManager:
    def __init__(self, server="localhost\\SQLEXPRESS", database="parqueo"):
        self.conn = ConexionDB(server=server, database=database)
        self.conn.conectar()
        #Se crea el esquema de tablas en caso de que no exista
        self._crear_tablas()

    def _crear_tablas(self):
        # Se crean las tablas principales: Vehículos, espacios para autos y motos, valet, cola, calle, historial y configuración
        queries = []

        queries.append("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Vehiculos' AND xtype='U')
        CREATE TABLE Vehiculos (
            Placa VARCHAR(20) PRIMARY KEY,
            Tipo VARCHAR(10),
            Marca VARCHAR(100),
            Modelo VARCHAR(100),
            Color VARCHAR(50)
        )
        """)

        queries.append("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='EspaciosAutos' AND xtype='U')
        CREATE TABLE EspaciosAutos (
            Clave VARCHAR(10) PRIMARY KEY,
            Placa VARCHAR(20) NULL
        )
        """)

        queries.append("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='EspaciosMotos' AND xtype='U')
        CREATE TABLE EspaciosMotos (
            Clave VARCHAR(10) PRIMARY KEY,
            Placa VARCHAR(20) NULL
        )
        """)

        queries.append("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='EspaciosValet' AND xtype='U')
        CREATE TABLE EspaciosValet (
            Clave VARCHAR(10) PRIMARY KEY,
            Placa VARCHAR(20) NULL
        )
        """)

        queries.append("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ValetOrder' AND xtype='U')
        CREATE TABLE ValetOrder (
            Pos INT PRIMARY KEY,
            Placa VARCHAR(20)
        )
        """)

        queries.append("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='EspaciosCola' AND xtype='U')
        CREATE TABLE EspaciosCola (
            Clave VARCHAR(10) PRIMARY KEY,
            Placa VARCHAR(20) NULL
        )
        """)

        queries.append("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ColaOrder' AND xtype='U')
        CREATE TABLE ColaOrder (
            Pos INT PRIMARY KEY,
            Placa VARCHAR(20)
        )
        """)

        queries.append("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Calle' AND xtype='U')
        CREATE TABLE Calle (
            Clave VARCHAR(20) PRIMARY KEY,
            Placa VARCHAR(20) NULL,
            OrigSlot VARCHAR(20) NULL
        )
        """)

        queries.append("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Historial' AND xtype='U')
        CREATE TABLE Historial (
            Id INT IDENTITY(1,1) PRIMARY KEY,
            Placa VARCHAR(20),
            Tipo VARCHAR(10),
            Marca VARCHAR(100),
            Modelo VARCHAR(100),
            Color VARCHAR(50),
            HoraEntrada DATETIME,
            HoraSalida DATETIME,
            TotalPagado FLOAT,
            Ubicacion VARCHAR(50)
        )
        """)

        queries.append("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Config' AND xtype='U')
        CREATE TABLE Config (
            [Key] VARCHAR(50) PRIMARY KEY,
            [Value] VARCHAR(200)
        )
        """)

        for q in queries:
            try:
                self.conn.ejecutar(q)
            except Exception as e:
                # No interrumpo el proceso en caso de que la tabla ya exista o no haya permisos
                pass

    # Se guarda el estado completo del parqueo

    def save_state(self, parqueo):
        
        # Guarda las estructuras principales del objeto parqueo.

        # Vehiculos conocidos
        self._save_vehiculos(parqueo.placas_conocidas)

        # Espacios autos
        self._save_espacios_table("EspaciosAutos", parqueo.espacios.espacios_autos)

        # Espacios motos
        self._save_espacios_table("EspaciosMotos", parqueo.espacios.espacios_motos)

        # Valet (espacios y orden)
        self._save_espacios_table("EspaciosValet", parqueo.valet.espacios_valet)
        self._save_valet_order(parqueo.valet.valet_autos)

        # Cola (espacios y orden)
        self._save_espacios_table("EspaciosCola", parqueo.cola.espacios_cola)
        self._save_cola_order(parqueo.cola.cola_espera_autos)

        # Calle
        self._save_calle(parqueo.calle, parqueo.calle_objs)

        # Config (cantidad espacios actuales)
        cfg = {
            "cantidad_espacios_autos": str(parqueo.configuracion.cantidad_espacios_autos),
            "cantidad_espacios_motos": str(parqueo.configuracion.cantidad_espacios_motos),
            "cobro_fraccionado": "1" if parqueo.configuracion.cobro_fraccionado else "0"
        }
        self._save_config(cfg)

    def _save_vehiculos(self, placas_conocidas):
        # Se reinicia la tabla Vehículos eliminando todo el contenido y registrando nuevamente los datos
        try:
            self.conn.ejecutar("DELETE FROM Vehiculos")
        except Exception:
            pass
        for placa, datos in placas_conocidas.items():
            q = "INSERT INTO Vehiculos (Placa, Tipo, Marca, Modelo, Color) VALUES (?, ?, ?, ?, ?)"
            params = (placa, datos.get("tipo"), datos.get("marca"), datos.get("modelo"), datos.get("color"))
            self.conn.ejecutar(q, params)

    def _save_espacios_table(self, table, dict_esp):
        # Se eliminan los registros de la tabla y se vuelven a insertar las claves y placas correspondientes
        try:
            self.conn.ejecutar(f"DELETE FROM {table}")
        except Exception:
            pass
        for clave in sorted(dict_esp.keys()):
            placa = dict_esp[clave]
            q = f"INSERT INTO {table} (Clave, Placa) VALUES (?, ?)"
            self.conn.ejecutar(q, (clave, placa))

    def _save_valet_order(self, valet_list):
        # La lista de valet Vehículos en el orden en que ingresaron (último en entrar es el primero en salir)
        try:
            self.conn.ejecutar("DELETE FROM ValetOrder")
        except Exception:
            pass
        pos = 1
        for v in valet_list:
            placa = v.placa
            self.conn.ejecutar("INSERT INTO ValetOrder (Pos, Placa) VALUES (?, ?)", (pos, placa))
            pos += 1

    def _save_cola_order(self, cola_list):
        try:
            self.conn.ejecutar("DELETE FROM ColaOrder")
        except Exception:
            pass
        pos = 1
        for v in cola_list:
            placa = v.placa
            self.conn.ejecutar("INSERT INTO ColaOrder (Pos, Placa) VALUES (?, ?)", (pos, placa))
            pos += 1

    def _save_calle(self, calle_dict, calle_objs):
        try:
            self.conn.ejecutar("DELETE FROM Calle")
        except Exception:
            pass
        for clave, placa in calle_dict.items():
            orig = None
            if calle_objs and calle_objs.get(clave):
                orig = calle_objs.get(clave).get("orig")
            self.conn.ejecutar("INSERT INTO Calle (Clave, Placa, OrigSlot) VALUES (?, ?, ?)", (clave, placa, orig))

    def _save_config(self, cfg_dict):
        try:
            self.conn.ejecutar("DELETE FROM Config")
        except Exception:
            pass
        for k, v in cfg_dict.items():
            self.conn.ejecutar("INSERT INTO Config ([Key], [Value]) VALUES (?, ?)", (k, v))

    # Se carga el estado del parqueo al iniciar la aplicación
    def load_state(self, parqueo):
        # Carga el estado desde la BD y lo asigna en el objeto parqueo en memoria.

        # Vehiculos conocidos
        filas = self.conn.consultar("SELECT Placa, Tipo, Marca, Modelo, Color FROM Vehiculos")
        placas = {}
        for f in filas:
            placas[f[0]] = {"tipo": f[1], "marca": f[2], "modelo": f[3], "color": f[4]}
        parqueo.placas_conocidas = placas

        # Espacios autos
        filas = self.conn.consultar("SELECT Clave, Placa FROM EspaciosAutos ORDER BY Clave")
        if filas:
            parqueo.espacios.espacios_autos = {f[0]: f[1] for f in filas}
        # Si no hay registros se construye según configuración actual
        else:
            parqueo.espacios.actualizar_espacios()

        # Espacios motos
        filas = self.conn.consultar("SELECT Clave, Placa FROM EspaciosMotos ORDER BY Clave")
        if filas:
            parqueo.espacios.espacios_motos = {f[0]: f[1] for f in filas}

        # Valet: espacios + orden
        filas = self.conn.consultar("SELECT Clave, Placa FROM EspaciosValet ORDER BY Clave")
        if filas:
            parqueo.valet.espacios_valet = {f[0]: f[1] for f in filas}
        filas = self.conn.consultar("SELECT Pos, Placa FROM ValetOrder ORDER BY Pos")
        valet_list = []
        for f in filas:
            placa = f[1]
            # Se reconstruye el objeto Vehículo usando los datos conocidos de la placa; si no existen datos se asigna el tipo 'auto'
            datos = parqueo.placas_conocidas.get(placa, {})
            v = Vehiculo(placa, datos.get("tipo", "auto"))
            v.marca = datos.get("marca")
            v.modelo = datos.get("modelo")
            v.color = datos.get("color")
            valet_list.append(v)
        if valet_list:
            parqueo.valet.valet_autos = valet_list

        # Cola: espacios + orden
        filas = self.conn.consultar("SELECT Clave, Placa FROM EspaciosCola ORDER BY Clave")
        if filas:
            parqueo.cola.espacios_cola = {f[0]: f[1] for f in filas}
        filas = self.conn.consultar("SELECT Pos, Placa FROM ColaOrder ORDER BY Pos")
        cola_list = []
        for f in filas:
            placa = f[1]
            datos = parqueo.placas_conocidas.get(placa, {})
            v = Vehiculo(placa, datos.get("tipo", "auto"))
            v.marca = datos.get("marca")
            v.modelo = datos.get("modelo")
            v.color = datos.get("color")
            cola_list.append(v)
        if cola_list:
            parqueo.cola.cola_espera_autos = cola_list

        # Calle
        filas = self.conn.consultar("SELECT Clave, Placa, OrigSlot FROM Calle ORDER BY Clave")
        for f in filas:
            clave, placa, orig = f[0], f[1], f[2]
            parqueo.calle[clave] = placa
            if placa:
                datos = parqueo.placas_conocidas.get(placa, {})
                v = Vehiculo(placa, datos.get("tipo", "auto"))
                v.marca = datos.get("marca")
                v.modelo = datos.get("modelo")
                v.color = datos.get("color")
                parqueo.calle_objs[clave] = {"veh": v, "orig": orig}
            else:
                parqueo.calle_objs[clave] = None

        # Se cargan los valores de configuración si existen, solo con las cantidades disponibles
        filas = self.conn.consultar("SELECT [Key], [Value] FROM Config")
        for f in filas:
            k, v = f[0], f[1]
            if k == "cantidad_espacios_autos":
                try:
                    parqueo.configuracion.cantidad_espacios_autos = int(v)
                except:
                    pass
            if k == "cantidad_espacios_motos":
                try:
                    parqueo.configuracion.cantidad_espacios_motos = int(v)
                except:
                    pass
            if k == "cobro_fraccionado":
                parqueo.configuracion.cobro_fraccionado = (v == "1")

        # Si no existen datos en las tablas principales, inicializa la estructura acutal
        parqueo.espacios.actualizar_espacios()

   
    def insert_historial(self, registro):
        # Inserta el rgistro al momento de la Salida en la tabla Historial.

        q = """
        INSERT INTO Historial (Placa, Tipo, Marca, Modelo, Color, HoraEntrada, HoraSalida, TotalPagado, Ubicacion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        marca = getattr(registro, "marca", None)
        modelo = getattr(registro, "modelo", None)
        color = getattr(registro, "color", None)
        hora_entrada = registro.hora_entrada if registro.hora_entrada else None
        hora_salida = registro.hora_salida if registro.hora_salida else None
        total = getattr(registro, "total_pagado", None)
        ubic = getattr(registro, "ubicacion", None) if hasattr(registro, "ubicacion") else None
        self.conn.ejecutar(q, (registro.placa, registro.tipo, marca, modelo, color, hora_entrada, hora_salida, total, ubic))

    # Cerrar conexión
    def close(self):
        self.conn.cerrar()
