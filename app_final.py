import logging
import os
from pathlib import Path

from fastapi import Body, FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("simple_notes")

app = FastAPI(title="Простая заметка")

VERSION = "1.0.0"
NOTE_FILE = Path(__file__).with_name(
    os.getenv("NOTE_FILENAME", "note.txt")
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"version": VERSION}


@app.get("/note")
def read_note():
    if NOTE_FILE.exists():
        text = NOTE_FILE.read_text(encoding="utf-8")
    else:
        text = ""

    logger.info("Заметка прочитана")
    return {"text": text}


@app.post("/save")
def save_note(text: str = Body(embed=True)):
    NOTE_FILE.write_text(text, encoding="utf-8")
    logger.info("Заметка сохранена")
    return {"text": text}


@app.post("/clear")
def clear_note():
    NOTE_FILE.write_text("", encoding="utf-8")
    logger.info("Заметка очищена")
    return {"text": ""}