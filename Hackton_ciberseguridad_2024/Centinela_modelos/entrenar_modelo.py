# entrenar_modelo.py
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
from sqlalchemy import create_engine
import pymysql

# Configuración de la conexión a la base de datos
usuario = 'root'
contrasena = ''
host = 'localhost'
base_de_datos = 'centinela'

# Crear el motor de SQLAlchemy
conexion = create_engine(f'mysql+pymysql://{usuario}:{contrasena}@{host}/{base_de_datos}')

def entrenar_modelo():
    query = "SELECT * FROM incidente_criminal"
    
    try:
        # Obtén los datos usando pandas
        datos = pd.read_sql(query, conexion)
        print("Datos obtenidos con éxito.")
        
        # Identificar columnas de tipo datetime
        columnas_datetime = datos.select_dtypes(include=['datetime64']).columns
        
        # Convertir las columnas de datetime en variables numéricas (por ejemplo, año, mes, día)
        for columna in columnas_datetime:
            datos[columna + '_year'] = datos[columna].dt.year
            datos[columna + '_month'] = datos[columna].dt.month
            datos[columna + '_day'] = datos[columna].dt.day
        
        # Eliminar las columnas originales de tipo datetime
        datos = datos.drop(columns=columnas_datetime)
        
        # Separar las características (X) y la variable objetivo (y)
        X = datos.drop(columns=['tipo_delito'])  # Suponiendo que 'tipo_delito' es la columna objetivo
        y = datos['tipo_delito']
        
        # Convertir las variables categóricas en variables numéricas
        X = pd.get_dummies(X, drop_first=True)
        print("Variables categóricas convertidas a numéricas.")
        
        # Dividir los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Entrenar el modelo
        modelo = LogisticRegression(max_iter=1000)  # Aumentar el número de iteraciones si es necesario
        modelo.fit(X_train, y_train)

        # Guardar el modelo entrenado
        joblib.dump(modelo, 'modelo_entrenado.pkl')
        print("Modelo guardado como 'modelo_entrenado.pkl'.")

        # Guardar las características del modelo
        características = X.columns.tolist()
        pd.Series(características).to_csv('features.csv', index=False)  # Guardar características en un archivo CSV
        print("Características del modelo guardadas como 'features.csv'.")

    except Exception as e:
        print(f"Error al obtener datos: {e}")

def guardar_predicciones():
    try:
        # Cargar el modelo previamente entrenado
        modelo = joblib.load('modelo_entrenado.pkl')
        print("Modelo cargado con éxito.")
        
        # Obtener datos para la predicción
        query = "SELECT * FROM incidente_criminal WHERE tipo_delito IS NULL"  # Obtener datos sin predicciones
        datos = pd.read_sql(query, conexion)

        if datos.empty:
            print("No se obtuvieron datos para la predicción.")
            return
        
        # Convertir las columnas de datetime en variables numéricas
        columnas_datetime = datos.select_dtypes(include=['datetime64']).columns
        for columna in columnas_datetime:
            datos[columna + '_year'] = datos[columna].dt.year
            datos[columna + '_month'] = datos[columna].dt.month
            datos[columna + '_day'] = datos[columna].dt.day
        
        # Eliminar las columnas originales de tipo datetime
        datos = datos.drop(columns=columnas_datetime)

        # Preparar las características para la predicción
        X = datos.drop(columns=['tipo_delito', 'fecha_incidente'])  # Asegúrate de que estas columnas estén presentes
        X = pd.get_dummies(X, drop_first=True)

        # Cargar características esperadas desde el archivo CSV
        características_esperadas = pd.read_csv('features.csv').squeeze().tolist()
        
        # Asegurarse de que todas las características esperadas estén presentes en X
        for feature in características_esperadas:
            if feature not in X.columns:
                X[feature] = 0  # Agregar columna con ceros si falta
        X = X[características_esperadas]  # Reordenar las columnas

        # Realizar predicciones
        predicciones = modelo.predict(X)

        # Guardar las predicciones en la base de datos
        with conexion.connect() as connection:
            for index, prediccion in enumerate(predicciones):
                query = "UPDATE incidente_criminal SET tipo_delito = %s WHERE id_incidente = %s"
                connection.execute(query, (prediccion, datos.iloc[index]['id_incidente']))

        print("Predicciones guardadas exitosamente.")
    
    except Exception as e:
        print(f"Error al guardar predicciones: {e}")

if __name__ == "__main__":
    entrenar_modelo()
    guardar_predicciones()
