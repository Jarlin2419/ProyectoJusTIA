import time

def mostrar_panel_explicabilidad():
    # 1. Entrada del usuario (Simulación de un caso real del Consultorio Virtual)
    consulta_usuario = (
        "Soy un trabajador del sector rural desplazado. Llevo más de un año en un predio, "
        "pero la junta local me dice que no tengo derechos de reclamación y me quieren sacar sin "
        "atender mi declaración de víctima."
    )
    
    # 2. Configuración de variables internas del modelo de IA (JustIA v2.1.0)
    modelo_consultado = "RoBERTa-Spanish-SQuAD2 (Reader) + Sentence-BERT (Retriever)"
    nivel_certeza = 94.2
    fuente_jurisprudencia = "Ley 1448 de 2011 (Ley de Víctimas y Restitución de Tierras) - Artículos 60 y 72"
    
    # Tokens o palabras clave que el tokenizador de JustIA identificó con mayor peso matemático
    tokens_clave = {
        "desplazado": 0.96,
        "predio": 0.89,
        "reclamación": 0.85,
        "declaración": 0.91,
        "víctima": 0.98
    }
    
    justificacion_natural = (
        "El sistema JustIA identificó con un 94.2% de certeza que la consulta corresponde al eje de "
        "Restitución de Tierras para Población Víctima del Conflicto. La IA seleccionó este camino debido "
        "a la alta densidad semántica de los tokens 'desplazado' y 'víctima'. Con base en el artículo 72 "
        "de la Ley 1448, las acciones de despojo o abandono forzado otorgan protección constitucional sobre "
        "los predios, inhabilitando las decisiones de juntas locales que pretendan vulnerar el debido proceso."
    )

    # 3. Renderizado del Panel Visual en Consola (Mockup Funcional)
    print("=" * 85)
    print("  JUSTIA XAI - PANEL DE EXPLICABILIDAD ALGORTÍMICA Y TRAZABILIDAD LEGAL")
    print("  Programa de Transformación Digital - Consultorio Virtual UniAsturias")
    print("=" * 85)
    time.sleep(0.5)
    
    print(f"[*] CASO INGRESADO:\n    \"{consulta_usuario}\"\n")
    print("-" * 85)
    
    print(f"[*] MODELO ARQUITECTÓNICO:  {modelo_consultado}")
    print(f"[*] NIVEL DE CERTEZA (CONFIDENCE SCORE): {nivel_certeza}%")
    print(f"[*] FUENTE DOCUMENTAL INDEXADA: {fuente_jurisprudencia}")
    print("-" * 85)
    
    print("[*] MATRIZ DE ATENCIÓN DE TOKENS (VALORACIÓN MATEMÁTICA DEL MODELO):")
    print(f"    {'TOKEN IDENTIFICADO':<25} | {'PESO EN EL EMBEDDING (0.0 a 1.0)':<35}")
    print("    " + "-" * 63)
    for token, peso in tokens_clave.items():
        # Generar una barra visual pequeña para representar la atención del transformer
        barra = "■" * int(peso * 10)
        print(f"    - {token:<21} | {peso:<31} [{barra:<10}]")
    print("-" * 85)
    
    print("[*] JUSTIFICACIÓN EN LENGUAJE NATURAL (EXPLICABILIDAD DE LA RECOMENDACIÓN):")
    lines = justificacion_natural.split(". ")
    for line in lines:
        if line:
            print(f"    ➢ {line.strip()}.")
    print("=" * 85)
    print("  [ESTADO DE AUDITORÍA: TRAZABILIDAD COMPLETA - SIN ALUCINACIONES DETECTADAS]")
    print("=" * 85)

if __name__ == "__main__":
    mostrar_panel_explicabilidad()