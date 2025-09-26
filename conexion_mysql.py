import mysql.connector
from mysql.connector import errorcode


# Configuración de la conexión a la base de datos
DB_CONFIG = {
    'user': 'sql5799726',
    'password': '4ULUABLR5l',
    'host': 'sql5.freesqldatabase.com',
    'database': 'sql5799726'
}

# Definición de las sentencias SQL para crear las tablas
TABLES = {}


TABLES ['contries'] = (
    "CREATE TABLE `countries` ("
    " `id` INT AUTO_INCREMENT,"
    "`country_name` VARCHAR(100) UNIQUE NOT NULL,"
    "`iso_code` CHAR(3) UNIQUE,"
    " PRIMARY KEY (id)"
    ")ENGINE=InnoDB"
)




# 1. Establecer la conexión y crear un cursor
try:
    cnn = mysql.connector.connect(**DB_CONFIG)
    cursor = cnn.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        print("La base de datos no existe.")
    elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Usuario o contraseña incorrectos.")
    else:
        print(f"Error de conexión: {err}")
    exit()

# 2. Iterar y ejecutar las sentencias de creación de tablas
def create_tables():
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print(f"Creando tabla {table_name}: ", end='')
            cursor.execute(table_description)
            print("OK")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("ya existe.")
            else:
                print(f"Error al crear tabla: {err.msg}")

# Llamar a la función para crear las tablas
create_tables()

# 3. Cerrar el cursor y la conexión
cursor.close()
cnn.close()

