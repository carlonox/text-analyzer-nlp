# Analizador de texto basado en Python, usando sus principios básicos
import fmodule as fm
import os
intro = os.listdir()

fname = input('Ingrese la lectura a analizar: ')
if fname not in intro:
    print('''
    El documento ingresado no se encuentra,
    recuerde ingresar el formato del texto
    al final (.txt, .pdf, etc...).
    ''')
    
    fname = input('Ingrese de nuevo la lectura a analizar: ')
    if fname not in intro:
        print('''
    Segundo fallo en el ingreso del documento.
    Saliendo de la aplicación...
    ''')
        exit
    else:  
        point_index = fname.find('.')
        if fname[point_index:(point_index + 4)] != '.txt':
            print('''
        Formato de documento no admitido
        Saliendo de la aplicación...
        ''')
            exit

        with open(fname, encoding='utf8') as file_object:
            file = file_object.read()

            read = fm.txt_normalized(file)
            particular_read = fm.txt_without_punctuation(file)

            print(f'\nA continuación los resultdos del análisis.')
            print(f'''
    El número de caracteres es: {fm.count_letters(read)}
    El número de palabras es: {fm.count_words(read)}
    Histograma de letras{fm.frecuency_histogram(particular_read)}
    Histograma de palabras{fm.histogram_wordslen(particular_read)}
    Las 100 palabras más frecuentes son:
        R/ {fm.frecuency_words(read)}.
    Existen {fm.diferent_words(read)} palabras diferentes.
    El lenguaje del texto es: {fm.identify_language(particular_read)}.
    Las 50 palabras más frecuentes que no corresponden a Stop Words, son:
        R/ {fm.frecuency_nonstopwords(particular_read)}.
    Los personajes y las veces que aparecen son:
        R/ {fm.identify_characters(read)}
    Los personajes principales son:
        R/ {fm.principal_characters(read)}
    Los lugares que hay en la obra son:
        R/ {fm.places(read)}
    El tiempo en que trascurre la obra es: {fm.temporality(read)}.
    ''')
else:  
    point_index = fname.find('.')
    if fname[point_index:(point_index + 4)] != '.txt':
        print('''
    Formato de documento no admitido
    Saliendo de la aplicación...
    ''')
        exit

    with open(fname, encoding='utf8') as file_object:
        file = file_object.read()

        read = fm.txt_normalized(file)
        particular_read = fm.txt_without_punctuation(file)

        print(f'\nA continuación los resultados del análisis.')
        print(f'''
    El número de caracteres es: {fm.count_letters(read)}
    El número de palabras es: {fm.count_words(read)}
    Histograma de letras{fm.frecuency_histogram(particular_read)}
    Histograma de palabras{fm.histogram_wordslen(particular_read)}
    Las 100 palabras más frecuentes son:
        R/ {fm.frecuency_words(read)}.
    Existen {fm.diferent_words(read)} palabras diferentes.
    El lenguaje del texto es: {fm.identify_language(particular_read)}.
    Las 50 palabras más frecuentes que no corresponden a Stop Words, son:
        R/ {fm.frecuency_nonstopwords(particular_read)}.
    Los personajes y las veces que aparecen son:
        R/ {fm.identify_characters(read)}
    Los personajes principales son:
        R/ {fm.principal_characters(read)}
    Los lugares que hay en la obra son:
        R/ {fm.places(file)}
    El tiempo en que trascurre la obra es: {fm.temporality(read)}.
    ''')
