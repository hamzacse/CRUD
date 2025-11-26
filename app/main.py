from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from models import Note, NoteCreate
from database import notes_db
import asyncio
from datetime import datetime

app = FastAPI()

# -------- Logging function --------
def write_log(message: str):
    with open("notes.log", "a") as f:
        f.write(message + "\n")


@app.get("/")
async def home():
    return {"message": "FastAPI is working with async & background tasks!"}


# -------- CREATE --------
@app.post("/notes/", response_model=Note)
async def create_note(note: NoteCreate, background_tasks: BackgroundTasks):

    await asyncio.sleep(1)

    new_id = len(notes_db) + 1
    new_note = Note(id=new_id, **note.model_dump())
    notes_db.append(new_note)

    background_tasks.add_task(
        write_log,
        f"[{datetime.now()}] Note created: {new_note.title} and {new_note.content}"
    )

    return new_note


# -------- READ ALL (with Pagination + Query params) --------
@app.get("/notes")
async def get_notes(
    page: int = 1,
    limit: int = 5,
    search: str | None = None
):
    """
    page   -> which page number
    limit  -> items per page
    search -> optional keyword filter
    
    """

    await asyncio.sleep(0.2)

    # --- APPLY SEARCH FILTER (if provided) ---
    filtered_notes = notes_db
    if search:
        filtered_notes = [
            n for n in notes_db
            if search.lower() in n.title.lower() or search.lower() in n.content.lower()
        ]

    # --- APPLY PAGINATION ---
    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total": len(filtered_notes),
        "data": filtered_notes[start:end],
    }


# -------- READ ONE --------
@app.get("/notes/{note_id}", response_model=Note)
async def read_note(note_id: int):
    await asyncio.sleep(0.2)
    for note in notes_db:
        if note.id == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")


# -------- UPDATE --------
@app.put("/notes/{note_id}", response_model=Note)
async def update_note(note_id: int, updated: NoteCreate):
    await asyncio.sleep(0.5)
    for index, note in enumerate(notes_db):
        if note.id == note_id:
            new_note = Note(id=note_id, **updated.model_dump())
            notes_db[index] = new_note
            return new_note
    raise HTTPException(status_code=404, detail="Note not found")


# -------- DELETE --------
@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    await asyncio.sleep(0.5)
    for note in notes_db:
        if note.id == note_id:
            notes_db.remove(note)
            return {"message": "Note deleted"}
    raise HTTPException(status_code=404, detail="Note not found")


# ------------------------- CUSTOM EXCEPTION HANDLERS --------------------------------


@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    """Custom JSON response for Not Found errors."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": exc.detail,
            "path": str(request.url)
        },
    )


@app.exception_handler(500)
async def custom_500_handler(request: Request, exc: Exception):
    """Handles internal server errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Server Error",
            "message": "Something went wrong!",
            "path": str(request.url),
        },
    )
