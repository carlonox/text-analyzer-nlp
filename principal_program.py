"""
Literary text analyzer with natural language processing.

Program entry point. Prompts for a text file, processes it,
and displays the results of the statistical and linguistic
analysis.

Usage:
    python principal_program.py
"""
import fmodule as fm
import os
import sys


def main():
    """Runs the main text analysis flow."""
    intro = os.listdir()
    fname = input('Enter the text file to analyze: ')

    for intento in range(2):
        if fname in intro:
            break
        print('The specified file was not found.')
        print('Remember to include the .txt extension at the end.')
        if intento == 1:
            print('Second failure. Exiting the application...')
            sys.exit(1)
        fname = input('Enter the text file again: ')

    if not fname.lower().endswith('.txt'):
        print('Unsupported file format.')
        sys.exit(1)

    with open(fname, encoding='utf-8') as fh:
        raw_text = fh.read()

    # Preprocess: remove Gutenberg headers and special symbols
    text = fm.preprocess_text(raw_text)

    # Normalized versions for the different analyses
    read = fm.txt_normalized(text)
    particular_read = fm.txt_without_punctuation(text)

    print('\nAnalysis results:\n')
    print(f'Number of characters: {fm.count_letters(read)}')
    print(f'Number of words: {fm.count_words(read)}')
    print(f'Letter histogram{fm.frecuency_histogram(particular_read)}')
    print(f'Word histogram{fm.histogram_wordslen(particular_read)}')

    print('The 100 most frequent words are:')
    print(f'\t{fm.frecuency_words(read)}.')
    print(f'There are {fm.diferent_words(read)} different words.')
    print(f'The language of the text is: {fm.identify_language(read)}.')

    print('The 50 most frequent words without stopwords:')
    print(f'\t{fm.frecuency_nonstopwords(particular_read)}.')

    print('Identified characters:')
    personajes = fm.identify_characters(raw_text)
    for nombre, freq in personajes.items():
        print(f'\t{nombre}: {freq} times')

    print('\nMain characters:')
    for nombre, freq in fm.principal_characters(raw_text):
        print(f'\t{nombre}: {freq} times')

    print('Places found:')
    lugares = fm.places(raw_text)
    if isinstance(lugares, list):
        for lugar in lugares:
            print(f'\t- {lugar}')
    else:
        print(f'\t{lugares}')

    print(f'Temporality of the work: {fm.temporality(read)}.')


if __name__ == '__main__':
    main()
