"""
Modulo de analisis de texto con procesamiento de lenguaje natural.

Proporciona funciones para normalizacion, analisis estadistico,
deteccion de idioma, reconocimiento de entidades y visualizacion
de textos literarios. Disenado originalmente como proyecto universitario
para la materia Programacion en la Universidad Distrital FJC.

Dependencias:
    - matplotlib: generacion de histogramas
    - stopwordsiso: filtrado de palabras vacias multilingue
    - spacy: modelo de lenguaje para NER (Named Entity Recognition)
"""
import matplotlib.pyplot as plt
import stopwordsiso as stp
import string
import spacy
import re

from unicodedata import normalize

# Palabras comunes por idioma para deteccion basica.
# Se usa como fallback cuando no se dispone de langdetect.
LANGUAGE_MARKERS = {
    'es': {'el', 'la', 'los', 'las', 'de', 'que', 'y', 'a', 'en', 'un', 'una', 'por', 'con', 'para', 'es', 'su'},
    'en': {'the', 'and', 'of', 'to', 'in', 'is', 'that', 'it', 'for', 'with', 'on', 'are', 'be', 'was', 'by'},
    'fr': {'le', 'la', 'de', 'et', 'est', 'que', 'dans', 'sur', 'pour', 'avec', 'les', 'des', 'une', 'pas'},
    'pt': {'o', 'a', 'de', 'que', 'e', 'do', 'da', 'em', 'para', 'com', 'por', 'os', 'as', 'se', 'na'},
    'de': {'der', 'die', 'das', 'und', 'ist', 'von', 'mit', 'auf', 'fur', 'den', 'dem', 'ein', 'eine'},
}

# Cache del modelo de spaCy para evitar recargarlo en cada llamada
_nlp_cache = {}


def _clean_gutenberg_header(text):
    """
    Elimina el encabezado de licencia de Project Gutenberg.

    Los textos de Project Gutenberg incluyen un bloque legal extenso
    antes del contenido literario. Este bloque interfiere con el analisis
    porque introduce entidades (Gutenberg, License, Foundation, etc.)
    que no pertenecen a la obra. La funcion detecta el inicio del texto
    literario mediante la marca 'START OF' y descarta todo lo anterior.

    Args:
        text (str): Texto completo incluyendo el encabezado.

    Returns:
        str: Texto a partir del inicio de la obra, o el texto original
             si no se encuentra la marca de inicio.
    """
    start_marker = re.search(
        r'\*\*\* START OF (THIS|THE) (PROJECT|GUTENBERG).*?\*\*\*',
        text,
        re.IGNORECASE
    )
    if start_marker:
        return text[start_marker.end():]
    return text


def _clean_gutenberg_footer(text):
    """
    Elimina el pie de pagina de Project Gutenberg.

    Similar al encabezado, el pie contiene informacion de licencia
    que no forma parte de la obra literaria.

    Args:
        text (str): Texto completo incluyendo el pie.

    Returns:
        str: Texto hasta antes de la marca de fin, o el texto original
             si no se encuentra la marca.
    """
    end_marker = re.search(
        r'\*\*\* END OF (THIS|THE) (PROJECT|GUTENBERG).*?\*\*\*',
        text,
        re.IGNORECASE
    )
    if end_marker:
        return text[:end_marker.start()]
    return text


def preprocess_text(text):
    """
    Preprocesa el texto eliminando encabezados de licencia y caracteres especiales.

    Realiza tres operaciones en orden:
    1. Elimina el encabezado de Project Gutenberg
    2. Elimina el pie de pagina de Project Gutenberg
    3. Elimina simbolos especiales (marcas registradas, copyright, etc.)

    Args:
        text (str): Texto crudo de entrada.

    Returns:
        str: Texto limpio listo para analisis.
    """
    text = _clean_gutenberg_header(text)
    text = _clean_gutenberg_footer(text)
    # Eliminar simbolos especiales comunes (TM, (R), (C), etc.)
    text = re.sub(r'[\u2122\u00ae\u00a9\u2120\u00a7\u00b6]', '', text)
    return text


def txt_normalized(file):
    """
    Normaliza el texto eliminando acentos, signos de puntuacion y
    caracteres especiales mediante descomposicion Unicode.

    Se utiliza como preprocesamiento en la mayoria de las funciones
    de analisis para garantizar consistencia en los resultados.

    Args:
        file (str): Texto a normalizar.

    Returns:
        str: Texto normalizado sin acentos ni puntuacion.
    """
    file = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+",
        r"\1",
        normalize("NFD", file),
        0,
        re.I
    )
    file = normalize('NFC', file)
    file = file.translate(str.maketrans({key: None for key in string.punctuation}))
    return file


def txt_without_punctuation(file):
    """
    Elimina solo los signos de puntuacion del texto.

    A diferencia de txt_normalized, esta funcion conserva los acentos
    y caracteres originales. Util en funciones donde se requiere
    analisis sin alteracion del vocabulario.

    Args:
        file (str): Texto de entrada.

    Returns:
        str: Texto sin signos de puntuacion.
    """
    return file.translate(str.maketrans({key: None for key in string.punctuation}))


def count_letters(file):
    """
    Calcula el numero total de letras del texto, excluyendo espacios.

    Args:
        file (str): Texto previamente normalizado.

    Returns:
        int: Cantidad de caracteres alfabeticos en el texto.
    """
    return len(file) - file.count(" ")


def count_words(file):
    """
    Calcula el numero total de palabras del texto.

    Args:
        file (str): Texto previamente normalizado.

    Returns:
        int: Cantidad de palabras.
    """
    return len(file.split())


def frecuency_histogram(file):
    """
    Genera un histograma de barras con la frecuencia de cada letra
    del alfabeto (a-z) en el texto.

    Muestra la distribucion de caracteres para identificar patrones
    como las letras mas usadas en el idioma del texto. Los valores
    numericos se imprimen en consola para debug.

    Args:
        file (str): Texto normalizado.

    Returns:
        str: Mensaje de confirmacion de generacion del histograma.
    """
    file = file.lower()
    alphabet = [chr(x) for x in range(97, 123)]
    freq = {}
    for char in file:
        if char in alphabet:
            freq[char] = freq.get(char, 0) + 1
    freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

    # Salida en consola para debug
    print('\n\tFrecuencia de letras:')
    for letra, count in freq.items():
        bar = '█' * max(1, count // 10)
        print(f'\t  {letra}: {count:5d} {bar}')

    plt.figure(figsize=(8, 5))
    plt.bar(freq.keys(), freq.values())
    plt.title('Histograma de frecuencia de caracteres')
    plt.xlabel('Caracteres')
    plt.ylabel('Frecuencia')
    plt.tight_layout()
    plt.show()
    return '\n\tHistograma generado.'


def histogram_wordslen(file):
    """
    Genera un histograma con la longitud de las 50 palabras mas largas
    del texto. Permite identificar la complejidad lexica de la obra.
    Los valores numericos se imprimen en consola para debug.

    Args:
        file (str): Texto normalizado.

    Returns:
        str: Mensaje de confirmacion de generacion del histograma.
    """
    words = file.lower().split()
    word_lengths = {}
    for word in words:
        if word not in word_lengths:
            word_lengths[word] = len(word)
    word_lengths = dict(
        sorted(word_lengths.items(), key=lambda item: item[1], reverse=True)[:50]
    )

    # Salida en consola para debug
    print('\n\tLongitud de las 50 palabras mas largas:')
    for word, length in word_lengths.items():
        bar = '█' * min(length, 40)
        print(f'\t  {word[:25]:25s} {length:2d} {bar}')

    plt.figure(figsize=(10, 5))
    plt.bar(word_lengths.keys(), word_lengths.values())
    plt.xlabel('Palabras')
    plt.ylabel('Longitud')
    plt.title('Longitud de las palabras en el texto')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    return '\n\tHistograma generado.'


def frecuency_words(file):
    """
    Obtiene las 100 palabras mas frecuentes en el texto.

    Args:
        file (str): Texto normalizado.

    Returns:
        str: Lista separada por comas de las 100 palabras mas frecuentes.
    """
    words = file.lower().split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))
    return ', '.join(list(freq.keys())[:100])


def diferent_words(file):
    """
    Calcula la cantidad de palabras distintas en el texto.
    Tambien conocido como vocabulario unico o riqueza lexica.

    Args:
        file (str): Texto normalizado.

    Returns:
        int: Numero de palabras unicas en el texto.
    """
    return len(set(file.lower().split()))


def identify_language(text):
    """
    Detecta el idioma del texto mediante comparacion de frecuencia
    de palabras comunes.

    Compara la presencia de palabras caracteristicas de cada idioma
    soportado (espanol, ingles, frances, portugues, aleman) y
    selecciona el que tenga mayor coincidencia.

    Args:
        text (str): Texto de entrada.

    Returns:
        str: Nombre del idioma detectado en espanol, o 'Not available'
             si no se pudo determinar.
    """
    words = text.lower().split()
    if not words:
        return 'No disponible'

    scores = {}
    for lang, markers in LANGUAGE_MARKERS.items():
        scores[lang] = sum(1 for w in words if w in markers)

    if not scores:
        return 'No disponible'

    max_score = max(scores.values())
    if max_score == 0:
        return 'No disponible'

    detected = max(scores, key=scores.get)

    lang_map = {
        'es': 'Espanol',
        'en': 'Ingles',
        'fr': 'Frances',
        'pt': 'Portugues',
        'de': 'Aleman'
    }
    # Confianza basica: si el score es menor a 0.5% del texto
    # probablemente la deteccion no es confiable
    confidence = max_score / len(words)
    if confidence < 0.005:
        return 'No disponible'

    return lang_map.get(detected, 'No disponible')


def frecuency_nonstopwords(file):
    """
    Obtiene las 50 palabras mas frecuentes del texto excluyendo
    stopwords (palabras vacias) en cinco idiomas.

    Las stopwords son palabras funcionales (articulos, preposiciones,
    conjunciones) que aparecen con frecuencia pero aportan poco
    significado. Al eliminarlas, se revelan las palabras tematicas.

    Args:
        file (str): Texto normalizado sin puntuacion.

    Returns:
        str: Lista separada por comas de las 50 palabras mas relevantes.
    """
    stopwords = stp.stopwords(['en', 'es', 'fr', 'pt', 'de'])
    words = file.lower().split()
    freq = {}
    for word in words:
        if word not in stopwords:
            freq[word] = freq.get(word, 0) + 1
    freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))
    return ', '.join(list(freq.keys())[:50])


def _get_nlp_model(text):
    """
    Carga y retorna el modelo de spaCy adecuado segun el idioma del texto.

    Los modelos se cachean en la variable global _nlp_cache para evitar
    recargarlos en llamadas consecutivas a funciones de NER.

    Args:
        text (str): Texto para determinar el idioma.

    Returns:
        tuple: (modelo_nlp, idioma_detectado)
    """
    language = identify_language(text)
    model_map = {
        'Espanol': 'es_core_news_sm',
        'Aleman': 'de_core_news_sm',
        'Frances': 'fr_core_news_sm',
    }
    model_name = model_map.get(language, 'en_core_web_sm')

    if model_name not in _nlp_cache:
        _nlp_cache[model_name] = spacy.load(model_name)

    return _nlp_cache[model_name], language


def identify_characters(text):
    """
    Identifica los personajes del texto usando reconocimiento de
    entidades nombradas (NER) con spaCy.

    Procesa el texto con el modelo linguistico adecuado segun el
    idioma detectado y extrae las entidades etiquetadas como PERSON.
    Ignora menciones a 'Project Gutenberg' que son falsos positivos
    del encabezado legal.

    Args:
        text (str): Texto completo de la obra.

    Returns:
        dict: Diccionario con nombres de personajes como claves y
              su frecuencia de aparicion como valores, ordenado de
              mayor a menor frecuencia.
    """
    # Aplicar preprocesamiento para limpiar encabezados de Gutenberg
    cleaned_text = preprocess_text(text)
    cleaned_text = cleaned_text.replace("\n", " ")

    nlp, _ = _get_nlp_model(cleaned_text)
    doc = nlp(txt_normalized(cleaned_text))

    characters = {}
    ignore_phrases = {"project gutenberg", "gutenberg", "license", "trademark"}

    for ent in doc.ents:
        if ent.label_ != "PERSON":
            continue

        name_lower = ent.text.lower()
        if any(phrase in name_lower for phrase in ignore_phrases):
            continue

        characters[ent.text] = characters.get(ent.text, 0) + 1

    return dict(
        sorted(characters.items(), key=lambda item: item[1], reverse=True)
    )


def principal_characters(text):
    """
    Obtiene los 3 personajes mas mencionados en el texto.

    Args:
        text (str): Texto completo de la obra.

    Returns:
        list: Lista de tuplas (nombre, frecuencia) de los 3 principales.
    """
    characters = identify_characters(text)
    return list(characters.items())[:3]


def places(text):
    """
    Identifica lugares mencionados en el texto mediante NER con spaCy.

    A diferencia de la implementacion original que usaba mayusculas,
    esta version utiliza el reconocimiento de entidades de spaCy
    etiquetadas como GPE (Geopolitical Entity) o LOC (Location),
    lo que reduce significativamente los falsos positivos.

    Args:
        text (str): Texto completo de la obra.

    Returns:
        list: Lista de lugares identificados, o mensaje si no se
              encontraron.
    """
    cleaned_text = preprocess_text(text)

    nlp, language = _get_nlp_model(cleaned_text)
    doc = nlp(cleaned_text)

    locations = []
    seen = set()
    for ent in doc.ents:
        if ent.label_ in ("GPE", "LOC") and ent.text not in seen:
            locations.append(ent.text)
            seen.add(ent.text)

    return locations[:50] if locations else 'No se encontraron lugares'


def temporality(file):
    """
    Identifica la temporalidad de la obra.

    Pendiente de implementacion completa. La idea original era
    clasificar la obra en: anterior a la edad contemporanea,
    contemporanea, o futurista, mediante analisis del vocabulario
    y referencias temporales.

    Args:
        file (str): Texto de la obra (no utilizado actualmente).

    Returns:
        str: Mensaje indicando que la funcionalidad esta en desarrollo.
    """
    return 'No disponible'
