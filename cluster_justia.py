import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

# ==========================================================
# 1. CARGA DEL DATASET (120 fragmentos generados en Actividad 2)
# ==========================================================
ruta_csv = "data/textos_juridicos.csv"

print(f"⏳ Cargando fragmentos jurídicos desde '{ruta_csv}'...")
if not os.path.exists(ruta_csv):
    print(f"❌ Error: No se encontró '{ruta_csv}'. Ejecuta primero tu generador de la Actividad 2.")
    exit()

df = pd.read_csv(ruta_csv)
textos = df["texto"].dropna().tolist()
temas_reales = df["tema"].dropna().tolist()
print(f"✅ Se cargaron {len(textos)} fragmentos indexados.")

# ==========================================================
# 2. EXTRACCIÓN DE EMBEDDINGS SEMÁNTICOS (Sentence-BERT)
# ==========================================================
print("\n⏳ Inicializando Sentence-BERT (paraphrase-multilingual-MiniLM-L12-v2)...")
# Este modelo lee el español a nivel conceptual, no solo por palabras sueltas
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

print("⏳ Calculando embeddings semánticos para los 120 fragmentos...")
embeddings = model.encode(textos, show_progress_bar=True)
print(f"✅ Embeddings generados con éxito. Dimensión de la matriz: {embeddings.shape}")

# ==========================================================
# 3. AGRUPAMIENTO TEMÁTICO (K-Means Clustering)
# ==========================================================
# Como el generador original tiene 5 temas (laboral, penal, civil, familia, constitucional)
num_clusters = 5
print(f"\n⏳ Aplicando algoritmo K-Means para generar {num_clusters} clusters semánticos...")

kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
df["cluster_id"] = kmeans.fit_predict(embeddings)
print("✅ Asignación de clusters finalizada.")

# ==========================================================
# 4. REDUCCIÓN DE DIMENSIONES PARA VISUALIZACIÓN (t-SNE)
# ==========================================================
print("\n⏳ Reduciendo dimensiones con t-SNE para la representación gráfica...")
# t-SNE comprime las dimensiones del embedding a solo 2 ejes (X, Y) para poder graficarlo
tsne = TSNE(n_components=2, perplexity=30, random_state=42, init='pca', learning_rate='auto')
embeddings_2d = tsne.fit_transform(embeddings)

df["tsne_x"] = embeddings_2d[:, 0]
df["tsne_y"] = embeddings_2d[:, 1]

# ==========================================================
# 5. VISUALIZACIÓN GRÁFICA CON MATPLOTLIB
# ==========================================================
print("📊 Generando el mapa de dispersión conceptual...")
plt.figure(figsize=(10, 8))

# Mapeamos los temas originales a colores para verificar si la IA agrupó correctamente
temas_unicos = list(set(temas_reales))
colores = plt.cm.get_cmap("Set2", len(temas_unicos))

for i, tema in enumerate(temas_unicos):
    mascara = df["tema"] == tema
    plt.scatter(
        df.loc[mascara, "tsne_x"],
        df.loc[mascara, "tsne_y"],
        label=tema.upper(),
        s=60,
        alpha=0.8,
        edgecolors='w'
    )

plt.title("JustIA - Agrupamiento Semántico de Textos Jurídicos (Sentence-BERT + t-SNE)", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Dimensión t-SNE 1", fontsize=10)
plt.ylabel("Dimensión t-SNE 2", fontsize=10)
plt.legend(title="Temas Originales", loc="best", frameon=True)
plt.grid(True, linestyle='--', alpha=0.5)

# Guardar la gráfica automáticamente como evidencia para tu informe
nombre_grafica = "justia_clusters_tsne.png"
plt.savefig(nombre_grafica, dpi=300, bbox_inches='tight')
print(f"💾 ¡Excelente! Gráfica guardada con éxito como '{nombre_grafica}'.")

# Mostrar la gráfica en pantalla
print("🚀 Abriendo ventana de visualización...")
plt.show()