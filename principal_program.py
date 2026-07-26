"""
Analizador de texto literario con procesamiento de lenguaje natural.

Punto de entrada del programa. Solicita un archivo de texto,
lo procesa y muestra los resultados del analisis estadistico
y linguistico.

Uso:
    python principal_program.py
"""
import fmodule as fm
import os
import sys


def main():
    """Ejecuta el flujo principal de analisis de texto."""
    intro = os.listdir()
    fname = input('Ingrese la lectura a analizar: ')

    for intento in range(2):
        if fname in intro:
            break
        print('El documento ingresado no se encuentra.')
        print('Recuerde ingresar el formato del texto al final (.txt).')
        if intento == 1:
            print('Segundo fallo. Saliendo de la aplicacion...')
            sys.exit(1)
        fname = input('Ingrese de nuevo la lectura a analizar: ')

    if not fname.lower().endswith('.txt'):
        print('Formato de documento no admitido.')
        sys.exit(1)

    with open(fname, encoding='utf-8') as fh:
        raw_text = fh.read()

    # Preprocesar: eliminar encabezados de Gutenberg y simbolos especiales
    text = fm.preprocess_text(raw_text)

    # Versiones normalizadas para diferentes analisis
    read = fm.txt_normalized(text)
    particular_read = fm.txt_without_punctuation(text)

    print('\nA continuacion los resultados del analisis:\n')
    print(f'El numero de caracteres es: {fm.count_letters(read)}')
    print(f'El numero de palabras es: {fm.count_words(read)}')
    print(f'Histograma de letras{fm.frecuency_histogram(particular_read)}')
    print(f'Histograma de palabras{fm.histogram_wordslen(particular_read)}')

    print('Las 100 palabras mas frecuentes son:')
    print(f'\tR/ {fm.frecuency_words(read)}.')
    print(f'Existen {fm.diferent_words(read)} palabras diferentes.')
    print(f'El lenguaje del texto es: {fm.identify_language(read)}.')

    print('Las 50 palabras mas frecuentes sin stopwords:')
    print(f'\tR/ {fm.frecuency_nonstopwords(particular_read)}.')

    print('Personajes identificados:')
    personajes = fm.identify_characters(raw_text)
    for nombre, freq in personajes.items():
        print(f'\t{nombre}: {freq} veces')

    print('\nPersonajes principales:')
    for nombre, freq in fm.principal_characters(raw_text):
        print(f'\t{nombre}: {freq} veces')

    print('Lugares encontrados:')
    lugares = fm.places(raw_text)
    if isinstance(lugares, list):
        for lugar in lugares:
            print(f'\t- {lugar}')
    else:
        print(f'\t{lugares}')

    print(f'Temporalidad de la obra: {fm.temporality(read)}.')


if __name__ == '__main__':
    main()
