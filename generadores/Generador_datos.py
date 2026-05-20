import pandas as pd
import os

# 1. Asegurar que la carpeta data existe
if not os.path.exists("data"):
    os.makedirs("data")

# 2. Tu dataset base (el que me pasaste)
data = {
    "texto": [
        "El acusado fue condenado por homicidio agravado", "Investigación por tráfico de estupefacientes",
        "Captura por porte ilegal de armas", "Proceso por violencia intrafamiliar",
        "Demanda por incumplimiento de contrato", "Proceso de responsabilidad civil extracontractual",
        "Litigio sobre propiedad privada", "Disputa por contrato de arrendamiento",
        "Despido injustificado del trabajador", "Reclamación por liquidación laboral",
        "Proceso por acoso laboral", "Solicitud de pago de prestaciones sociales",
        "Custodia y alimentos del menor", "Proceso de divorcio contencioso",
        "Solicitud de patria potestad", "Demanda por violencia familiar"
    ],
    "tema": ["penal", "penal", "penal", "penal", "civil", "civil", "civil", "civil", "laboral", "laboral", "laboral", "laboral", "familia", "familia", "familia", "familia"]
}

df_original = pd.DataFrame(data)

# 3. Lógica de Aumentación (Crear variantes para que la IA aprenda patrones)
prefijos = [
    "Se registra un", "Existe un nuevo", "Reporte de", "Inicia el", 
    "Fallo sobre el", "Sentencia de", "Se analiza el", "Radicado de",
    "Expediente de", "Documento sobre", "Notificación de", "Audiencia por"
]

nuevos_datos = []
for _, row in df_original.iterrows():
    for pref in prefijos:
        # Mezclamos el prefijo con el texto original en minúsculas
        nuevos_datos.append({
            "texto": f"{pref} {row['texto'].lower()}", 
            "tema": row['tema']
        })

# 4. Combinar y guardar
df_extendido = pd.concat([df_original, pd.DataFrame(nuevos_datos)]).drop_duplicates()
df_extendido.to_csv("data/dataset.csv", index=False) # Sobrescribimos el archivo que usa train.py

print(f"✅ ¡Éxito! El dataset ahora tiene {len(df_extendido)} ejemplos para entrenar.")