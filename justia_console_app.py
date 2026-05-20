"""
Proyecto: JustIA - Corporación Universitaria de Asturias
Actividad 3: Interfaz de Consola y Triaje Automatizado para Usuarios Vulnerables
Autor: Estudiante de Posgrado
"""

import os
import time
from justia_classifier import predecir_categoria_justia, cargar_diccionario

# Configuración de rutas del proyecto
RUTA_DICCIONARIO = os.path.join("data", "diccionario_justia.json")

def mostrar_encabezado():
    """Muestra el banner institucional del Consultorio Virtual."""
    print("=" * 75)
    print("        PROJECT JustIA - CORPORACIÓN UNIVERSITARIA DE ASTURIAS        ")
    print("        SISTEMA DE ASISTENCIA Y TRIAJE JURÍDICO PARA ENTIDADES SOCIALES")
    print("=" * 75)
    print(" Enfoque: Población Vulnerable, Rural, Víctimas del Conflicto y Migrantes")
    print("-" * 75)

def mostrar_menu():
    """Muestra las opciones de interacción de la primera capa del sistema."""
    print("\n--- MENÚ DE OPERACIONES PRINCIPALES ---")
    print("[1] Ingresar consulta legal en lenguaje natural (Asistente Virtual)")
    print("[2] Cargar e indexar documento externo (Simulación OCR para PDF/Imágenes)")
    print("[3] Ver estado del sistema y Diccionario de Control Ético")
    print("[4] Salir de la aplicación JustIA")
    print("-" * 39)

def ejecutar_asistente_virtual(diccionario):
    """Módulo que procesa preguntas frecuentes usando el clasificador por diccionario."""
    print("\n[MÓDULO] ASISTENTE VIRTUAL LEGAL")
    print("Escriba la inquietud planteada por el usuario (o escriba 'volver' para regresar):")
    consulta = input(">> ").strip()
    
    if consulta.lower() == 'volver' or not consulta:
        return

    print("\n[Procesando texto legal...]")
    time.sleep(1) # Simulación de tiempo de cómputo del modelo NLP
    
    # Consumir la función de predicción de la Actividad 2
    categoria, _, evidencias = predecir_categoria_justia(consulta, diccionario)
    
    print("\n" + "*" * 50)
    print(f"RESULTADO DEL TRIAJE AUTOMATIZADO:")
    print(f" -> Materia del Derecho: {categoria}")
    print("*" * 50)
    
    # Mostrar evidencias encontradas bajo el principio de transparencia
    palabras_encontradas = []
    for cat, pal in evidencias.items():
        if pal:
            palabras_encontradas.extend(pal)
            
    if palabras_encontradas:
        print(f"Evidencias léxicas detectadas: {', '.join(palabras_encontradas)}")
    else:
        print("Aviso: No se encontraron patrones claros en el diccionario.")
        
    print("\n[RECOMENDACIÓN ÉTICA - HUMAN IN THE LOOP]:")
    print("> Esta es una orientación informativa preliminar generada por el algoritmo.")
    print("> El caso ha sido asignado a la bandeja de revisión para estudiantes del consultorio.")
    print("=" * 75)

def ejecutar_ocr_simulado():
    """Módulo que simula la carga de PDFs/Imágenes escaneadas de juzgados rurales."""
    print("\n[MÓDULO] CARGA DE DOCUMENTOS EXTERNOS (OCR)")
    print("Simule la recepción de un archivo judicial introduciendo su ruta o nombre (ej: tutela.pdf):")
    nombre_archivo = input("Ruta del archivo >> ").strip()
    
    if not nombre_archivo:
        print("Error: No se especificó ningún archivo.")
        return
        
    _, extension = os.path.splitext(nombre_archivo.lower())
    
    print(f"\n[Analizando extensión del archivo: {extension if extension else 'Sin formato'}]")
    time.sleep(0.8)
    
    # Validación de formatos permitidos en el entorno seguro
    if extension in ['.pdf', '.txt']:
        print("✔ Formato válido aceptado por el ecosistema de JustIA.")
        print("[Extrayendo texto mediante capas de visión artificial y OCR...]")
        time.sleep(1.5)
        
        # Simulación de extracción de variables críticas (Anonimizadas)
        print("\n--- METADATOS EXTRAÍDOS DEL DOCUMENTO ---")
        print(f"Archivo: {os.path.basename(nombre_archivo)}")
        print("Sujeto Identificado: [PROTEGIDO - ANONIMIZADO LEY 1581]")
        print("Hechos extraídos: Reclamación por despojo de tierras rurales / Restitución.")
        print("Estado del proceso: Pendiente de radicación formal.")
        print("-" * 40)
        print("✔ El documento fue convertido a texto plano e indexado en el repositorio central.")
    else:
        print("❌ Error de Seguridad Algorítmica: Formato no soportado.")
        print("JustIA solo procesa archivos estructurados (.pdf, .txt) para mitigar malware y fugas de datos.")

def mostrar_estado_sistema(diccionario):
    """Muestra estadísticas actuales del diccionario de control ético."""
    print("\n[MÓDULO] ESTADO DE LA GOBERNANZA LÉXICA")
    print(f"Ubicación del Diccionario: '{RUTA_DICCIONARIO}'")
    print(f"Categorías jurídicas mapeadas actualmente: {len(diccionario.keys())}")
    for cat, terminos in diccionario.items():
        print(f" * Área [{cat}]: {len(terminos)} términos entrenados como rasgos (features).")
    print("\nPrincipio activo: Doble factor de verificación obligatoria (Estudiante + Docente).")

# ==========================================
# CICLO PRINCIPAL DE LA INTERFAZ
# ==========================================
def iniciar_aplicacion():
    # Intento de cargar el diccionario de la Actividad 2
    try:
        diccionario_control = cargar_diccionario(RUTA_DICCIONARIO)
    except FileNotFoundError:
        print(f"❌ Alerta: No se encontró el archivo '{RUTA_DICCIONARIO}'.")
        print("Por favor, ejecuta primero tu script 'ampliar_diccionario_justia.py' para generar la carpeta de datos.")
        return

    # Ciclo infinito de control por consola
    while True:
        mostrar_encabezado()
        mostrar_menu()
        
        opcion = input("Seleccione una opción (1-4): ").strip()
        
        if opcion == "1":
            ejecutar_asistente_virtual(diccionario_control)
        elif opcion == "2":
            ejecutar_ocr_simulado()
        elif opcion == "3":
            mostrar_estado_sistema(diccionario_control)
        elif opcion == "4":
            print("\nCerrando sesión en JustIA. Conciencia, ética y sensibilidad institucional. ¡Hasta pronto!")
            print("=" * 75)
            break
        else:
            print("\n❌ Opción no válida. Por favor ingrese un número entre 1 y 4.")
            
        # Pausa estética antes de limpiar la consola y repetir el menú
        input("\nPresione ENTER para continuar...")
        # Limpia la pantalla en Windows (cls) o Mac/Linux (clear) para simular una App real
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    iniciar_aplicacion()