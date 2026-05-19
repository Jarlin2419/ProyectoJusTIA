import spacy
from spacy.pipeline import EntityRuler
from spacy import displacy
import pandas as pd

# ==========================================
# 1. CORPUS: CARGA AUTOMÁTICA DESDE TU CSV GENERADO
# ==========================================
ruta_csv = "data/textos_juridicos.csv"

try:
    # Leemos el CSV generado por tu otro script
    df_ner = pd.read_csv(ruta_csv)
    
    # Tomamos los primeros 10 o 15 textos para la muestra y visualización académica
    # (Puedes quitar el [:15] si quieres procesar los 120 de golpe en consola)
    textos_juridicos = df_ner["texto"].dropna().tolist()[:15]
    print(f"✅ Se cargaron exitosamente los textos desde '{ruta_csv}'. Tomando muestra de control.")
except FileNotFoundError:
    print(f"❌ Error: No se encontró el archivo '{ruta_csv}'.")
    print("👉 Asegúrate de ejecutar primero tu script generador para crear el archivo CSV.")
    exit()

# ==========================================
# 2. CARGAR MODELO SPACY EN ESPAÑOL
# ==========================================
print("⏳ Cargando modelo lingüístico de spaCy (es_core_news_md)...")
try:
    nlp = spacy.load("es_core_news_md")
except OSError:
    print("❌ Error: Modelo no encontrado. Ejecuta: pip install spacy && python -m spacy download es_core_news_md")
    exit()

# ==========================================
# 3. CONFIGURACIÓN DEL ENTITYRULER (REGLAS ADAPTADAS)
# ==========================================
ruler = nlp.add_pipe("entity_ruler", before="ner")

patrones = [
    # ---- Regla para Normas Jurídicas ----
    # Captura: "Ley 1010 de 2006", "Ley 906 de 2004", "Código Civil", etc.
    {
        "label": "NORMA_JURIDICA", 
        "pattern": [
            {"LOWER": {"IN": ["ley", "decreto", "artículo", "articulo", "código", "codigo"]}}, 
            {"SHAPE": "dXd", "OP": "?"}, 
            {"IS_DIGIT": True, "OP": "?"}, # Para el número de la ley
            {"LOWER": "de", "OP": "?"}, 
            {"IS_DIGIT": True, "OP": "?"}  # Para el año
        ]
    },
    {
        "label": "NORMA_JURIDICA",
        "pattern": [{"LOWER": "constitución"}]
    },
    
    # ---- Regla para Tipos de Violencia o Delitos de tu generador ----
    # Captura: "violencia intrafamiliar", "hurto agravado", "homicidio culposo", "acoso laboral", "fraude procesal"
    {
        "label": "DELITO_O_CONDUCTA", 
        "pattern": [
            {"LOWER": "violencia"}, 
            {"LOWER": "intrafamiliar"}
        ]
    },
    {
        "label": "DELITO_O_CONDUCTA", 
        "pattern": [
            {"LOWER": {"IN": ["hurto", "homicidio", "fraude", "acoso"]}}, 
            {"LOWER": {"IN": ["agravado", "culposo", "procesal", "laboral"]}}
        ]
    },
    
    # ---- Regla para Jurisdicciones / Entidades del Estado ----
    # Captura: "Ministerio de Trabajo", "Corte Constitucional"
    {
        "label": "INSTITUCION",
        "pattern": [
            {"LOWER": "ministerio"},
            {"LOWER": "de"},
            {"LOWER": "trabajo"}
        ]
    },
    {
        "label": "INSTITUCION",
        "pattern": [
            {"LOWER": "corte"},
            {"LOWER": "constitucional"}
        ]
    }
]

ruler.add_patterns(patrones)
print("✅ Reglas acopladas y calibradas para el nuevo dataset.")

# ==========================================
# 4. PROCESAMIENTO Y EXTRACCIÓN EN CONSOLA
# ==========================================
print("\n🚀 Ejecutando Extractor NER en los datos simulados...")
print("="*70)

for idx, texto in enumerate(textos_juridicos, 1):
    doc = nlp(texto)
    print(f"\n📄 CASO EVALUADO #{idx}:")
    print(f"\"{texto}\"")
    print("-" * 40)
    
    if not doc.ents:
        print("  [Sin entidades detectadas en esta frase]")
    else:
        for ent in doc.ents:
            label_limpio = ent.label_
            # Homologamos etiquetas nativas de spaCy si llegaran a salir (ej: PER)
            if label_limpio == "PER": label_limpio = "PERSONA"
            if label_limpio == "LOC": label_limpio = "LUGAR"
            if label_limpio == "ORG" and ent.text not in ["Ministerio de Trabajo", "Corte Constitucional"]: 
                label_limpio = "INSTITUCION"
            if label_limpio == "MISC": continue
            
            print(f"  • {ent.text:<28} ➔ Etiqueta: [{label_limpio}]")

# ==========================================
# 5. VISUALIZACIÓN EN VIVO CON DISPLACY
# ==========================================
print("\n" + "="*70)
print("📊 Renderizando visualización web con displaCy...")

opciones_visuales = {
    "ents": ["NORMA_JURIDICA", "DELITO_O_CONDUCTA", "INSTITUCION", "PERSONA"],
    "colors": {
        "NORMA_JURIDICA": "#ffb3ba",    # Rosa pastel
        "DELITO_O_CONDUCTA": "#ffdfba", # Naranja pastel
        "INSTITUCION": "#bae1ff",       # Azul pastel
        "PERSONA": "#baffc9"            # Verde pastel
    }
}

corpus_unificado = nlp(" \n\n ".join(textos_juridicos))

print("🌍 Servidor local corriendo.")
print("👉 Abre en tu navegador: http://localhost:5000")
print("🛑 Presiona Ctrl + C en la terminal para apagar el servidor visual.")

displacy.serve(corpus_unificado, style="ent", options=opciones_visuales, port=5000)