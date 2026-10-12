from pathlib import Path

from fastapi import Body, FastAPI

app = FastAPI(title="Простая заметка")

NOTE_FILE = Path(__file__).with_name("note.txt")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/note")
def read_note():
    if NOTE_FILE.exists():
        text = NOTE_FILE.read_text(encoding="utf-8")
    else:
        text = ""
    return {"text": text}


@app.post("/save")
def save_note(text: str = Body(embed=True)):
    NOTE_FILE.write_text(text, encoding="utf-8")
    return {"text": text}


@app.post("/clear")
def clear_note():
    NOTE_FILE.write_text("", encoding="utf-8")
    return {"text": ""}