# Wise Syllabifier

A robust Python-based tool for splitting Nepali words into syllables. This project provides both a command-line interface and a high-performance REST API using FastAPI.

## Features

- **Accurate Syllabification**: Correctly handles complex Nepali compound letters and modifiers.
- **FastAPI Integration**: Includes a ready-to-use web server with interactive API documentation.
- **CLI Support**: Simple command-line tool for quick testing.
- **Lightweight**: Minimal dependencies.

## Installation

1. Clone the repository.

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Command Line Interface (CLI)

You can use the interactive CLI to syllabify words directly in your terminal.

```bash
python main.py
```

**Example Output:**
```text
--- Nepali Syllabifier (Type 'exit' to quit) ---

Enter text: राष्ट्रियताको
Original: राष्ट्रियताको
Syllables: ['रा', 'ष्ट्रि', 'य', 'ता', 'को']
```

### 2. Web API (FastAPI)

Start the API server:

```bash
python api.py
# OR
uvicorn api:app --reload
```

The server will start at `http://127.0.0.1:8000`.

#### API Endpoints

- **GET /syllabify**: `http://127.0.0.1:8000/syllabify?text=नेपाल`
- **POST /syllabify**: Submit text via form data.

### 3. Interactive Documentation

Once the server is running, visit the interactive API docs (Swagger UI) at:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 4. Python Library

You can import the `SyllableTokenizer` directly into your own Python scripts.

```python
from syllabifier.syllable_tokenizer import SyllableTokenizer

text = "काठमाडौँ"
boundaries = SyllableTokenizer.find_all_boundaries(text)
print(boundaries)
# Output: ['का', 'ठ', 'मा', 'डौँ']
```

## Testing

Run the included unit tests to ensure everything is working correctly:

```bash
python -m unittest discover tests
```

## Credits & Inspiration

This project is a Python implementation inspired by the work found at:
[https://github.com/santabasnet](https://github.com/santabasnet)

Special thanks to the open-source community for their contributions to Nepali NLP.
