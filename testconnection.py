import psycopg2
from psycopg2 import OperationalError

# --- Configuración de la Conexión ---
CONFIG = {
    'user': 'postgres',       
    'password': 'sistemas2024',   
    'host': '192.168.56.101',          
    'port': '5432'                  

}

def test_postgresql_server_connection(config):
    """
    Intenta establecer una conexión al servidor PostgreSQL 
    usando la configuración proporcionada y reporta el resultado.
    """
    conn = None  
    try:
        # 1. Intentar la Conexión
        print(f"Intentando conectar al servidor PostgreSQL en host '{config['host']}'...")
        
        # psycopg2 usa 'password' y 'port' directamente en los argumentos de la función
        conn = psycopg2.connect(
            user=config['user'], 
            password=config['password'], 
            host=config['host'], 
            port=config['port']
        )
        
        # 2. Verificar si la conexión fue exitosa
        print("\n✅ ¡Conexión al servidor PostgreSQL exitosa!")
        print("El servidor está activo y tus credenciales son válidas.")
        
    # 3. Manejar Errores Específicos de PostgreSQL
    except OperationalError as e:
        print("\n❌ ¡Error de Conexión a PostgreSQL!")
        error_message = str(e)
        
        if "fe_sendauth: no password supplied" in error_message or "password authentication failed" in error_message:
            print("  - Error de autenticación. Verifica tu usuario y contraseña.")
        elif "could not connect to server" in error_message:
            print(f"  - No se pudo conectar al host '{config['host']}' o puerto '{config['port']}'. Asegúrate de que PostgreSQL esté corriendo y la configuración de red sea correcta.")
        else:
            print(f"  - Error operacional desconocido: {error_message}")
            
    # 4. Asegurar el Cierre de la Conexión
    finally:
        if conn is not None:
            print("\nCerrando la conexión a PostgreSQL...")
            conn.close()
            print("Conexión cerrada.")

if __name__ == '__main__':

    print("-----------------------------------------------")
    
    test_postgresql_server_connection(CONFIG)