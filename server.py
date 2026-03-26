from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3

app = FastAPI()

def get_connection():
    return sqlite3.connect("database.db")

with get_connection() as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS elements (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, type TEXT)")

class Element(BaseModel):
    title: str
    content: str
    type: str

@app.post("/lagre")
def lagre(data: Element):
    with get_connection() as conn:
        conn.execute("INSERT INTO elements (title, content, type) VALUES (?,?,?)", (data.title, data.content, data.type))
        conn.commit()
    return {"status": "ok"}

# VIKTIG: Denne henter nå ID-en fra databasen
@app.get("/hent")
def hent():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, title, content, type FROM elements")
        return [{"id": r[0], "title": r[1], "content": r[2], "type": r[3]} for r in cur.fetchall()]

# NYTT: Denne sletter et spesifikt punkt basert på ID
@app.delete("/slett/{item_id}")
def slett_punkt(item_id: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM elements WHERE id = ?", (item_id,))
        conn.commit()
    return {"status": "slettet"}

@app.get("/")
def main():
    return FileResponse('public/index.html')

app.mount("/", StaticFiles(directory="public"), name="static")