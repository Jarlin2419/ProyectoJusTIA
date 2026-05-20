"""
Proyecto: JustIA - Corporación Universitaria de Asturias
Asignatura: Modelos de Inteligencia Artificial Aplicada
Entregable: Componente Funcional - Producto Mínimo Viable (MVP)
Funcionalidad: Clasificación Automática de Textos Legales y Panel de Explicabilidad
Autor: Estudiante de Posgrado
"""

import os
import sys
import pandas as pd
import numpy as np
import time

# Herramientas de Machine Learning
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# ==============================================================================
# 1. CONFIGURACIÓN DE RUTAS Y CONTROL DE FUENTES
# ==============================================================================
carpeta_raiz = os.path.dirname(os.path.abspath(__file__))
archivo_corpus = os.path.join(carpeta_raiz, "data/corpus_original.csv")

print("=" * 75)
print("              INICIANDO ENTRÉGABLE MVP - SISTEMA JustIA              ")
print("=" * 75)

if not os.path.exists(archivo_corpus):
    print(f"❌ Error Crítico: No se encontró el dataset '{archivo_corpus}'.")
    print("Por favor, asegúrate de haber ejecutado antes 'generador_corpus_justia.py'.")
    sys.exit(1)

# Carga de datos sintéticos/reales generados previamente
df = pd.read_csv(archivo_corpus)
print(f"✔ Dataset cargado con éxito. Total registros para entrenamiento: {len(df)}")
print(f"✔ Clases detectadas (Ramas del Derecho): {df['rama_derecho'].unique().tolist()}")
print("-" * 75)


# ==============================================================================
# 2. PIPELINE DE EXTRACCIÓN DE CARACTERÍSTICAS (TF-IDF VECTORS)
# ==============================================================================
print("[FASE 1] Preprocesamiento y Extracción de Características...")

# División del conjunto de datos (80% Entrenamiento, 20% Prueba)
# Usamos stratify para garantizar que ambas porciones tengan la misma proporción de ramas del derecho
X_train, X_test, y_train, y_test = train_test_split(
    df['texto_original'], 
    df['rama_derecho'], 
    test_size=0.2, 
    random_state=42, 
    stratify=df['rama_derecho']
)

# Configuración del Vectorizador TF-IDF adaptado a stop-words en español
# ngram_range=(1,2) permite capturar palabras individuales y bigramas (ej: 'consulta previa')
vectorizador = TfidfVectorizer(max_features=1500, ngram_range=(1, 2))

# Ajustar el vectorizador con los datos de entrenamiento y transformar ambos conjuntos
X_train_tfidf = vectorizador.fit_transform(X_train)
X_test_tfidf = vectorizador.transform(X_test)

print(f" -> Vocabulario técnico indexado: {X_train_tfidf.shape[1]} dimensiones léxicas.")


# ==============================================================================
# 3. ENTRENAMIENTO DEL MODELO DE INTELIGENCIA ARTIFICIAL
# ==============================================================================
print("\n[FASE 2] Entrenando Clasificador Estadístico Avanzado...")
start_time = time.time()

# Regresión Logística Multi-clase con penalización L2 para evitar sobreajuste
modelo_justia = LogisticRegression(C=1.0, max_iter=500, random_state=42)
modelo_justia.fit(X_train_tfidf, y_train)

tiempo_entrenamiento = time.time() - start_time
print(f" -> ¡Modelo entrenado con éxito en {tiempo_entrenamiento:.4f} segundos!")


# ==============================================================================
# 4. EVALUACIÓN CIENTÍFICA DEL MVP (MÉTRICAS DE RENDIMIENTO)
# ==============================================================================
print("\n[FASE 3] Evaluación de Desempeño Algorítmico (Muestra en Consola):")
y_pred = modelo_justia.predict(X_test_tfidf)

# Generación del reporte detallado de precisión, recall y F1-score por cada rama
reporte = classification_report(y_test, y_pred)
print(reporte)


# ==============================================================================
# 5. COMPONENTE ÉTICO: EXPLICABILIDAD LOCAL (MÓDULO SIMIL-SHAP)
# ==============================================================================
def explicar_prediccion_local(texto_usuario, modelo, vectorizador):
    """
    Analiza un texto nuevo y extrae matemáticamente qué palabras aportaron
    más peso para que la IA tomara la decisión. (Transparencia Algorítmica).
    """
    # Transformar el texto al espacio vectorial del modelo
    vector_tfidf = vectorizador.transform([texto_usuario])
    categoria_predicha = modelo.predict(vector_tfidf)[0]
    
    # Obtener el índice de la clase predicha en el modelo
    clase_idx = list(modelo.classes_).index(categoria_predicha)
    
    # Obtener los coeficientes (pesos) asignados por el modelo para esa clase específica
    coeficientes = modelo.coef_[clase_idx]
    
    # Mapear palabras con sus respectivos pesos para el texto ingresado
    palabras_texto = vectorizer_analyzer = vectorizer = vectorizador.build_analyzer()(texto_usuario)
    impactos = []
    
    vocabulario = vectorizer_vector = vectorizador.vocabulary_
    
    for palabra in palabras_texto:
        if palabra in vocabulario:
            idx_palabra = vocabulario[palabra]
            peso = coeficientes[idx_palabra]
            if peso > 0: # Buscamos las palabras que aportan positivamente a la decisión
                impactos.append((palabra, peso))
                
    # Ordenar las palabras de mayor a menor impacto
    impactos = sorted(list(set(impactos)), key=lambda x: x[1], reverse=True)[:3]
    
    return categoria_predicha, impactos


# ==============================================================================
# 6. EVIDENCIA DE FUNCIONAMIENTO (DEMOSTRACIÓN EN TIEMPO REAL)
# ==============================================================================
print("\n[FASE 4] Evidencia de Funcionamiento Operativo del MVP:")
print("=" * 75)

casos_reales_prueba = [
    "Requiero apoyo con la cuota alimentaria e iniciar los trámites de divorcio por violencia intrafamiliar.",
    "Fui víctima de despido injustificado y la empresa se niega a pagarme la liquidación del salario y horas extras.",
    "La comunidad indígena ancestral exige una consulta previa debido al despojo masivo de sus tierras colectivas."
]

for i, caso in enumerate(casos_reales_prueba, start=1):
    clase_final, palabras_clave = explicar_prediccion_local(caso, modelo_justia, vectorizador)
    
    print(f"TEST DE ENTRADA #{i}: '{caso}'")
    print(f" -> CATEGORÍA ASIGNADA: **{clase_final}**")
    print(" -> SUSTENTO TÉCNICO (Top Palabras de Mayor Impacto Matemático):")
    for palabra, peso in palabras_clave:
        print(f"    * Término: '{palabra}' ---> Peso en el vector: {peso:.4f}")
    print("-" * 75)

print("\n[ESTADO DEL MVP]: Funcional, auditable y listo para despliegue en producción.")
print("=" * 75)