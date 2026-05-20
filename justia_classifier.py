"""
Proyecto: JustIA - Corporación Universitaria de Asturias
Actividad 2: Clasificador de Casos Basado en Diccionario Técnico Ponderado
Autor: Estudiante de Posgrado
"""

import json
import re
import unicodedata
import os

def cargar_diccionario(ruta_json):
    """Carga el diccionario de términos desde el archivo JSON."""
    if not os.path.exists(ruta_json):
        raise FileNotFoundError(f"No se encontró el archivo del diccionario en: {ruta_json}")
    with open(ruta_json, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def normalizar_texto_simple(texto):
    """
    Limpia el texto de entrada quitando tildes, caracteres especiales
    y pasándolo a minúsculas para que coincida exactamente con el diccionario.
    """
    if not isinstance(texto, str):
        return ""
    texto = texto.lower()
    # Remover tildes de forma segura
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn' or c in ['\u0303']
    )
    texto = unicodedata.normalize('NFC', texto)
    # Mantener solo letras, espacios y la eñe
    texto = re.sub(r'[^a-zñ\s]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def predecir_categoria_justia(texto_usuario, diccionario):
    """
    Analiza el texto y devuelve la categoría jurídica con mayor puntaje de coincidencia.
    Si no encuentra palabras clave, devuelve 'Indeterminado' para control humano.
    """
    texto_limpio = normalizar_texto_simple(texto_usuario)
    
    # Inicializar el marcador de puntajes por categoría
    puntajes = {categoria: 0 for categoria in diccionario.keys()}
    detalles_coincidencias = {categoria: [] for categoria in diccionario.keys()}
    
    # Buscar coincidencias de las palabras clave en el texto limpio
    for categoria, palabras_clave in diccionario.items():
        for palabra in palabras_clave:
            # Usamos expresiones regulares con límites de palabra (\b) para evitar falsos positivos
            patron = rf'\b{palabra}\b'
            coincidencias = len(re.findall(patron, texto_limpio))
            
            if coincidencias > 0:
                puntajes[categoria] += coincidencias
                detalles_coincidencias[categoria].append(f"'{palabra}' (x{coincidencias})")
                
    # Determinar el puntaje máximo obtenido
    max_puntaje = max(puntajes.values())
    
    # PRINCIPIO ÉTICO DE CONTROL HUMANO: Si ninguna palabra clave coincide, no adivina
    if max_puntaje == 0:
        return "Indeterminado (Requiere revisión humana)", puntajes, detalles_coincidencias
    
    # Identificar si hay empates entre categorías
    categorias_ganadoras = [cat for cat, puntaje in puntajes.items() if puntaje == max_puntaje]
    
    # Si hay un empate técnico, se escala a revisión humana para evitar clasificaciones sesgadas
    if len(categorias_ganadoras) > 1:
        return f"Empate Técnico {categorias_ganadoras} (Requiere revisión humana)", puntajes, detalles_coincidencias
        
    return categorias_ganadoras[0], puntajes, detalles_coincidencias


# ==========================================
# PRUEBAS DE EVALUACIÓN DEL SISTEMA
# ==========================================
if __name__ == "__main__":
    ruta_dict = 'data/diccionario_justia.json'
    
    try:
        # 1. Cargar el recurso estructurado
        dict_justia = cargar_diccionario(ruta_dict)
        print("¡Diccionario técnico cargado con éxito para el proyecto JustIA!\n")
        
        # 2. Casos de prueba simulados que llegan de zonas rurales o usuarios vulnerables
        casos_entrada = [
            "Buenas tardes, requiero iniciar un trámite de divorcio porque sufro de violencia intrafamiliar y necesito asegurar la custodia y los alimentos de mi menor hijo.",
            "La empresa donde trabajaba me hizo un despido sin justa causa y no me han pagado mis prestaciones sociales ni la indemnización del salario.",
            "Soy un pequeño agricultor y un vecino bloqueó el camino; necesito saber cómo interponer una servidumbre de tránsito sobre ese predio rural.",
            "Un miembro de la Policía Nacional cometió un abuso de autoridad contra mi comunidad durante una manifestación pública.",
            "Nuestra comunidad indígena solicita una consulta previa ante el despojo violento que sufrió nuestro territorio ancestral.",
            "Necesito una asesoría jurídica para saber cómo redactar una carta de presentación para un empleo." # Caso ambiguo / sin palabras clave
        ]
        
        # 3. Ejecutar la predicción para cada caso
        for i, caso in enumerate(casos_entrada, start=1):
            print(f"================ CASO DE ENTRADA CLIENTE VULNERABLE #{i} ================")
            print(f"Texto: '{caso}'\n")
            
            categoria_asignada, matriz_votos, evidencias = predecir_categoria_justia(caso, dict_justia)
            
            print(f"-> CATEGORÍA ASIGNADA POR JustIA: **{categoria_asignada}**")
            print("-> Evidencias encontradas:")
            for cat, pal in evidencias.items():  # Corregido: 'in' en lugar de 'en'
                if pal:
                    print(f"   * En [{cat}]: coinciden los términos {', '.join(pal)}")
            print("-" * 70 + "\n")
            
    except FileNotFoundError as e:
        print(e)
        print("Asegúrate de haber creado el archivo 'diccionario_justia.json' en esta misma carpeta antes de correr el script.")