import pandas as pd
import joblib
from sqlalchemy import create_engine

def conectar_db():
    try:
        engine = create_engine('mysql+pymysql://root:@localhost/centinela')
        print("Conexión exitosa a la base de datos")
        return engine
    except Exception as e:
        print(f"Error en la conexión a la base de datos: {e}")
        return None

def obtener_datos_para_prediccion(engine):
    query = "SELECT * FROM incidente_criminal"  # Ajusta la consulta según tus necesidades
    try:
        datos = pd.read_sql(query, engine)
        return datos
    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return None

def guardar_predicciones():
    try:
        # Cargar el modelo previamente entrenado
        modelo = joblib.load('modelo_entrenado.pkl')
        print("Modelo cargado con éxito.")
        
        # Conexión a la base de datos
        engine = conectar_db()
        if engine is None:
            return
        
        # Obtener los datos para predicciones
        datos = obtener_datos_para_prediccion(engine)
        
        if datos is None or datos.empty:
            print("No se obtuvieron datos para la predicción.")
            return
        
        print("Datos para predicción obtenidos con éxito.")
        print("Columnas disponibles en el DataFrame:", datos.columns.tolist())
        
        # Eliminar la columna 'tipo_delito' (objetivo) y cualquier columna que no sea necesaria
        if 'tipo_delito' in datos.columns:
            X = datos.drop(columns=['tipo_delito', 'fecha_incidente'])  # Asegúrate de eliminar columnas no necesarias
        else:
            X = datos
        
        # Convertir variables categóricas a numéricas
        X = pd.get_dummies(X, drop_first=True)
        
        print("Características generadas:", X.columns.tolist())
        
        # Asegúrate de que todas las características necesarias estén presentes
        required_features = [
            'descripcion_Asalto a un vehículo de reparto',
            'descripcion_Asalto en cajero automático',
            'descripcion_Daños a propiedad privada en zona residencial',
            'descripcion_Destrozos en una tienda de electrónica',
            'descripcion_Destrucción de bancos en parque de la ciudad',
            # Agrega otras características necesarias
        ]
        
        missing_features = [feature for feature in required_features if feature not in X.columns]
        if missing_features:
            print("Faltan las siguientes características:", missing_features)
            return  # O manejar de otra forma
        
        # Asegúrate de que X tenga las características requeridas
        X = X[required_features]
        
        # Realizar predicciones
        predicciones = modelo.predict(X)
        
        # Guardar las predicciones en la base de datos
        with engine.connect() as connection:
            for index, prediccion in enumerate(predicciones):
                query_update = "UPDATE incidente_criminal SET tipo_delito = %s WHERE id_incidente = %s"
                connection.execute(query_update, (prediccion, datos.iloc[index]['id_incidente']))
        
        print("Predicciones guardadas exitosamente.")
        
    except Exception as e:
        print(f"Error al obtener datos o guardar predicciones: {e}")
