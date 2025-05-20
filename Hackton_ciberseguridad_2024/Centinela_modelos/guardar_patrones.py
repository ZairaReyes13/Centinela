# guardar_patrones.py

from sqlalchemy import create_engine
import pandas as pd

# Conexión a la base de datos
def conectar_db():
    try:
        user = 'root'
        password = ''
        host = 'localhost'
        database = 'centinela'
        engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')
        return engine
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Obtener datos para el análisis
# Obtener datos para el análisis
def obtener_datos_para_analisis():
    engine = conectar_db()
    if engine is None:
        return None

    try:
        query = """
        SELECT i.*, zr.id_zona_riesgo, zr.nombre_zona
        FROM incidente_criminal i
        JOIN zona_riesgo zr ON i.id_zona_riesgo = zr.id_zona_riesgo
        JOIN ubicacion u ON i.id_ubicacion = u.id_ubicacion
        JOIN demografia d ON i.id_demografia = d.id_demografia
        """
        datos = pd.read_sql(query, engine)
        return datos
    except Exception as e:
        print(f"Error al obtener datos para análisis: {e}")
        return None


# Función para detectar patrones
def detectar_patrones(datos):
    patrones_detectados = []

    # Analizar los datos para detectar patrones
    for index, fila in datos.iterrows():
        # Aquí agregas tu lógica para detectar patrones
        # Ejemplo: Si el tipo de delito es 'robo' en una zona de riesgo 'alto'
        if fila['tipo_delito'] == 'robo' and fila['nivel_riesgo'] == 'alto':
            patrones_detectados.append({
                'descripcion_patron': 'Aumento de robos en zona de alto riesgo',
                'id_zona_riesgo': fila['id_zona_riesgo'],
                'frecuencia': 1,  # Cambia según tu lógica
                'fecha_inicio': pd.to_datetime('today').date(),
                'temporalidad': 'diurno'  # Cambia según tu lógica
            })
    
    return patrones_detectados

# Guardar patrones en la base de datos
def guardar_patrones(patrones):
    engine = conectar_db()
    if engine is None:
        return

    for patron in patrones:
        try:
            query = """
            INSERT INTO patron_criminal (descripcion_patron, id_zona_riesgo, frecuencia, fecha_inicio, temporalidad)
            VALUES (%s, %s, %s, %s, %s)
            """
            with engine.connect() as connection:
                connection.execute(query, (
                    patron['descripcion_patron'],
                    patron['id_zona_riesgo'],
                    patron['frecuencia'],
                    patron['fecha_inicio'],
                    patron['temporalidad']
                ))
            print(f"Patrón guardado: {patron['descripcion_patron']}")
        except Exception as e:
            print(f"Error al guardar patrón: {e}")

# Función principal para realizar el análisis y guardar los patrones
def realizar_analisis_y_guardar():
    datos = obtener_datos_para_analisis()
    if datos is not None and not datos.empty:
        patrones = detectar_patrones(datos)
        if patrones:
            guardar_patrones(patrones)
        else:
            print("No se detectaron patrones.")
    else:
        print("No se obtuvieron datos para el análisis.")

# Ejemplo de uso
if __name__ == "__main__":
    realizar_analisis_y_guardar()
