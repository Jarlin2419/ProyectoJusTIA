"""
Proyecto: JustIA - Corporación Universitaria de Asturias
Herramienta: Generador Sintético de Corpus Jurídico (500 fragmentos únicos)
Autor: Estudiante de Posgrado
"""

import pandas as pd
import random
import os  # Importamos os para el manejo seguro de carpetas

# Definición de componentes gramaticales por rama del derecho para garantizar coherencia
componentes_legales = {
    "Familia": {
        "sujetos": ["El defensor de familia", "La madre cabeza de hogar", "El comisario de familia", "El juez promiscuo municipal", "El alimentante", "El menor de edad"],
        "verbos": ["deberá fijar", "solicita la regulación urgente de", "interpone medida de protección por", "declarará la existencia de", "suspende temporalmente", "exige la restitución de"],
        "objetos": ["la cuota alimentaria obligatoria", "la violencia intrafamiliar física y económica", "la custodia y cuidado personal del menor", "la unión marital de hecho patrimonial", "la patria potestad por abandono", "los derechos del niño interviniente"],
        "contextos": ["de acuerdo con los ingresos reales demostrados.", "para proteger de manera prioritaria el interés superior.", "ante la notaría pública o centro de conciliación.", "tras comprobarse la convivencia continua de dos años.", "de forma inmediata para mitigar el riesgo inminente.", "con base en el Código de la Infancia y la Adolescencia colombiana."]
    },
    "Laboral": {
        "sujetos": ["El empleador", "El trabajador de la empresa", "El inspector de trabajo", "El juez laboral del circuito", "El sindicato de la institución", "La trabajadora en estado de embarazo"],
        "verbos": ["está obligado a pagar", "denuncia el acoso laboral y", "reconoce la estabilidad laboral reforzada de", "exige el reconocimiento de", "prohíbe la retención ilegal de", "tramita la indemnización por"],
        "objetos": ["el salario mínimo legal mensual vigente", "las horas extras y recargos nocturnos", "el despido injustificado sin el debido proceso", "las prestaciones sociales y aportes de seguridad social", "el fuero sindical de los delegados", "la jornada laboral máxima legal permitida"],
        "contextos": ["dentro de los términos establecidos por el Código Sustantivo del Trabajo.", "bajo la gravedad de sanción por reincidencia o mora.", "sin que medie discriminación por razones de nacionalidad o género.", "de manera inmediata tras la terminación del vínculo contractual.", "mediante previa autorización de la oficina judicial competente.", "de conformidad con los fallos hito de la Corte Suprema de Justicia."]
    },
    "Civil_Y_Tierras": {
        "sujetos": ["El poseedor del bien inmueble", "El predio sirviente", "El propietario inscrito", "El juez civil municipal", "El pequeño agricultor de la zona rural", "El acreedor hipotecario"],
        "verbos": ["demanda la prescripción adquisitiva de", "está obligado a otorgar", "adelanta el proceso de pertenencia sobre", "constituye gravamen de hipoteca mediante", "solicita la restitución del predio por", "exige el deslinde y amojonamiento de"],
        "objetos": ["la propiedad privada sujeta a función social", "la servidumbre de tránsito hacia la vía pública", "el terreno rural explotado económicamente", "la escritura pública ante el notario", "el contrato de arrendamiento de fincas", "los linderos oficiales certificados por el IGAC"],
        "contextos": ["para sanear legalmente los títulos de propiedad de la tierra.", "con base en los requisitos del Código Civil colombiano.", "tras demostrarse una explotación agraria pacífica y continua.", "inscrito debidamente en la Oficina de Registro de Instrumentos Públicos.", "requiriendo el pago justo de una indemnización previa.", "para evitar conflictos de tenencia entre los campesinos de la región."]
    },
    "Disciplinario_Policial": {
        "sujetos": ["El servidor público", "El comité disciplinario de la entidad", "El miembro de la Policía Nacional", "El sujeto disciplinable", "El funcionario de la procuraduría", "El personero municipal"],
        "verbos": ["incurre en falta gravísima por", "debe actuar bajo el principio de", "será sancionado con destitución e inhabilidad ante", "vulnera el debido proceso durante", "asume la responsabilidad legal por", "debe garantizar el derecho a de"],
        "objetos": ["el incumplimiento estricto de la Constitución Política", "actos que configuren discriminación u hostigamiento", "el abuso de autoridad contra los ciudadanos", "la expedición de fallos sin sustento probatorio", "la omisión de los deberes funcionales del cargo", "tratos crueles, inhumanos o degradantes"],
        "contextos": ["según los parámetros vigentes de la Ley 1952 de 2019.", "en concordancia con el Estatuto Disciplinario Policial Ley 2196.", "lo cual genera una investigación interna de carácter preferente.", "salvo que concurra una causal de exclusión de responsabilidad.", "garantizando siempre una función preventiva y correctiva de la ley.", "durante todas las actuaciones de la etapa de juzgamiento."]
    },
    "Etnico_Y_Victimas": {
        "sujetos": ["La comunidad indígena ancestral", "La Unidad de Restitución de Tierras", "La población víctima del conflicto armado", "La jurisdicción especial indígena", "El refugiado extranjero", "El colectivo afrodescendiente"],
        "verbos": ["ejerce el derecho fundamental a", "administra justicia propia mediante", "tramita la devolución y saneamiento de", "recibirá atención humanitaria de emergencia por", "exige garantías de no repetición ante", "goza de medidas de protección contra"],
        "objetos": ["la consulta previa, libre e informada", "sus usos, costumbres y ámbito territorial propio", "los territorios colectivos inalienables", "el despojo violento de predios rurales", "la verdad, la justicia y la reparación integral", "la discriminación algorítmica e institucional"],
        "contextos": ["para asegurar la supervivencia física y cultural del pueblo.", "coordinando acciones con el marco de la Constitución colombiana.", "por causa del desplazamiento forzado interno en zonas rurales.", "bajo las directrices internacionales para la protección de migrantes.", "con enfoque diferencial y de género para minorías étnicas.", "financiado por el fondo nacional de atención a víctimas."]
    }
}

def generar_fragmento_unico(rama):
    """Construye un fragmento jurídico seleccionando elementos al azar de una rama."""
    comp = components = componentes_legales[rama]
    sujeto = random.choice(comp["sujetos"])
    verbo = random.choice(comp["verbos"])
    objeto = random.choice(comp["objetos"])
    contexto = random.choice(comp["contextos"])
    
    # Armamos la estructura sintáctica básica
    return f"{sujeto} {verbo} {objeto} {contexto}"

# ==========================================
# CONSTRUCCIÓN DEL DATASET DE 500 REGISTROS
# ==========================================
print("Iniciando la generación de 500 fragmentos jurídicos para JustIA...")

fragmentos_totales = []
ramas = list(componentes_legales.keys())

# Para evitar textos idénticos repetidos, usaremos un set para controlar la unicidad
textos_unicos = set()
contador_id = 1

while len(textos_unicos) < 500:
    # Elegimos una rama equitativamente para mantener un dataset balanceado
    rama_actual = ramas[len(textos_unicos) % len(ramas)]
    
    nuevo_texto = generar_fragmento_unico(rama_actual)
    
    if nuevo_texto not in textos_unicos:
        textos_unicos.add(nuevo_texto)
        fragmentos_totales.append({
            "id": contador_id,
            "rama_derecho": rama_actual,
            "texto_original": nuevo_texto
        })
        contador_id += 1

# Convertir a DataFrame de Pandas
df_sintetico = pd.DataFrame(fragmentos_totales)

# ==========================================
# GESTIÓN SEGURA DE CARPETAS Y SALIDA
# ==========================================
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
carpeta_data = os.path.join(carpeta_actual, "data")

# Crear la carpeta 'data' si no existe en tu espacio de trabajo
if not os.path.exists(carpeta_data):
    os.makedirs(carpeta_data)

archivo_salida = os.path.join(carpeta_data, 'corpus_original.csv')
df_sintetico.to_csv(archivo_salida, index=False, encoding='utf-8')

print(f"¡Éxito! Archivo '{archivo_salida}' creado con 500 fragmentos jurídicos colombianos distribuidos equitativamente.")
print("\nMuestra de distribución por área del derecho:")
print(df_sintetico['rama_derecho'].value_counts())
print("\nPrimeros 2 ejemplos del archivo generado:")
print(df_sintetico[['id', 'rama_derecho', 'texto_original']].head(2).to_string(index=False))