# Todo notater
# Beskrivelse

# En enkel web-applikasjon for å holde styr på hverdagen. Den er delt i to seksjoner: en for vanlige notater og en for To do lister med # sjekkbokser. Alle data lagres i en SQLite-database.

Installasjon og oppstart av server

Installer nødvendige biblioteker:


Start serveren fra terminalen:

skriv 
# pip install fastapi uvicorn



så skriv 
# uvicorn server:app --reload

Hvordan starte klienten

trykk på linken command + trykk 
ELLER
Gå til adressen: http://127.0.0.1:8000

Eksempler på bruk av API

Appen bruker følgende endepunkter for å snakke med databasen:

POST /lagre: Sender tittel, innhold og type (notat/todo) til serveren.

GET /hent: Henter alle lagrede elementer fra databasen.

DELETE /slett/{id}: Sletter et spesifikt notat eller liste ved bruk av dens ID.