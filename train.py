import pandas as pd
import numpy as np
import os
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

# ======================
# CONFIGURACIÓN DE ENTORNO (CRÍTICO PARA WINDOWS)
# ======================
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# ======================
# Cargar dataset
# ======================
try:
    df = pd.read_csv("data/dataset.csv")
    print("✅ Dataset cargado correctamente.")
except FileNotFoundError:
    print("❌ Error: No se encontró 'data/dataset.csv'. Revisa la ruta.")
    exit()

# ======================
# Etiquetas
# ======================
labels = {
    "penal": 0,
    "civil": 1,
    "laboral": 2,
    "familia": 3
}

df["label"] = df["tema"].map(labels)

# Validar si hay valores nulos tras el mapeo por textos mal etiquetados
if df["label"].isnull().any():
    print("⚠️ Advertencia: Hay filas con temas que no coinciden con el diccionario de etiquetas. Eliminándolas...")
    df = df.dropna(subset=["label"])
    df["label"] = df["label"].astype(int)

# ======================
# División entrenamiento/prueba
# ======================
train_texts, test_texts, train_labels, test_labels = train_test_split(
    df["texto"],
    df["label"],
    test_size=0.2,
    random_state=42
)

# ======================
# Crear datasets
# ======================
train_dataset = Dataset.from_dict({
    "text": train_texts.tolist(),
    "label": train_labels.tolist()
})

test_dataset = Dataset.from_dict({
    "text": test_texts.tolist(),
    "label": test_labels.tolist()
})

# ======================
# Modelo BETO
# ======================
modelo_path = "dccuchile/bert-base-spanish-wwm-cased"
print(f"⏳ Descargando/Cargando modelo y tokenizador: {modelo_path}")
tokenizer = AutoTokenizer.from_pretrained(modelo_path)

# ======================
# Tokenización
# ======================
def tokenize(batch):
    return tokenizer(
        batch["text"],
        padding="max_length", 
        truncation=True,
        max_length=128
    )

print("⏳ Tokenizando datos...")
train_dataset = train_dataset.map(tokenize, batched=True)
test_dataset = test_dataset.map(tokenize, batched=True)

# CORRECCIÓN DE FORMATO: Forzar el formato PyTorch y conservar las columnas necesarias
train_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])
test_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

# ======================
# Modelo clasificación
# ======================
model = AutoModelForSequenceClassification.from_pretrained(
    modelo_path,
    num_labels=4
)

# ======================
# Métricas
# ======================
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    accuracy = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions, average="weighted")
    return {
        "accuracy": accuracy,
        "f1": f1
    }

# ======================
# Configuración entrenamiento (OPTIMIZADA)
# ======================
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4, 
    per_device_eval_batch_size=4,
    
    # AJUSTE DE ÉPOCAS: Si entrenas en CPU, 3-4 épocas evitan que el equipo colapse por horas.
    # Si logras configurar CUDA/GPU, puedes subirlo a 5 o más sin problema.
    num_train_epochs=3, 
    
    weight_decay=0.01,
    logging_steps=5,
    
    # RECOMENDACIÓN: Cambiar a False si tienes tarjeta gráfica NVIDIA configurada con CUDA.
    use_cpu=True, 
    
    load_best_model_at_end=True, # Guarda automáticamente el mejor modelo basado en la pérdida de evaluación
    metric_for_best_model="f1"
)

# ======================
# Trainer
# ======================
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics
)

# ======================
# Entrenamiento
# ======================
print("🚀 Iniciando entrenamiento del sistema JustIA...")
trainer.train()

# ======================
# Evaluación
# ======================
print("\n📊 Evaluación final:")
results = trainer.evaluate()
print(results)

# Guardar el modelo entrenado y el tokenizador para producción
print("\n💾 Guardando modelo entrenado en './modelo_justia'...")
model.save_pretrained("./modelo_justia")
tokenizer.save_pretrained("./modelo_justia")
print("✅ ¡Proceso completado con éxito!")