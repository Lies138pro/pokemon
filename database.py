from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Crée une connexion à la base de données SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./pokemon.db"  # Assure-toi que le fichier pokemon.db est bien là

# Crée l'objet de moteur SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Crée la base
Base = declarative_base()

# Crée la session locale pour interagir avec la base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Définition du modèle Pokémon avec SQLAlchemy
class Pokemon(Base):
    __tablename__ = "pokemons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)

# Crée les tables dans la base de données
Base.metadata.create_all(bind=engine)
