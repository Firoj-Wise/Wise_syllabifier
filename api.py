from fastapi import FastAPI, Form, HTTPException
from syllabifier.syllable_tokenizer import SyllableTokenizer
import uvicorn

app = FastAPI(
    title="Nepali Syllabifier API",
    description="API for splitting Nepali words into syllables.",
    version="1.0.0"
)

# 1. GET Endpoint (Easy for browser testing)
# Usage: http://localhost:8000/syllabify?text=राष्ट्रियताको
@app.get("/syllabify")
def syllabify_get(text: str):
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
        
    boundaries = SyllableTokenizer.find_all_boundaries(text)
    return {
        "original": text,
        "syllables": boundaries,
        "count": len(boundaries)
    }

# 2. POST Endpoint (Using Form for simple input in Docs)
# This renders a simple text box in Swagger UI instead of a JSON schema.
@app.post("/syllabify")
def syllabify_post(text: str = Form(..., description="Enter Nepali text to syllabify")):
    """
    Syllabifies the input text.
    """
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    boundaries = SyllableTokenizer.find_all_boundaries(text)
    return {
        "original": text,
        "syllables": boundaries,
        "count": len(boundaries)
    }

if __name__ == "__main__":
    # Run the server
    uvicorn.run(app, host="127.0.0.1", port=8000)