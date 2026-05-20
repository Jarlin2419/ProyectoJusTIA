"""
Generador de textos jurídicos simulados
Proyecto JustIA - Actividad 4
Autor: David
Fecha: Mayo 2026
"""

import random

# 1. Definir temas y frases base
temas = {
    "laboral": [
        "El trabajador tiene derecho a vacaciones remuneradas.",
        "La Ley 1010 de 2006 protege contra el acoso laboral.",
        "El contrato laboral debe incluir salario y prestaciones.",
        "El Ministerio de Trabajo regula las condiciones laborales."
    ],
    "penal": [
        "El delito de hurto agravado se sanciona con prisión.",
        "El homicidio culposo tiene sanciones específicas.",
        "La violencia intrafamiliar constituye delito según la ley.",
        "El juez dictó sentencia en caso de fraude procesal."
    ],
    "civil": [
        "El contrato de compraventa debe cumplir requisitos legales.",
        "La responsabilidad civil extracontractual se aplica en daños.",
        "El Código Civil regula las obligaciones y contratos.",
        "La sucesión intestada se rige por normas específicas."
    ],
    "familia": [
        "El matrimonio produce efectos jurídicos reconocidos por la ley.",
        "La custodia compartida busca proteger el interés superior del menor.",
        "La adopción requiere sentencia judicial.",
        "La violencia intrafamiliar puede dar lugar a medidas de protección."
    ],
    "constitucional": [
        "La Corte Constitucional declaró exequible la Ley 906 de 2004.",
        "La Constitución garantiza el derecho a la igualdad.",
        "El derecho a la salud es fundamental según jurisprudencia.",
        "La acción de tutela protege derechos fundamentales."
    ]
}

# 2. Generar dataset simulado
def generar_textos(num_textos=100):
    textos = []
    temas_lista = list(temas.keys())
    for i in range(num_textos):
        tema = random.choice(temas_lista)
        frase = random.choice(temas[tema])
        textos.append({"id": i+1, "tema": tema, "texto": frase})
    return textos

# 3. Guardar en archivo CSV
import csv
dataset = generar_textos(120)  # Genera 120 fragmentos

with open("textos_juridicos.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "tema", "texto"])
    writer.writeheader()
    writer.writerows(dataset)

print("Dataset generado: textos_juridicos.csv con", len(dataset), "fragmentos")
