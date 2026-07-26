# Analizador de texto basado en Python, usando sus principios basicos
import fmodule as fm
import os
import sys


def main():
    intro = os.listdir()

    fname = input('Ingrese la lectura a analizar: ')

    # Verificar si el archivo existe
    for intento in range(2):
        if fname in intro:
            break
        print('El documento ingresado no se encuentra,')
        print('recuerde ingresar el formato del texto al final (.txt).')
        if intento == 1:
            print('Segundo fallo en el ingreso del documento.')
            print('Saliendo de la aplicacion...')
            sys.exit(1)
        fname = input('Ingrese de nuevo la lectura a analizar: ')

    # Verificar extension
    if not fname.lower().endswith('.txt'):
        print('Formato de documento no admitido.')
        print('Saliendo de la aplicacion...')
        sys.exit(1)

    # Leer y analizar
    with open(fname, encoding='utf8') as file_object:
        file = file_object.read()

    read = fm.txt_normalized(file)
    particular_read = fm.txt_without_punctuation(file)

    print('\nA continuacion los resultados del analisis:\n')

    print(f'El numero de caracteres es: {fm.count_letters(read)}')
    print(f'El numero de palabras es: {fm.count_words(read)}')
    print(f'Histograma de letras{fm.frecuency_histogram(particular_read)}')
    print(f'Histograma de palabras{fm.histogram_wordslen(particular_read)}')

    print(f'Las 100 palabras mas frecuentes son:')
    print(f'\tR/ {fm.frecuency_words(read)}.')
    print(f'Existen {fm.diferent_words(read)} palabras diferentes.')
    print(f'El lenguaje del texto es: {fm.identify_language(read)}.')

    print(f'Las 50 palabras mas frecuentes que no corresponden a Stop Words, son:')
    print(f'\tR/ {fm.frecuency_nonstopwords(particular_read)}.')

    print('Los personajes y las veces que aparecen son:')
    fm.identify_characters(read)

    print(f'Los personajes principales son:')
    print(f'\tR/ {fm.principal_characters(read)}')
    print(f'Los lugares que hay en la obra son:')
    print(f'\tR/ {fm.places(file)}')
    print(f'El tiempo en que transcurre la obra es: {fm.temporality(read)}.')


if __name__ == '__main__':
    main()
