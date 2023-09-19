import mysql.connector

class MySQLDatabase:
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos")
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")

    def execute_query(self, query, data=None):
        if not self.connection:
            print("No hay conexión a la base de datos. Primero, realiza una conexión.")
            return False

        cursor = self.connection.cursor()
        try:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            self.connection.commit()  # ¡Importante para confirmar la inserción!
            return True
        except mysql.connector.Error as err:
            print(f"Error al ejecutar la consulta: {err}")
            self.connection.rollback()  # Revertir cualquier cambio si ocurre un error
            return False
        finally:
            cursor.close()

    def close(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada")