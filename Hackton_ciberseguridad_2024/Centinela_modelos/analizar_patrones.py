import pandas as pd
from datetime import datetime
import numpy as np
from preparar_datos_analisis import obtener_datos_para_analisis, conectar_db

# Función para detectar patrones criminales
def detectar_patrones(datos):
    patrones_detectados = []
    for index, fila in datos.iterrows():
        if fila['nivel_riesgo'] == 'alto' and fila['gravedad'] == 'grave':
            descripcion_patron = f"Aumento de {fila['tipo_delito']} en zonas de alto riesgo."
            patrones_detectados.append({
                'descripcion_patron': descripcion_patron,
                'id_zona_riesgo': index + 1,
                'frecuencia': np.random.randint(5, 15),
                'fecha_inicio': datetime.now().date(),
                'fecha_fin': None,
                'temporalidad': 'nocturno'
            })
    return patrones_detectados

# Función para guardar los patrones en la base de datos
def guardar_patrones(patrones):
    conexion = conectar_db()
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return
    try:
        with conexion.cursor() as cursor:
            for patron in patrones:
                sql = """
                INSERT INTO patron_criminal (descripcion_patron, id_zona_riesgo, frecuencia, fecha_inicio, fecha_fin, temporalidad)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    patron['descripcion_patron'], 
                    patron['id_zona_riesgo'], 
                    patron['frecuencia'], 
                    patron['fecha_inicio'], 
                    patron['fecha_fin'], 
                    patron['temporalidad']
                ))
        conexion.commit()
        print("Patrones guardados exitosamente.")
    except Exception as e:
        print(f"Error al guardar patrones: {e}")
    finally:
        conexion.close()

# Función principal para realizar el análisis
def realizar_analisis_y_guardar():
    datos = obtener_datos_para_analisis()
    if datos is not None:
        patrones = detectar_patrones(datos)
        if patrones:
            guardar_patrones(patrones)
        else:
            print("No se detectaron patrones.")
    else:
        print("No se pudieron obtener los datos.")
