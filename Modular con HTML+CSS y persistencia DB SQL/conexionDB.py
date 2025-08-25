# conexionDB.py

# Importo pyodbc para conexión con SQL Server
import pyodbc

class ConexionDB:
    def __init__(self, server="localhost\\SQLEXPRESS", database="parqueo"):
        # Defino el servidor SQL Server
        self._server = server
        # Defino la base de datos
        self._database = database
        # Creo variable para almacenar la conexión
        self._conn = None

    def conectar(self):
        # método para abrir la conexión hacia la base de datos
        try:
            self._conn = pyodbc.connect(
                "DRIVER={SQL Server};SERVER=" + self._server +
                ";DATABASE=" + self._database + ";Trusted_Connection=yes;"
            )
        except Exception as e:
            raise ConnectionError("No se pudo conectar a la base de datos: " + str(e))

    def cerrar(self):
        # Cierro la conexión si está abierta
        if self._conn:
            self._conn.close()
            self._conn = None

    def ejecutar(self, query, parametros=None):
        # Verifico que exista conexión antes de ejecutar
        if not self._conn:
            raise ValueError("No hay conexión abierta a la base de datos.")
        cursor = self._conn.cursor()
        if parametros:
            cursor.execute(query, parametros)
        else:
            cursor.execute(query)
        self._conn.commit()
        cursor.close()

    def consultar(self, query, parametros=None):
        # Verifico que exista conexión antes de ejecutar
        if not self._conn:
            raise ValueError("No hay conexión abierta a la base de datos.")
        cursor = self._conn.cursor()
        if parametros:
            cursor.execute(query, parametros)
        else:
            cursor.execute(query)
        resultado = cursor.fetchall()
        cursor.close()
        return resultado
