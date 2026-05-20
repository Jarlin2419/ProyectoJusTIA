"""
Proyecto: JustIA - Corporación Universitaria de Asturias
Actividad 1: Preprocesamiento de Corpus Jurídico desde Fuente Externa (CSV)
Autor: Estudiante de Posgrado
"""

import pandas as pd
import re
import unicodedata
import os
import spacy

def cargar_modelo_spacy():
    """Carga el modelo de procesamiento de lenguaje en español de spaCy."""
    try:
        return spacy.load("es_core_news_sm")
    except OSError:
        raise OSError("Por favor, descarga el modelo ejecutando: python -m spacy download es_core_news_sm")

def limpiar_texto_base(texto):
    """
    Realiza la limpieza básica de texto conservando la estructura lingüística del español.
    Remueve tildes de forma segura, elimina caracteres especiales y números.
    """
    if not isinstance(texto, str):
        return ""
    
    # 1. Conversión a minúsculas
    texto = texto.lower()
    
    # 2. Eliminación de tildes respetando la 'ñ' y caracteres Unicode latinos
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn' or c in ['\u0303']
    )
    texto = unicodedata.normalize('NFC', texto)
    
    # 3. Remover números
    texto = re.sub(r'\d+', '', texto)
    
    # 4. Remover símbolos y puntuación (mantiene ñ y espacios)
    texto = re.sub(r'[^a-zñáéíóúü\s]', '', texto)
    
    # 5. Eliminar espacios múltiples
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto

def procesar_nlp_juridico(texto, nlp_model):
    """
    Aplica tokenización, remoción de stopwords personalizadas y lematización
    utilizando spaCy.
    """
    if not texto:
        return ""
    
    doc = nlp_model(texto)
    tokens_procesados = []
    
    for token in doc:
        palabra = token.text
        
        # Excepción de stopword para el entorno legal de JustIA
        if token.is_stop and palabra != 'no':
            continue
            
        if not token.text.strip():
            continue
            
        # Extraer la forma base (lema)
        tokens_procesados.append(token.lemma_)
        
    return " ".join(tokens_procesados)


# ==========================================
# FLUJO PRINCIPAL DE EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    archivo_entrada = 'data/corpus_original.csv'
    archivo_salida = 'data/corpus_justia_limpio.csv'
    
    # Verificación de la existencia de la fuente de datos externa
    if not os.path.exists(archivo_entrada):
        raise FileNotFoundError(
            f"No se encontró el archivo '{archivo_entrada}'. "
            f"Por favor, asegúrate de crearlo en el mismo directorio que este script."
        )
        
    print(f"Cargando datos desde: {archivo_entrada}...")
    # Leer el archivo CSV externo
    df_justia = pd.read_csv(archivo_entrada)
    
    print("Inicializando componentes de NLP...")
    nlp = cargar_modelo_spacy()
    
    # Procesamiento por fases
    print("Ejecutando Fase 1: Normalización de texto y remoción de caracteres...")
    df_justia['texto_limpieza_base'] = df_justia['texto_original'].apply(limpiar_texto_base)
    
    print("Ejecutando Fase 2: Lematización y filtrado de stopwords legal...")
    df_justia['texto_limpio_lematizado'] = df_justia['texto_limpieza_base'].apply(
        lambda x: procesar_nlp_juridico(x, nlp)
    )
    
    # Guardar los resultados estructurados
    print(f"Exportando resultados a: {archivo_salida}...")
    df_justia.to_csv(archivo_salida, index=False, encoding='utf-8')
    
    print("\n¡Proceso completado exitosamente!")
    print("\nMuestra de los primeros 3 registros procesados:")
    print(df_justia[['id', 'texto_original', 'texto_limpio_lematizado']].head(3).to_string(index=False))