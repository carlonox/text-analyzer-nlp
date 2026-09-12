"""
Text analysis module with natural language processing.

Provides functions for normalization, statistical analysis,
language detection, entity recognition, and visualization
of literary texts. Originally designed as a university project
for the Programming course at Universidad Distrital FJC.

Dependencies:
    - matplotlib: histogram generation
    - stopwordsiso: multilingual stopword filtering
    - spacy: language model for NER (Named Entity Recognition)
"""
import matplotlib.pyplot as plt
import stopwordsiso as stp
import string
import spacy
import re

from unicodedata import normalize

# Common words per language for basic detection.
# Used as a fallback when langdetect is not available.
LANGUAGE_MARKERS = {
    'es': {'el', 'la', 'los', 'las', 'de', 'que', 'y', 'a', 'en', 'un', 'una', 'por', 'con', 'para', 'es', 'su'},
    'en': {'the', 'and', 'of', 'to', 'in', 'is', 'that', 'it', 'for', 'with', 'on', 'are', 'be', 'was', 'by'},
    'fr': {'le', 'la', 'de', 'et', 'est', 'que', 'dans', 'sur', 'pour', 'avec', 'les', 'des', 'une', 'pas'},
    'pt': {'o', 'a', 'de', 'que', 'e', 'do', 'da', 'em', 'para', 'com', 'por', 'os', 'as', 'se', 'na'},
    'de': {'der', 'die', 'das', 'und', 'ist', 'von', 'mit', 'auf', 'fur', 'den', 'dem', 'ein', 'eine'},
}

# spaCy model cache to avoid reloading it on every call
_nlp_cache = {}


def _clean_gutenberg_header(text):
    """
    Removes the Project Gutenberg license header.

    Project Gutenberg texts include an extensive legal block before the
    literary content. This block interferes with the analysis because it
    introduces entities (Gutenberg, License, Foundation, etc.) that do not
    belong to the work. The function detects the start of the literary text
    via the 'START OF' marker and discards everything before it.

    Args:
        text (str): Full text including the header.

    Returns:
        str: Text starting at the beginning of the work, or the original
             text if the start marker is not found.
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
    Removes the Project Gutenberg footer.

    Like the header, the footer contains licensing information that is
    not part of the literary work.

    Args:
        text (str): Full text including the footer.

    Returns:
        str: Text up to (but not including) the end marker, or the
             original text if the marker is not found.
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
    Preprocesses the text by removing license headers and special
    characters.

    Performs three operations in order:
    1. Removes the Project Gutenberg header
    2. Removes the Project Gutenberg footer
    3. Removes special symbols (trademarks, copyright, etc.)

    Args:
        text (str): Raw input text.

    Returns:
        str: Clean text ready for analysis.
    """
    text = _clean_gutenberg_header(text)
    text = _clean_gutenberg_footer(text)
    # Remove common special symbols (TM, (R), (C), etc.)
    text = re.sub(r'[\u2122\u00ae\u00a9\u2120\u00a7\u00b6]', '', text)
    return text


def txt_normalized(file):
    """
    Normalizes the text by removing accents, punctuation marks, and
    special characters through Unicode decomposition.

    Used as preprocessing in most analysis functions to guarantee
    consistent results.

    Args:
        file (str): Text to normalize.

    Returns:
        str: Normalized text without accents or punctuation.
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
    Removes only the punctuation marks from the text.

    Unlike txt_normalized, this function preserves accents and the
    original characters. Useful in functions that require analysis
    without altering the vocabulary.

    Args:
        file (str): Input text.

    Returns:
        str: Text without punctuation marks.
    """
    return file.translate(str.maketrans({key: None for key in string.punctuation}))


def count_letters(file):
    """
    Computes the total number of letters in the text, excluding spaces.

    Args:
        file (str): Previously normalized text.

    Returns:
        int: Number of alphabetic characters in the text.
    """
    return len(file) - file.count(" ")


def count_words(file):
    """
    Computes the total number of words in the text.

    Args:
        file (str): Previously normalized text.

    Returns:
        int: Word count.
    """
    return len(file.split())


def frecuency_histogram(file):
    """
    Generates a bar histogram with the frequency of each letter of the
    alphabet (a-z) in the text.

    Shows the character distribution to identify patterns such as the
    most used letters in the language of the text. The numeric values
    are printed to the console for debugging.

    Args:
        file (str): Normalized text.

    Returns:
        str: Confirmation message that the histogram was generated.
    """
    file = file.lower()
    alphabet = [chr(x) for x in range(97, 123)]
    freq = {}
    for char in file:
        if char in alphabet:
            freq[char] = freq.get(char, 0) + 1
    freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

    # Console output for debugging
    print('\n\tLetter frequency:')
    for letra, count in freq.items():
        bar = '█' * max(1, count // 10)
        print(f'\t  {letra}: {count:5d} {bar}')

    plt.figure(figsize=(8, 5))
    plt.bar(freq.keys(), freq.values())
    plt.title('Character frequency histogram')
    plt.xlabel('Characters')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()
    return '\n\tHistogram generated.'


def histogram_wordslen(file):
    """
    Generates a histogram with the lengths of the 50 longest words in
    the text. Helps identify the lexical complexity of the work.
    The numeric values are printed to the console for debugging.

    Args:
        file (str): Normalized text.

    Returns:
        str: Confirmation message that the histogram was generated.
    """
    words = file.lower().split()
    word_lengths = {}
    for word in words:
        if word not in word_lengths:
            word_lengths[word] = len(word)
    word_lengths = dict(
        sorted(word_lengths.items(), key=lambda item: item[1], reverse=True)[:50]
    )

    # Console output for debugging
    print('\n\tLength of the 50 longest words:')
    for word, length in word_lengths.items():
        bar = '█' * min(length, 40)
        print(f'\t  {word[:25]:25s} {length:2d} {bar}')

    plt.figure(figsize=(10, 5))
    plt.bar(word_lengths.keys(), word_lengths.values())
    plt.xlabel('Words')
    plt.ylabel('Length')
    plt.title('Word length distribution')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    return '\n\tHistogram generated.'


def frecuency_words(file):
    """
    Gets the 100 most frequent words in the text.

    Args:
        file (str): Normalized text.

    Returns:
        str: Comma-separated list of the 100 most frequent words.
    """
    words = file.lower().split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))
    return ', '.join(list(freq.keys())[:100])


def diferent_words(file):
    """
    Computes the number of distinct words in the text.
    Also known as unique vocabulary or lexical richness.

    Args:
        file (str): Normalized text.

    Returns:
        int: Number of unique words in the text.
    """
    return len(set(file.lower().split()))


def identify_language(text):
    """
    Detects the language of the text by comparing the frequency of
    common words.

    Compares the presence of characteristic words from each supported
    language (Spanish, English, French, Portuguese, German) and selects
    the one with the highest match count.

    Args:
        text (str): Input text.

    Returns:
        str: Name of the detected language, or 'Not available' if it
             could not be determined.
    """
    words = text.lower().split()
    if not words:
        return 'Not available'

    scores = {}
    for lang, markers in LANGUAGE_MARKERS.items():
        scores[lang] = sum(1 for w in words if w in markers)

    if not scores:
        return 'Not available'

    max_score = max(scores.values())
    if max_score == 0:
        return 'Not available'

    detected = max(scores, key=scores.get)

    lang_map = {
        'es': 'Spanish',
        'en': 'English',
        'fr': 'French',
        'pt': 'Portuguese',
        'de': 'German'
    }
    # Basic confidence check: if the score is below 0.5% of the text,
    # the detection is probably not reliable
    confidence = max_score / len(words)
    if confidence < 0.005:
        return 'Not available'

    return lang_map.get(detected, 'Not available')


def frecuency_nonstopwords(file):
    """
    Gets the 50 most frequent words in the text, excluding stopwords
    in five languages.

    Stopwords are function words (articles, prepositions, conjunctions)
    that appear frequently but carry little meaning. Removing them
    reveals the topic words.

    Args:
        file (str): Normalized text without punctuation.

    Returns:
        str: Comma-separated list of the 50 most relevant words.
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
    Loads and returns the spaCy model that matches the text language.

    Models are cached in the global _nlp_cache variable to avoid
    reloading them on consecutive calls to the NER functions.

    Args:
        text (str): Text used to determine the language.

    Returns:
        tuple: (nlp_model, detected_language)
    """
    language = identify_language(text)
    model_map = {
        'Spanish': 'es_core_news_sm',
        'German': 'de_core_news_sm',
        'French': 'fr_core_news_sm',
    }
    model_name = model_map.get(language, 'en_core_web_sm')

    if model_name not in _nlp_cache:
        _nlp_cache[model_name] = spacy.load(model_name)

    return _nlp_cache[model_name], language


def identify_characters(text):
    """
    Identifies the characters in the text using named entity
    recognition (NER) with spaCy.

    Processes the text with the appropriate language model for the
    detected language and extracts the entities labeled as PERSON.
    Ignores mentions of 'Project Gutenberg' that are false positives
    from the legal header.

    Args:
        text (str): Full text of the work.

    Returns:
        dict: Dictionary with character names as keys and their
              frequency of appearance as values, sorted from highest
              to lowest frequency.
    """
    # Apply preprocessing to clean Gutenberg headers
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
    Gets the 3 most mentioned characters in the text.

    Args:
        text (str): Full text of the work.

    Returns:
        list: List of tuples (name, frequency) for the top 3.
    """
    characters = identify_characters(text)
    return list(characters.items())[:3]


def places(text):
    """
    Identifies places mentioned in the text using spaCy NER.

    Unlike the original implementation that used capitalization,
    this version uses spaCy entity recognition labeled as GPE
    (Geopolitical Entity) or LOC (Location), which significantly
    reduces false positives.

    Args:
        text (str): Full text of the work.

    Returns:
        list: List of identified places, or a message if none were
              found.
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

    return locations[:50] if locations else 'No locations found'


def temporality(file):
    """
    Identifies the temporality of the work.

    Pending full implementation. The original idea was to classify the
    work as: before the contemporary age, contemporary, or futuristic,
    through analysis of the vocabulary and temporal references.

    Args:
        file (str): Text of the work (not currently used).

    Returns:
        str: Message indicating that the functionality is in development.
    """
    return 'Not available'
