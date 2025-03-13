from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel

app = FastAPI()

# Modèle de données pour un Pokémon
class Pokemon(BaseModel):
    name: str
    type: str

# Connexion à la base SQLite
def get_db_connection():
    conn = sqlite3.connect("pokemon.db")
    conn.row_factory = sqlite3.Row
    return conn

# Route pour ajouter un Pokémon
@app.post("/pokemons")
def add_pokemon(pokemon: Pokemon):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pokemons (name, type) VALUES (?, ?)", (pokemon.name, pokemon.type))
    conn.commit()
    conn.close()
    return {"message": f"Pokémon {pokemon.name} ajouté avec succès!"}