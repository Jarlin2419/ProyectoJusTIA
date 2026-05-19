import os
import torch
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoModelForQuestionAnswering, AutoTokenizer

# ==========================================================
# 1. BASE DE CONOCIMIENTO (Lectura de archivos .txt en /data)
# ==========================================================
carpeta_data = "data"
base_conocimiento = []

print(f"⏳ Escaneando la carpeta '{carpeta_data}' para cargar los documentos...")

if not os.path.exists(carpeta_data):
    print(f"❌ Error: La carpeta '{carpeta_data}' no existe. Ejecuta primero tu generador.")
    exit()

for archivo in os.listdir(carpeta_data):
    if archivo.endswith(".txt"):
        ruta_completa = os.path.join(carpeta_data, archivo)
        with open(ruta_completa, "r", encoding="utf-8") as f:
            contenido = f.read()
            base_conocimiento.append({
                "fuente": f"Documento Fuente: {archivo}",
                "texto": contenido
            })

if not base_conocimiento:
    print(f"❌ Error: No se encontraron archivos .txt dentro de '{carpeta_data}'.")
    exit()

print(f"✅ Se cargaron exitosamente {len(base_conocimiento)} documentos jurídicos para JustIA.\n")
documentos = [doc["texto"] for doc in base_conocimiento]

# ==========================================================
# 2. IMPLEMENTACIÓN DEL RETRIEVER (Buscador Semántico)
# ==========================================================
vectorizer = TfidfVectorizer()
X_docs = vectorizer.fit_transform(documentos)

def buscar_documento_relevante(pregunta):
    query_vector = vectorizer.transform([pregunta])
    similitudes = cosine_similarity(query_vector, X_docs).flatten()
    mejor_idx = np.argmax(similitudes)
    
    if similitudes[mejor_idx] < 0.05:
        return None, None
    
    return base_conocimiento[mejor_idx]["texto"], base_conocimiento[mejor_idx]["fuente"]

# ==========================================================
# 3. CARGA NATIVA DEL MODELO Y TOKENIZADOR (Sin Pipelines)
# ==========================================================
print("⏳ Cargando modelo de QA en español RoBERTa (Procesamiento nativo)...")
model_name = "mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

print("✅ Sistema RAG de JustIA listo para responder consultas de forma nativa.")
print("=" * 75)

# ==========================================================
# 4. INTERFAZ DE EXTRACCIÓN DE RESPUESTAS NATIVA
# ==========================================================
def consultar_justia(pregunta_usuario):
    print(f"\n❓ PREGUNTA RECIBIDA: '{pregunta_usuario}'")
    
    # Paso 1: Retriever (Búsqueda del archivo adecuado)
    contexto, fuente = buscar_documento_relevante(pregunta_usuario)
    
    if not contexto:
        print("❌ JustIA: Lo siento, no encontré documentos en la base de conocimiento aplicables.")
        return

    # Paso 2: Tokenización manual de la entrada
    inputs = tokenizer(pregunta_usuario, contexto, return_tensors="pt", max_length=512, truncation=True)
    
    # Paso 3: Inferencia del modelo sin calcular gradientes (más rápido)
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Obtener las posiciones lógicas con mayor probabilidad de inicio y fin
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits
    
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores) + 1
    
    # Convertir los tokens matemáticos de vuelta a palabras reales
    tokens_respuesta = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end])
    respuesta = tokenizer.convert_tokens_to_string(tokens_respuesta).strip()
    
    # Control de respuestas vacías o fallas de contexto
    if not respuesta or "[CLS]" in respuesta or answer_end <= answer_start:
        respuesta = "Información no encontrada explícitamente en el fragmento"

    # Paso 4: Retornar los resultados en la terminal
    print("\n⚖️ --- RESPUESTA DE JUSTIA ---")
    print(f"👉 {respuesta.capitalize()}.")
    print(f"📖 Contexto de Soporte: \"{contexto.replace('\n', ' ')}\"")
    print(f"📌 Fuente Extraída: {fuente}")
    print("-" * 75)

# ==========================================================
# 5. BANCO DE PRUEBAS AUTOMÁTICO
# ==========================================================
preguntas_prueba = [
    "¿Qué derechos tienen los trabajadores ante el acoso laboral?",
    "¿Qué garantiza la Ley 906 de 2004?",
    "¿Qué incluye el sistema de seguridad social según la ley 100?",
    "¿Qué ordenó la Resolución 456 de 2020 para las empresas?"
]

for pregunta in preguntas_prueba:
    consultar_justia(pregunta)