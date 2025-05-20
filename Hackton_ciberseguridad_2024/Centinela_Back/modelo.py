# modelo_predictivo.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
from conexion_db import guardar_predicciones, conectar_bd

# Función para obtener los datos de las tablas necesarias
def obtener_datos():
    conexion = conectar_bd()

    consulta = """
    SELECT 
        d.edad_promedio, d.genero_predominante, d.nivel_educativo, d.nivel_socioeconomico, d.tasa_desempleo, d.densidad_poblacional,
        i.tipo_delito, i.gravedad, u.latitud, u.longitud, z.id_zona_riesgo, z.nivel_riesgo
    FROM
        Demografia d
        JOIN Incidente_Criminal i ON d.id_demografia = i.id_demografia
        JOIN Ubicacion u ON i.id_ubicacion = u.id_ubicacion
        JOIN Zona_Riesgo z ON i.id_zona_riesgo = z.id_zona_riesgo;
    """
    
    datos = pd.read_sql(consulta, conexion)
    conexion.close()
    
    return datos

# Codificación de variables categóricas
def codificar_datos(datos):
    label_encoder = LabelEncoder()

    datos['genero_predominante'] = label_encoder.fit_transform(datos['genero_predominante'])
    datos['nivel_educativo'] = label_encoder.fit_transform(datos['nivel_educativo'])
    datos['nivel_socioeconomico'] = label_encoder.fit_transform(datos['nivel_socioeconomico'])
    datos['tipo_delito'] = label_encoder.fit_transform(datos['tipo_delito'])
    datos['gravedad'] = label_encoder.fit_transform(datos['gravedad'])
    datos['nivel_riesgo'] = label_encoder.fit_transform(datos['nivel_riesgo'])
    
    return datos

# Entrenar el modelo y guardar las predicciones
def entrenar_modelo():
    datos = obtener_datos()
    datos_codificados = codificar_datos(datos)

    X = datos_codificados.drop(columns=['nivel_riesgo', 'id_zona_riesgo'])  # Variables predictoras
    Y = datos_codificados['nivel_riesgo']  # Variable objetivo
    zonas_riesgo = datos_codificados['id_zona_riesgo']  # Relación con zonas de riesgo

    # División de los datos en entrenamiento y prueba
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

    # Entrenamiento del modelo Random Forest
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, Y_train)

    # Predicción
    Y_pred = modelo.predict(X_test)
    prob_pred = modelo.predict_proba(X_test)[:, 1]  # Probabilidad de la predicción

    # Evaluación del modelo
    accuracy = accuracy_score(Y_test, Y_pred)
    print(f"Precisión del modelo: {accuracy * 100:.2f}%")
    print("Reporte de clasificación:")
    print(classification_report(Y_test, Y_pred))

    # Guardar el modelo entrenado
    with open('modelo_predictivo.pkl', 'wb') as archivo_modelo:
        pickle.dump(modelo, archivo_modelo)

    # Guardar las predicciones en la base de datos
    tipo_prediccion = ['robo'] * len(Y_pred)  # Tipo de predicción (por ejemplo, robo)
    guardar_predicciones(Y_pred, zonas_riesgo.values, prob_pred, tipo_prediccion)

# Ejecutar el proceso de entrenamiento y guardar predicciones
if __name__ == "__main__":
    entrenar_modelo()
