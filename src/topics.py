"""
Diccionario temático para análisis de discursos presidenciales chilenos.
Cada tema mapea a una lista de raíces (lemas) que captan sus variantes.
El matching se hace con regex que captura la raíz seguida de cualquier letra.
"""

DICCIONARIO_TEMATICO = {
    'Economía': [
        'econom', 'crecimiento', 'inversion', 'inversión', 'fiscal',
        'pib', 'productiv', 'exportac', 'importac', 'mercado', 'empresa',
        'pyme', 'pymes', 'innovaci', 'competitiv', 'tributari', 'impuesto',
        'inflaci', 'comercio', 'desarrollo económico'
    ],
    'Seguridad': [
        'seguridad', 'delincuen', 'delito', 'crimen', 'criminal',
        'narcotrafic', 'narcotráfico', 'droga', 'homicid', 'asalto',
        'robo', 'policia', 'policía', 'carabiner', 'pdi',
        'orden público', 'violencia', 'sicariato'
    ],
    'Pensiones': [
        'pension', 'pensión', 'jubilac', 'jubilad',
        'previsional', 'previsión', 'afp', 'reforma previsional',
        'pgu', 'pilar solidario', 'adulto mayor', 'tercera edad',
        'cotizaci'
    ],
    'Vivienda': [
        'vivienda', 'habitacional', 'casa propia', 'subsidio habitacional',
        'campamento', 'allegado', 'déficit habitacional',
        'serviu', 'minvu', 'arriendo', 'integraci', 'barrio'
    ],
    'Educación': [
        'educa', 'educación', 'enseñanza', 'enseñar', 'escuela',
        'escolar', 'liceo', 'colegio', 'universi', 'universitar',
        'profesor', 'estudiant', 'alumn', 'aprendi',
        'pedago', 'gratuidad', 'beca', 'cae',
        'jardín infantil', 'sala cuna', 'parvular', 'kinder',
        'docente'
    ],
    'Salud': [
        'salud', 'hospital', 'hospitalar', 'clínic',
        'medicament', 'enfermedad', 'enferm',
        'consultorio', 'cesfam', 'sapu', 'fonasa', 'isapre',
        'auge', 'ges', 'lista de espera', 'atención primaria',
        'medic', 'pandemia', 'covid', 'coronavirus',
        'vacuna', 'vacunaci', 'sanitari'
    ],
    'Araucanía/Mapuche': [
        'mapuche', 'araucanía', 'araucania', 'pueblo originario',
        'pueblos originarios', 'pueblo indígena', 'pueblos indígenas',
        'wallmapu', 'macrozona sur', 'conflicto mapuche',
        'tierras ancestrales', 'conadi'
    ],
    'Género/Mujer': [
        'mujer', 'mujeres', 'género', 'genero',
        'feminicidio', 'femicidio', 'femen',
        'paridad', 'brecha salarial', 'violencia contra la mujer',
        'violencia de género', 'sernam', 'sernameg',
        'igualdad de género'
    ],
    'Niños/Infancia': [
        'infancia', 'infantil',
        'menor de edad', 'menores de edad',
        'sename', 'mejor niñez',
        'primera infancia', 'cuidado infantil',
        'niños y niñas', 'niñas y niños',
        'vulneración de derechos',
        'protección de la niñez', 'política de infancia'
    ],
    'Medio ambiente': [
        'medio ambient', 'ambiental', 'cambio climático',
        'cambio climatico', 'climátic', 'climatic',
        'sustentab', 'sostenib', 'ecolog', 'biodiversidad',
        'contaminaci', 'emisiones', 'descarbonizaci',
        'energía renovable', 'energías renovables'
    ],
    'Trabajo/Empleo': [
        'trabajo', 'trabajador', 'empleo', 'empleador',
        'desempleo', 'cesantía', 'cesantia',
        'sindicato', 'sindical', 'salario',
        'sueldo mínimo', 'sueldo minimo', 'salario mínimo',
        'jornada laboral', '40 horas', 'subcontrataci'
    ],
    'Migración': [
        'migración', 'migracion', 'migrant', 'migratori',
        'extranjer', 'inmigra', 'frontera',
        'visa', 'expulsion', 'expulsión',
        'irregular', 'crisis migratoria'
    ],
    'Constitución': [
        'constituci', 'constitucional', 'carta magna',
        'proceso constituyente', 'convención constitucional',
        'plebiscito', 'nueva constitución',
        'reforma constitucional'
    ],
    'Derechos humanos': [
        'derechos humanos', 'ddhh', 'dictadura',
        'violaciones a los derechos humanos', 'detenidos desaparecidos',
        'memoria', 'verdad y justicia', 'museo de la memoria',
        'víctimas de la dictadura', 'tortura'
    ],
    'Regiones': [
        'región', 'regiones', 'regional', 'descentralizaci',
        'gobernador regional', 'territorio',
        'zonas extremas', 'desarrollo regional',
        'provincia', 'comuna', 'municipio'
    ],
    'Tecnología': [
        'tecnolog', 'digital', 'digitalizaci',
        'inteligencia artificial', 'innovaci',
        'ciencia', 'investigaci',
        'fibra óptica', 'fibra optica', '5g',
        'transformación digital', 'gobierno digital',
        'startup', 'emprendimiento tecnológico'
    ],

    'Corrupción': [
        'corrupción', 'corrupcion', 'corrupto', 'corruptos',
        'transparencia', 'rendición de cuentas',
        'probidad', 'cohecho', 'soborno',
        'conflicto de interés', 'conflictos de interés',
        'fraude', 'malversación',
        'caso penta', 'caso soquimich', 'caso corpesca',
        'lavado de activos'
    ],
    'Pobreza': [
        'pobreza', 'pobre', 'pobres',
        'extrema pobreza', 'línea de la pobreza',
        'vulnerabilidad social', 'vulnerables',
        'familias vulnerables', 'erradicar la pobreza',
        'superación de la pobreza',
        'hambre', 'hambruna'
    ],
    'Desigualdad': [
        'desigualdad', 'desigualdades',
        'inequidad', 'inequidades',
        'brecha social', 'brechas sociales',
        'redistribución', 'redistributiv',
        'justicia social', 'concentración de la riqueza',
        'concentración del ingreso',
        'sociedad más justa', 'país más justo'
    ],
}

# Stopwords para filtrar cuando hagamos análisis de contenido
# (nubes de palabras, términos distintivos, etc.)
# No se usan para el denominador de "menciones por mil palabras".
STOPWORDS_ESPAÑOL = {
    'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
    'de', 'del', 'al', 'a', 'en', 'con', 'sin', 'por', 'para',
    'que', 'y', 'o', 'u', 'e', 'ni', 'pero', 'mas', 'sino',
    'si', 'no', 'es', 'son', 'fue', 'fueron', 'ser', 'sido', 'está', 'están',
    'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas',
    'su', 'sus', 'mi', 'mis', 'tu', 'tus', 'nuestro', 'nuestra', 'nuestros', 'nuestras',
    'le', 'les', 'lo', 'la', 'me', 'te', 'se', 'nos',
    'como', 'cuando', 'donde', 'porque', 'aunque',
    'hay', 'ha', 'han', 'había', 'habían', 'he', 'hemos',
    'muy', 'más', 'menos', 'también', 'tan', 'tanto',
    'todo', 'toda', 'todos', 'todas', 'cada',
    'desde', 'hasta', 'sobre', 'entre', 'bajo', 'durante',
    'ya', 'aún', 'aun', 'siempre', 'nunca', 'jamás',
    'yo', 'tú', 'él', 'ella', 'nosotros', 'ustedes', 'ellos', 'ellas',
}

# Conteo total de temas y términos para diagnóstico
def resumen_diccionario():
    n_temas = len(DICCIONARIO_TEMATICO)
    n_terminos = sum(len(v) for v in DICCIONARIO_TEMATICO.values())
    print(f"Diccionario: {n_temas} temas, {n_terminos} términos totales")
    for tema, terminos in DICCIONARIO_TEMATICO.items():
        print(f"  {tema}: {len(terminos)} términos")

if __name__ == "__main__":
    resumen_diccionario()