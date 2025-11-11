import psycopg2
from psycopg2 import OperationalError, DatabaseError

# --- Configuración de la Conexión ---
CONFIG = {
    'user': 'postgres',       
    'password': 'sistemas2024',   
    'host': '192.168.56.101',           
    'port': '5432',                 
    'dbname': 'stardew'             
}

def list_stardew_tables(config):
    """
    Intenta conectar a la base de datos 'stardew' y lista todas sus tablas.
    """
    conn = None
    cursor = None
    
    db_name = config['dbname'] 
    
    try:
        print(f"Intentando conectar a la base de datos '{db_name}'...")
        
        conn = psycopg2.connect(
            user=config['user'], 
            password=config['password'], 
            host=config['host'], 
            port=config['port'],
            dbname=db_name
        )
        
        print(f"\n✅ ¡Conexión a la DB '{db_name}' exitosa!")
        
        cursor = conn.cursor()
        
        QUERY = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """
        
        cursor.execute(QUERY)
        
        tables = cursor.fetchall()
        
        print(f"\n **Tablas Encontradas en la Base de Datos '{db_name}':**")
        if tables:
            for (table_name,) in tables:
                print(f"* {table_name}")
        else:
            print(f"No se encontraron tablas en el esquema 'public' de la base de datos '{db_name}'.")

    except OperationalError as e:
        print(f"\n ¡Error de Conexión a PostgreSQL!")
        error_message = str(e)
        
        if "password authentication failed" in error_message:
            print("  - Error de autenticación. Verifica usuario y contraseña.")
        elif "could not connect to server" in error_message:
            print(f"  - No se pudo conectar al servidor. Host o Puerto incorrecto.")
        elif f'database "{db_name}" does not exist' in error_message:
            print(f"  - ¡La base de datos '{db_name}' no existe!")
            print("    Asegúrate de que la base de datos esté creada.")
        else:
            print(f"  - Error Operacional: {error_message}")
            
    except DatabaseError as e:
        print(f"\n ¡Error al ejecutar la consulta SQL! {e}")
            
    finally:
        if cursor:
            cursor.close()
        if conn:
            print("\nCerrando la conexión a PostgreSQL...")
            conn.close()
            print("Conexión cerrada.")

if __name__ == '__main__':

    list_stardew_tables(CONFIG)