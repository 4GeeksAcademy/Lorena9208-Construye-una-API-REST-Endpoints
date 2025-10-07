from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Text, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()



class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    age: Mapped[int] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(String(10), nullable=True)
    subscription_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)


    favorite_pokemons: Mapped[list["FavoritePokemon"]] = relationship("FavoritePokemon", back_populates="user")
    favorite_pokeballs: Mapped[list["FavoritePokeball"]] = relationship("FavoritePokeball", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "gender": self.gender,
            "subscription_date": self.subscription_date.isoformat()
        }



class Pokemon(db.Model):
    __tablename__ = "pokemons"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text)

    favorites: Mapped[list["FavoritePokemon"]] = relationship("FavoritePokemon", back_populates="pokemon")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "description": self.description
        }



class Pokeball(db.Model):
    __tablename__ = "pokeballs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    effect: Mapped[str] = mapped_column(Text)

    favorites: Mapped[list["FavoritePokeball"]] = relationship("FavoritePokeball", back_populates="pokeball")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "effect": self.effect
        }



class FavoritePokemon(db.Model):
    __tablename__ = "favorite_pokemons"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemons.id"))

    user: Mapped["User"] = relationship("User", back_populates="favorite_pokemons")
    pokemon: Mapped["Pokemon"] = relationship("Pokemon", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "pokemon_id": self.pokemon_id
        }



class FavoritePokeball(db.Model):
    __tablename__ = "favorite_pokeballs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    pokeball_id: Mapped[int] = mapped_column(ForeignKey("pokeballs.id"))

    user: Mapped["User"] = relationship("User", back_populates="favorite_pokeballs")
    pokeball: Mapped["Pokeball"] = relationship("Pokeball", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "pokeball_id": self.pokeball_id
        }