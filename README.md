# Text Analyzer NLP

A text analysis tool for literary works that performs natural language processing using spaCy, stopwords removal, and statistical analysis. Originally developed as a university project for the subject "Programacion" at Universidad Distrital Francisco Jose de Caldas.

## Features

- **Text Normalization** — Unicode normalization, accent removal, punctuation stripping using regular expressions.
- **Character Frequency Analysis** — Histogram generation for letter frequency distribution and word length distribution.
- **Lexical Statistics** — Word count, unique word count, top 100 most frequent words.
- **Multilingual Stopwords Removal** — Stopword filtering supporting English, Spanish, French, Portuguese, and German using the `stopwordsiso` library.
- **Language Detection** — Automatic language identification among five supported languages.
- **Named Entity Recognition** — Character identification using spaCy's NER models with automatic model selection based on detected language (Spanish, English, French, German).
- **Location Extraction** — Place name identification for Spanish-language texts.

## Requirements

- Python 3.7+
- spaCy with language models:
  - `es_core_news_sm`
  - `en_core_web_sm`
  - `de_core_news_sm`
  - `fr_core_news_sm`
- Additional dependencies listed in `requirements.txt`:
  - matplotlib
  - stopwordsiso
  - spacy
  - unicodedata

## Installation

```bash
pip install matplotlib stopwordsiso spacy
python -m spacy download es_core_news_sm
python -m spacy download en_core_web_sm
python -m spacy download de_core_news_sm
python -m spacy download fr_core_news_sm
```

## Usage

```bash
python principal_program.py
```

The program will prompt for a text file path. The input file should contain a literary work in plain text format. The output includes:

- Letter count and word count
- Letter frequency histogram
- Word length histogram
- Top 100 most frequent words
- Top 50 non-stopwords
- Named entity recognition results (characters and their frequency)
- Main character identification (top 3)

## Project Structure

```
text-analyzer-nlp/
├── fmodule.py              # Core NLP module with analysis functions
├── principal_program.py    # Command-line entry point
├── README.md
└── requirements.txt
```

## Module Functions

| Function | Description |
|----------|-------------|
| `txt_normalized()` | Text normalization (accents, punctuation, special characters) |
| `count_letters()` | Total letter count excluding whitespace |
| `count_words()` | Total word count |
| `frecuency_histogram()` | Letter frequency bar chart |
| `histogram_wordslen()` | Word length distribution chart |
| `frecuency_words()` | Top 100 most frequent words |
| `diferent_words()` | Unique vocabulary size |
| `identify_language()` | Language detection from text metadata |
| `frecuency_nonstopwords()` | Top 50 frequent words excluding stopwords |
| `identify_characters()` | NER-based character identification using spaCy |
| `principal_characters()` | Top 3 main characters by mention frequency |
| `places()` | Location entity extraction |
| `temporality()` | Temporal context detection (incomplete) |

## License

This project is licensed under the MIT License.
