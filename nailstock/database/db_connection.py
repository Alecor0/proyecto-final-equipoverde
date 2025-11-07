import sqlite3
import os

class DBConnection:
    def __init__(self, db_name="nailstack.db"):
        """
        Inicializa la conexión a la base de datos.
        Verifica si la base de datos existe, si no, la crea y ejecuta create_tables.sql
        """
        self.db_name = db_name
        self.connection = None
        
        # Verificar si la base de datos existe
        if not os.path.exists(self.db_name):
            print(f"La base de datos {self.db_name} no existe. Creándola...")
            self.create_tables()
        else:
            print(f"La base de datos {self.db_name} ya existe.")
            self.get_connection()
    
    def create_tables(self):
        """
        Ejecuta las sentencias SQL del archivo create_tables.sql
        """
        try:
            # Crear conexión (esto creará el archivo .db si no existe)
            self.connection = sqlite3.connect(self.db_name)
            cursor = self.connection.cursor()
            
            # Verificar si el archivo create_tables.sql existe
            if not os.path.exists("create_tables.sql"):
                print("Error: El archivo create_tables.sql no existe.")
                return
            
            # Leer y ejecutar el archivo SQL
            with open("create_tables.sql", "r") as sql_file:
                sql_script = sql_file.read()
            
            # Ejecutar cada sentencia SQL por separado
            cursor.executescript(sql_script)
            self.connection.commit()
            
            print("Tablas creadas exitosamente!")
            
        except sqlite3.Error as e:
            print(f"Error al crear las tablas: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        finally:
            if self.connection:
                self.connection.close()
    
    def get_connection(self):
        """
        Devuelve la conexión activa a la base de datos con claves foráneas habilitadas
        """
        try:
            if self.connection is None:
                self.connection = sqlite3.connect(self.db_name)
                
                # Habilitar claves foráneas
                cursor = self.connection.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")
                self.connection.commit()
                
            return self.connection
            
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            return None

# Instancia global de la conexión
_db_connection = DBConnection()

def get_db_connection():
    """
    Función global para obtener la conexión a la base de datos
    """
    return _db_connection.get_connection()

# Prueba de conexión al ejecutar el archivo directamente
if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        print("✅ Conexión a la base de datos establecida correctamente!")
        conn.close()
    else:
        print("❌ Error al conectar con la base de datos")