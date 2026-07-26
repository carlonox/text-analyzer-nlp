import matplotlib.pyplot as plt
import stopwordsiso as stp
import string
import spacy
import re

from unicodedata import normalize

# Palabras comunes por idioma para detección básica sin depender de metadatos
LANGUAGE_MARKERS = {
    'es': {'el', 'la', 'los', 'las', 'de', 'que', 'y', 'a', 'en', 'un', 'una', 'por', 'con', 'para', 'es'},
    'en': {'the', 'and', 'of', 'to', 'in', 'is', 'that', 'it', 'for', 'with', 'on', 'are', 'be', 'was'},
    'fr': {'le', 'la', 'de', 'et', 'est', 'que', 'dans', 'sur', 'pour', 'avec', 'les', 'des', 'une', 'pas'},
    'pt': {'o', 'a', 'de', 'que', 'e', 'do', 'da', 'em', 'para', 'com', 'por', 'os', 'as', 'se', 'na'},
    'de': {'der', 'die', 'das', 'und', 'ist', 'von', 'mit', 'auf', 'für', 'den', 'dem', 'ein', 'eine'},
}


def txt_normalized(file):
    '''
    Normaliza el texto eliminando acentos, signos de puntuación y caracteres especiales.
    Se utiliza como preprocesamiento en la mayoria de las funciones.
    '''
    file = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize("NFD", file), 0, re.I)
    file = normalize('NFC', file)
    file = file.translate(str.maketrans({key: None for key in string.punctuation}))
    return file


def txt_without_punctuation(file):
    '''
    Retorna el texto eliminando solo los signos de puntuacion.
    '''
    file = file.translate(str.maketrans({key: None for key in string.punctuation}))
    return file


def count_letters(file):
    '''
    Retorna el conteo total de letras del texto (excluyendo espacios).
    '''
    spaces = file.count(" ")
    letters = len(file)
    return letters - spaces


def count_words(file):
    '''
    Retorna el conteo total de palabras del texto.
    '''
    return len(file.split())


def frecuency_histogram(file):
    '''
    Calcula y genera un histograma con la frecuencia de las letras del alfabeto.
    '''
    file = file.lower()
    alphabet = [chr(x) for x in range(97, 123)]
    frecuency = {}
    for obj in file:
        if obj not in frecuency and obj in alphabet:
            frecuency[obj] = 1
        elif obj in alphabet:
            frecuency[obj] += 1
    frecuency = dict(sorted(frecuency.items(), key=lambda item: item[1], reverse=True))

    letr = list(frecuency.keys())
    val = list(frecuency.values())
    plt.figure(figsize=(8, 5))
    plt.bar(letr, val)
    plt.title('Histograma de frecuencia de caracteres')
    plt.xlabel('Caracteres')
    plt.ylabel('Frecuencia')
    plt.show()
    return '\n\tHistograma generado.'


def histogram_wordslen(file):
    '''
    Genera un histograma con las 50 palabras mas largas del texto.
    '''
    file = file.lower().split()
    result = {}
    for i in file:
        if i not in result:
            result[i] = len(i)
    result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))

    letrs = list(result.keys())[:50]
    large = list(result.values())[:50]

    plt.figure(figsize=(10, 5))
    plt.bar(letrs, large)
    plt.xlabel('Palabras')
    plt.ylabel('Longitud')
    plt.title('Longitud de las palabras en el texto')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    return '\n\tHistograma generado.'


def frecuency_words(file):
    '''
    Retorna las 100 palabras mas frecuentes en el texto.
    '''
    file = file.lower().split()
    frecuency = {}
    for obj in file:
        frecuency[obj] = frecuency.get(obj, 0) + 1
    frecuency = dict(sorted(frecuency.items(), key=lambda item: item[1], reverse=True))
    result = ', '.join(list(frecuency.keys())[:100])
    return result


def diferent_words(file):
    '''
    Retorna la cantidad de palabras distintas en el texto.
    '''
    file = file.lower().split()
    unique = set(file)
    return len(unique)


def identify_language(text):
    '''
    Detecta el idioma del texto comparando la frecuencia de palabras comunes.
    Retorna el nombre del idioma en espanol.
    '''
    words = text.lower().split()
    if not words:
        return 'Not available'

    scores = {}
    for lang, markers in LANGUAGE_MARKERS.items():
        scores[lang] = sum(1 for w in words if w in markers)

    if not scores:
        return 'Not available'

    max_score = max(list(scores.values()))
    if max_score == 0:
        return 'Not available'

    detected = max(scores, key=scores.get)  # type: ignore

    language_map = {
        'es': 'Espanol',
        'en': 'Ingles',
        'fr': 'Frances',
        'pt': 'Portugues',
        'de': 'Aleman'
    }
    return language_map.get(detected, 'Not available')


def frecuency_nonstopwords(file):
    '''
    Retorna las 50 palabras mas frecuentes que no corresponden a Stop Words,
    soportando espanol, ingles, frances, portugues y aleman.
    '''
    stopwords = stp.stopwords(['en', 'es', 'fr', 'pt', 'de'])
    file = file.lower().split()
    frecuency = {}
    for obj in file:
        if obj not in frecuency and obj not in stopwords:
            frecuency[obj] = 1
        elif obj not in stopwords:
            frecuency[obj] += 1
    frecuency = dict(sorted(frecuency.items(), key=lambda item: item[1], reverse=True))
    return ', '.join(list(frecuency.keys())[:50])


def _get_nlp_model(text):
    '''
    Selecciona y retorna el modelo de spaCy adecuado segun el idioma detectado.
    '''
    language = identify_language(text)
    model_map = {
        'Espanol': 'es_core_news_sm',
        'Aleman': 'de_core_news_sm',
        'Frances': 'fr_core_news_sm',
    }
    model_name = model_map.get(language, 'en_core_web_sm')
    return spacy.load(model_name), language


def identify_characters(text):
    '''
    Identifica los personajes del texto usando reconocimiento de entidades (NER) con spaCy.
    Retorna un diccionario con los nombres y su frecuencia de aparicion.
    '''
    nlp, _ = _get_nlp_model(text)
    text = text.replace("\n", " ")
    doc = nlp(txt_normalized(text))

    personajes = {}
    frase_a_ignorar = "Project Gutenberg"

    for ent in doc.ents:
        if ent.label_ == "PERSON" and frase_a_ignorar not in ent.text:
            personajes[ent.text] = personajes.get(ent.text, 0) + 1

    personajes = dict(sorted(personajes.items(), key=lambda item: item[1], reverse=True))
    return personajes


def principal_characters(file):
    '''
    Retorna los 3 personajes principales (mas mencionados) del texto.
    '''
    personajes = identify_characters(file)
    return list(personajes.items())[:3]


def places(read):
    '''
    Identifica lugares mencionados en el texto (soporta espanol e ingles).
    '''
    words = read.split()
    language = identify_language(read)
    if language not in ('Espanol', 'Ingles'):
        return 'Not available'

    mayus_letters = [chr(x) for x in range(65, 91)]
    lugares = []

    for word in words:
        if word and word[0] in mayus_letters and len(word) > 2:
            lugares.append(word)

    # Eliminar duplicados preservando orden
    seen = set()
    unique_lugares = []
    for l in lugares:
        if l not in seen:
            seen.add(l)
            unique_lugares.append(l)

    return unique_lugares[:50] if unique_lugares else 'No se encontraron lugares'


def temporality(file):
    '''
    Identifica la temporalidad de la obra.
    Funcionalidad en desarrollo.
    '''
    return 'No disponible'
