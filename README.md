# Text Analyzer NLP

A text analysis tool for literary works that performs natural language processing using spaCy, stopwords removal, and statistical analysis. Originally developed as a university project for the subject "Programacion" at Universidad Distrital Francisco Jose de Caldas, and later enhanced with production-grade improvements.

## Features

### Pre-processing
- **Gutenberg Header Removal** — Automatically strips Project Gutenberg license headers and footers that introduce false positives in entity recognition (License, Foundation, Gutenberg trademark mentions).
- **Special Character Sanitization** — Removes trademark (TM), registered (R), and copyright (C) symbols that interfere with text normalization.

### Text Statistics
- **Character Frequency Analysis** — Histogram generation for letter frequency distribution and word length distribution.
- **Lexical Statistics** — Word count, unique word count, top 100 most frequent words.
- **Multilingual Stopwords Removal** — Stopword filtering supporting English, Spanish, French, Portuguese, and German using the `stopwordsiso` library.

### Language Detection
- **Word Frequency Profiling** — Language identification by comparing text against common word markers for five languages.
- **Confidence Thresholding** — Detection only returns a result when the confidence score exceeds 0.5% of total word count, avoiding false positives on short or ambiguous texts.

### Named Entity Recognition
- **Character Identification** — NER-based character extraction using spaCy, with automatic model selection based on detected language.
- **Gutenberg Filtering** — Ignores false positive entities from license headers (Gutenberg, License, Project).
- **Location Extraction** — Place name identification using spaCy GPE/LOC entity labels instead of naive capitalization matching, drastically reducing false positives.
- **NER Model Caching** — spaCy models are loaded once and cached across function calls, avoiding redundant loading and improving performance on large texts.

### Visualization
- Letter frequency distribution histogram
- Word length distribution histogram (top 50 longest words)

## Requirements

- Python 3.7+
- spaCy with language models:
  - `es_core_news_sm` (Spanish)
  - `en_core_web_sm` (English)
  - `de_core_news_sm` (German)
  - `fr_core_news_sm` (French)
- Additional dependencies listed in `requirements.txt`

## Installation

```bash
pip install matplotlib stopwordsiso spacy
python -m spacy download es_core_news_sm
python -m spacy download en_core_web_sm
```

Optional language models:
```bash
python -m spacy download de_core_news_sm
python -m spacy download fr_core_news_sm
```

## Usage

```bash
python principal_program.py
```

The program will prompt for a text file path. Sample texts are included for testing:
- `proof_one.txt` — "Anarchy" (English, 35 KB)
- `proof_two.txt` — "Los valores literarios" (Spanish, 474 KB)

### Output

The analysis produces:
1. Letter count and word count
2. Letter frequency histogram (interactive window)
3. Word length histogram (interactive window)
4. Top 100 most frequent words
5. Unique vocabulary size
6. Detected language
7. Top 50 non-stopwords
8. Named entity recognition results (characters and their frequency)
9. Main character identification (top 3)
10. Location extraction using NER

## Project Structure

```
text-analyzer-nlp/
├── fmodule.py              # Core NLP module with analysis functions
├── principal_program.py    # Command-line entry point
├── proof_one.txt           # Sample text in English (Gutenberg)
├── proof_two.txt           # Sample text in Spanish (Gutenberg)
├── README.md
└── requirements.txt
```

## Module API

### Pre-processing

| Function | Description |
|----------|-------------|
| `preprocess_text()` | Removes Gutenberg headers/footers and special symbols |
| `txt_normalized()` | Unicode normalization (accents, punctuation, special chars) |
| `txt_without_punctuation()` | Punctuation removal only |

### Statistics

| Function | Description |
|----------|-------------|
| `count_letters()` | Total letter count excluding whitespace |
| `count_words()` | Total word count |
| `frecuency_histogram()` | Letter frequency bar chart |
| `histogram_wordslen()` | Word length distribution chart |
| `frecuency_words()` | Top 100 most frequent words |
| `diferent_words()` | Unique vocabulary size |
| `frecuency_nonstopwords()` | Top 50 frequent words excluding stopwords |

### Language and Entities

| Function | Description |
|----------|-------------|
| `identify_language()` | Language detection via common word markers |
| `identify_characters()` | NER-based character identification using spaCy |
| `principal_characters()` | Top 3 main characters by mention frequency |
| `places()` | Location extraction using spaCy GPE/LOC NER |
| `temporality()` | Temporal context detection (in development) |

### Internal

| Function | Description |
|----------|-------------|
| `_get_nlp_model()` | Cached spaCy model loader |
| `_clean_gutenberg_header()` | Gutenberg license header removal |
| `_clean_gutenberg_footer()` | Gutenberg license footer removal |

## Improvements over Original Version

- Added Gutenberg header/footer stripping to eliminate license noise from analysis
- Changed location extraction from naive capitalization matching to spaCy NER (GPE/LOC labels)
- Implemented spaCy model caching to avoid redundant loading across function calls
- Added confidence thresholding to language detection
- Added TM/R/C symbol sanitization
- Fixed `exit()` without parentheses bug causing silent failures
- Fixed `places()` crash from calling `split()` on an existing list
- Removed duplicated code in `principal_program.py`

## License

This project is licensed under the MIT License.
