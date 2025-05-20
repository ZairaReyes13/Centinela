# preparar_datos.py
import pandas as pd
import pymysql

def conectar_db():
    try:
        conexion = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='centinela'
        )
        print("Conexión exitosa a la base de datos")
        return conexion
    except Exception as e:
        print(f"Error en la conexión a la base de datos: {e}")
        return None

def preparar_datos():
    conexion = conectar_db()
    if conexion is None:
        return None
    
    # Aquí puedes implementar la lógica para preparar y limpiar los datos
    # Por ejemplo, asegurarte de que no haya valores nulos en las columnas relevantes
    query = "SELECT * FROM incidente_criminal"
    datos = pd.read_sql(query, conexion)

    # Realiza cualquier procesamiento necesario
    # ...

    return datos

if __name__ == "__main__":
    preparar_datos()
