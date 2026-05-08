# Her henter vi verktøyene vi trenger fra bibliotekene
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3

# Her lager vi selve appen, alt skjer gjennom denne
app = FastAPI()

# Denne funksjonen åpner en forbindelse til databasefilen
# Vi kaller den hver gang vi vil lese eller skrive data
def get_connection():
    return sqlite3.connect("database.db")

# Dette kjører én gang når serveren starter
# Lager tabellen hvis den ikke finnes fra før
with get_connection() as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS elements (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, type TEXT)")

# Dette er oppskriften på hvordan et notat skal se ut
# FastAPI sjekker automatisk at dataene er riktige
class Element(BaseModel):
    title: str
    content: str
    type: str

# Denne kjører når nettleseren sender et notat til /lagre
# Den tar imot notatet og lagrer det i databasen
@app.post("/lagre")
def lagre(data: Element):
    with get_connection() as conn:
        conn.execute("INSERT INTO elements (title, content, type) VALUES (?,?,?)", (data.title, data.content, data.type))
        conn.commit()
    return {"status": "ok"}

# Denne kjører når nettleseren ber om alle notater fra /hent
# Den henter alle rader fra databasen og sender dem tilbake som JSON
@app.get("/hent")
def hent():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, title, content, type FROM elements")
        return [{"id": r[0], "title": r[1], "content": r[2], "type": r[3]} for r in cur.fetchall()]

# Denne kjører når nettleseren vil slette et notat
# {item_id} er ID-en til notatet som skal slettes
@app.delete("/slett/{item_id}")
def slett_punkt(item_id: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM elements WHERE id = ?", (item_id,))
        conn.commit()
    return {"status": "slettet"}

# Denne sender index.html til brukeren når de går til forsiden
@app.get("/")
def main():
    return FileResponse('public/index.html')

# Denne gjør at CSS og andre filer er tilgjengelige i nettleseren
app.mount("/", StaticFiles(directory="public"), name="static")