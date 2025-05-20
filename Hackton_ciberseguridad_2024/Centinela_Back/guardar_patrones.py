# guardar_patrones.py
from conexion_db import conectar_bd
from modelo_Analitico import obtener_datos, analizar_patrones

def guardar_patrones(patrones):
    conexion = conectar_bd()
    if conexion is None:
        return

    cursor = conexion.cursor()

    try:
        for patron in patrones:
            consulta_insert = """
            INSERT INTO Patron_Criminal (descripcion_patron, id_zona_riesgo, frecuencia, fecha_inicio, fecha_fin, temporalidad)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (patron['descripcion_patron'], patron['id_zona_riesgo'], patron['frecuencia'], patron['fecha_inicio'], patron['fecha_fin'], patron['temporalidad'])
            cursor.execute(consulta_insert, valores)

        conexion.commit()
        print("Patrones guardados exitosamente en la base de datos.")
        
    except Error as e:
        print(f"Error al guardar patrones: {e}")
        conexion.rollback()
    finally:
        cursor.close()
        conexion.close()

if __name__ == "__main__":
    datos = obtener_datos()
    if datos is not None:
        patrones = analizar_patrones(datos)
        guardar_patrones(patrones)
