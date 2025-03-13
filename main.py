from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, Pokemon
import sqlite3  # ✅ Importation de SQLite au début

app = FastAPI()

# Dépendance pour la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modèle Pydantic pour les requêtes
class PokemonSchema(BaseModel):
    name: str
    type: str

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Pokémon !"}

# Endpoint pour ajouter un Pokémon
@app.post("/pokemons/")
def create_pokemon(pokemon: PokemonSchema, db: Session = Depends(get_db)):
    new_pokemon = Pokemon(name=pokemon.name, type=pokemon.type)
    db.add(new_pokemon)
    db.commit()
    db.refresh(new_pokemon)
    return {"message": f"Pokémon {new_pokemon.name} ajouté avec succès !"}

# Endpoint pour lister tous les Pokémon
@app.get("/pokemons/")
def get_pokemons(db: Session = Depends(get_db)):
    pokemons = db.query(Pokemon).all()
    return pokemons

# Endpoint pour filtrer les Pokémon par type
@app.get("/pokemons/{type}")
def get_pokemons_by_type(type: str, db: Session = Depends(get_db)):
    pokemons = db.query(Pokemon).filter(Pokemon.type == type).all()
    return pokemons

# Endpoint pour supprimer un Pokémon par son nom
@app.delete("/pokemons/{name}")
def delete_pokemon(name: str, db: Session = Depends(get_db)):
    pokemon = db.query(Pokemon).filter(Pokemon.name == name).first()
    if pokemon:
        db.delete(pokemon)
        db.commit()
        return {"message": f"Pokémon {name} supprimé avec succès !"}
    return {"error": "Pokémon non trouvé"}