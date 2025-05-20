# preparar_datos_analisis.py

import pandas as pd
from sqlalchemy import create_engine

def conectar_db():
    try:
        # Cambia estos valores según tu configuración
        user = 'root'
        password = ''
        host = 'localhost'
        database = 'centinela'

        # Crear el motor de SQLAlchemy
        engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')
        return engine
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def obtener_datos_para_analisis():
    engine = conectar_db()
    if engine is None:
        return None

    try:
        query = """
        SELECT i.*, u.id_zona_riesgo
        FROM incidente_criminal i
        JOIN ubicacion u ON i.id_ubicacion = u.id_ubicacion
        JOIN zona_riesgo zr ON i.id_zona_riesgo = zr.id_zona_riesgo
        JOIN demografia d ON i.id_demografia = d.id_demografia
        """
        datos = pd.read_sql(query, engine)
        return datos
    except Exception as e:
        print(f"Error al obtener datos para análisis: {e}")
        return None
