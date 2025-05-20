import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime

# Conectar a la base de datos
def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            database='centinela',
            user='root',
            password=''
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            return conexion
    except Error as e:
        print(f"Error: {e}")
        return None

# Función para analizar datos y generar patrones criminales
def generar_patrones_criminales():
    conexion = conectar_bd()
    if conexion is None:
        return

    cursor = conexion.cursor()

    # Obtener datos de la tabla incidente_criminal
    cursor.execute("SELECT tipo_delito, id_zona_riesgo FROM Incidente_Criminal")
    resultados = cursor.fetchall()

    # Convertir resultados a DataFrame para análisis
    df = pd.DataFrame(resultados, columns=['tipo_delito', 'id_zona_riesgo'])

    # Identificar patrones: frecuencia de delitos por zona
    patrones = df.groupby(['id_zona_riesgo', 'tipo_delito']).size().reset_index(name='frecuencia')

    # Generar registros para la tabla patron_criminal
    for _, row in patrones.iterrows():
        id_zona_riesgo = row['id_zona_riesgo']
        descripcion_patron = f"Aumento de {row['frecuencia']} incidentes de {row['tipo_delito']} en la zona {id_zona_riesgo}"
        frecuencia = row['frecuencia']
        fecha_inicio = datetime.now()  # Aquí puedes ajustar según tus datos
        fecha_fin = None  # Puedes establecer esto si es necesario

        consulta_insert = """
        INSERT INTO Patron_Criminal (descripcion_patron, id_zona_riesgo, frecuencia, fecha_inicio, fecha_fin)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (descripcion_patron, id_zona_riesgo, frecuencia, fecha_inicio, fecha_fin)

        try:
            cursor.execute(consulta_insert, valores)
            print(f"Insertando patrón: {valores}")
        except Error as e:
            print(f"Error al insertar patrón: {e}")

    conexion.commit()
    cursor.close()
    conexion.close()
    print("Patrones criminales guardados exitosamente en la base de datos.")

# Ejecutar la función
generar_patrones_criminales()
