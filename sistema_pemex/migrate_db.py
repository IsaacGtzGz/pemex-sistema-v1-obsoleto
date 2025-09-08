"""
Script para migrar la base de datos a la nueva estructura
"""
import mysql.connector
from mysql.connector import Error

def migrate_database():
    try:
        # Conectar a la base de datos
        connection = mysql.connector.connect(
            host='localhost',
            database='sistema_pemex',
            user='root',
            password='root'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            print("Conectado a MySQL Server versión ", connection.get_server_info())
            
            # Verificar estructura actual
            cursor.execute("DESCRIBE usuarios")
            columns = cursor.fetchall()
            existing_columns = [col[0] for col in columns]
            print(f"Columnas existentes: {existing_columns}")
            
            # Agregar columnas faltantes
            new_columns = [
                ("nombre", "VARCHAR(100) NOT NULL DEFAULT ''"),
                ("apellido_paterno", "VARCHAR(100) NOT NULL DEFAULT ''"),
                ("apellido_materno", "VARCHAR(100) NULL"),
                ("telefono", "VARCHAR(20) NULL"),
                ("puesto", "VARCHAR(150) NULL")
            ]
            
            for column_name, column_definition in new_columns:
                if column_name not in existing_columns:
                    try:
                        alter_query = f"ALTER TABLE usuarios ADD COLUMN {column_name} {column_definition}"
                        cursor.execute(alter_query)
                        print(f"✓ Columna {column_name} agregada exitosamente")
                    except Error as e:
                        print(f"✗ Error agregando columna {column_name}: {e}")
            
            # Actualizar usuarios existentes con datos básicos
            cursor.execute("SELECT id, username FROM usuarios")
            usuarios = cursor.fetchall()
            
            for user_id, username in usuarios:
                if username == 'admin':
                    update_query = """
                    UPDATE usuarios 
                    SET nombre='Administrador', apellido_paterno='Sistema', puesto='Administrador General'
                    WHERE id = %s
                    """
                    cursor.execute(update_query, (user_id,))
                elif 'capturista' in username:
                    update_query = """
                    UPDATE usuarios 
                    SET nombre='Usuario', apellido_paterno='Capturista', puesto='Capturista de Datos'
                    WHERE id = %s
                    """
                    cursor.execute(update_query, (user_id,))
                else:
                    update_query = """
                    UPDATE usuarios 
                    SET nombre='Usuario', apellido_paterno='Sistema', puesto='Usuario General'
                    WHERE id = %s
                    """
                    cursor.execute(update_query, (user_id,))
            
            connection.commit()
            print("✓ Migración completada exitosamente")
            
    except Error as e:
        print(f"Error durante la migración: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión MySQL cerrada")

if __name__ == "__main__":
    migrate_database()
