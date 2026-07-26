import matplotlib.pyplot as plt
import stopwordsiso as stp
import string
import spacy 
import re

from unicodedata import normalize 

### 
def txt_normalized(file):
    '''
    __Se utiliza en la mayor parte de las funciones__
    - Retorna el documento sin los signos de puntuación.
    - Retorna el documento sin los acentos y otros tipos de particularidades de las letras.
        - Ej: letras cómo: â, ê, î... entre otros.
    '''
    file = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize("NFD", file), 0, re.I)
    file = normalize('NFC', file)
    file = file.translate(str.maketrans({key: None for key in string.punctuation}))
    return file

def txt_without_punctuation(file):
    '''
    __Se utiliza en funciones específicas__
    - Retorna el documento sin signos de puntuación.
    '''
    file = file.translate(str.maketrans({key: None for key in string.punctuation}))
    return file
### 

def count_letters(file):
    '''
    - Retorna el conteo de letras de todo el texto.
    '''
    spaces = file.count(" ")
    letters = len(file)
    return (letters - spaces)

def count_words(file):
    '''
    - Retorna el conteo de palabras de todo el texto.
    '''
    file = file.split()
    return len(file)

def frecuency_histogram(file):
    '''
    - Cálcula y retorna un histograma de las letras más frecuentes.
    '''
    file = file.lower()
    alphabet = [chr(x) for x in range(97, 123)]
    frecuency = dict()
    for obj in file:
        if obj not in frecuency and obj in alphabet:
            frecuency[obj] = 1
        elif obj in alphabet:
            frecuency[obj] = frecuency[obj] + 1
    frecuency = dict(sorted(frecuency.items(), key=lambda item:item[1], reverse=True))
    #Histograma
    letr = list(frecuency.keys())
    val = list(frecuency.values())
    plt.figure(figsize=(8, 5))
    plt.bar(letr, val)
    plt.title('Histograma de frecuencia de caracteres')
    plt.xlabel('Caracteres')
    plt.ylabel('Frecuencia')
    plt.show()
    return '.'

def histogram_wordslen(file):
    '''
    - Cálcula y retorna un histograma basado en el largo de las palabras.
    __Sólo las primeras 50 palabras más largas__
    '''
    file = file.lower()
    file = file.split()
    result = dict()
    for i in file:
        if i not in result:
            result[i] = len(i)
    result = dict(sorted(result.items(), key=lambda item:item[1], reverse=True))

    # Histograma
    letrs = list(result.keys())
    letrs = [i for i in letrs[0:50]]
    large = list(result.values())
    large = [i for i in large[0:50]]
    
    plt.figure(figsize=(10, 5))
    plt.bar(letrs, large)
    plt.bar(letrs, large)
    plt.xlabel('Tamaño de las palabras')
    plt.ylabel('Cantidad de apariciones')
    plt.title('Longitud de las palabras en el texto')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    return '.'

def frecuency_words(file):
    '''
    - Cálcula y retorna las 100 palabras más frecuentes en el texto.
    '''
    file = file.lower()
    file = file.split()
    frecuency = dict()
    for obj in file:
        if obj not in frecuency:
            frecuency[obj] = 1
        else:
            frecuency[obj] = frecuency[obj] + 1
    frecuency = dict(sorted(frecuency.items(), key=lambda item:item[1], reverse=True))
    result = str()
    count = 0 
    for obj in frecuency.keys():
        if count < 100:
            result += f'{obj}, '
            count += 1
        else:
            break
    return result[:-2]

def diferent_words(file):
    '''
    - Cálcula y retorna la cantidad de palabras distintas en el texto.
    '''
    file = file.lower()
    file = file.split()
    words = []
    result = -1
    for obj in file:
        if obj not in words and obj != '\n':
            result += 1
            words.append(obj)
    return result

def identify_language(file):
    '''
    - Indetifíca y retorna el lenguaje en el que se encuentra redactado el texto.
    ''' 
    file = file.split()
    if 'Language' in file:
        language = file[file.index('Language') + 1]
    else:
        return 'Not available'
    
    if language == 'English':
        return 'Inglés'
    elif language == 'Spanish':
        return 'Español'
    elif language == 'French':
        return 'Francés'
    elif language == 'Portuguese':
        return 'Portugués'
    elif language == 'German':
        return 'Alemán'
    else:
        return 'Language not supported'

def frecuency_nonstopwords(file):
    '''
    - Cálcula y retorna las 50 palabras más frecuentes, que no corresponden a Stop Words
    dentro del texto.
    '''
    stopwords = stp.stopwords(['en', 'es', 'fr', 'pt', 'de'])
    file = file.lower()
    file = file.split()
    frecuency = dict()
    for obj in file:
        if obj not in frecuency and obj not in stopwords:
            frecuency[obj] = 1
        elif obj not in stopwords:
            frecuency[obj] = frecuency[obj] + 1
    frecuency = dict(sorted(frecuency.items(), key=lambda item:item[1], reverse=True))
    result = str()
    count = 0 
    for obj in frecuency.keys():
        if count < 50:
            result += f'{obj}, '
            count += 1
        else:
            break
    return result[:-2] 

def identify_characters(texto):
    '''
    Identifica y retorna a todos los personajes del texto.
    '''
    
    
    language = identify_language(texto)

    if language == "Español":
        nlp = spacy.load("es_core_news_sm")
    elif language == "Alemán":
        nlp = spacy.load("de_core_news_sm")
    elif language == "Francés":
        nlp = spacy.load("fr_core_news_sm")
    else:
        nlp = spacy.load("en_core_web_sm")

    texto = texto.replace("\n", " ")  # Reemplazar saltos de línea con espacios
    doc = nlp(txt_normalized(texto))  # Utiliza txt_normalized para procesar el texto

    personajes = {}

    # Frase específica a ignorar
    frase_a_ignorar = "Project Gutenberg"
    nombre = ""
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            nombre = ent.text
            # Verifica si la frase a ignorar no está en el nombre
            if frase_a_ignorar not in nombre:
                if nombre in personajes:
                    personajes[nombre] += 1
                else:
                    personajes[nombre] = 1

    personajes = dict(sorted(personajes.items(), key=lambda item: item[1], reverse=True))

    print("Personajes identificados:")
    for personaje, frecuencia in personajes.items():
        print(f"{personaje}: {frecuencia} veces")

   
    return personajes  # Ahora se retorna el diccionario de personajes


def principal_characters(file):
    '''
    - Indetifíca y retorna los personajes principales del texto.
    '''
     # Obtener los personajes del texto.
    personajes = identify_characters(file)

    # Obtener los 3 personajes más frecuentes.
    principales = list(personajes.items())[:3]

    # Convertir a lista.
    principales = list(principales)

    return principales

def places(read):
    '''
    __Sólo disponible obras en español__
    - Identifíca y retorna los lugares que se mencionan dentro del texto.
    '''
    file = read.split()
    language = identify_language(" ".join(file))
    if language == 'Español':
        mayus_letters = [chr(x) for x in range(65, 91)]
        file = file.split()
        places = list()
        for i in file:
            if i[0] in mayus_letters and i not in identify_characters(file):
                places.append(i)
        return places
    else:
        return 'Not available'
    
def temporality(file):
    '''
    __Sólo disponible obras en español__
    - Identifíca y retorna la temporalidad en la que transcurre el texto.
        - Anterior a la edad contemporánea
        - En la edad contemporánea
        - Obra futurista
    '''
    if identify_language(file) == 'Español':
        return None
    else:
        return 'Not available'
     
