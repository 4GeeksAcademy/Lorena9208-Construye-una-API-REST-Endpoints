"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Pokemon, Pokeball, FavoritePokemon, FavoritePokeball
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


def commit_and_serialize(obj):
    db.session.add(obj)
    db.session.commit()
    return jsonify(obj.serialize()), 201


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users])


@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.serialize())


@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(email=data["email"],
                password=data.get('password'),
                first_name=data["first_name"],
                last_name=data.get("last_name"),
                age=data.get("age"),
                gender=data.get("gender"), is_active=data.get("is_active", True))
    return commit_and_serialize(user)


@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json
    user.email = data.get("email", user.email)
    user.is_active = data.get("is_active", user.is_active)
    db.session.commit()
    return jsonify(user.serialize())


@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})


@app.route("/users/<int:user_id>/favorites", methods=["GET"])
def get_user_favorites(user_id):
    user = User.query.get_or_404(user_id)
    fav_pokemons = FavoritePokemon.query.filter_by(user_id=user_id).all()
    fav_pokeballs = FavoritePokeball.query.filter_by(user_id=user_id).all()
    return jsonify({
        "user": user.serialize(),
        "favorite_pokemons": [f.serialize() for f in fav_pokemons],
        "favorite_pokeballs": [f.serialize() for f in fav_pokeballs]
    })


@app.route("/users/<int:user_id>/pokemons", methods=["POST"])
def create_user_pokemon(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    pokemon = Pokemon(name=data["name"], type=data["type"],
                      description=data.get("description"))
    fav = FavoritePokemon(user=user, pokemon=pokemon)
    db.session.add_all([pokemon, fav])
    db.session.commit()
    return jsonify({
        "message": "Pokemon created and assigned to user",
        "pokemon": pokemon.serialize()
    }), 201


@app.route("/users/<int:user_id>/pokeballs", methods=["POST"])
def create_user_pokeball(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    pokeball = Pokeball(name=data["name"], effect=data.get("effect"))
    fav = FavoritePokeball(user=user, pokeball=pokeball)
    db.session.add_all([pokeball, fav])
    db.session.commit()
    return jsonify({
        "message": "Pokeball created and assigned to user",
        "pokeball": pokeball.serialize()
    }), 201


@app.route("/pokemons", methods=["GET"])
def get_pokemons():
    pokemons = Pokemon.query.all()
    return jsonify([p.serialize() for p in pokemons])


@app.route("/pokemons/<int:id>", methods=["GET"])
def get_pokemon(id):
    pokemon = Pokemon.query.get_or_404(id)
    return jsonify(pokemon.serialize())


@app.route("/pokemons", methods=["POST"])
def create_pokemon():
    data = request.json
    pokemon = Pokemon(
        name=data["name"],
        type=data["type"],
        description=data.get("description")
    )
    return commit_and_serialize(pokemon)


@app.route("/pokemons/<int:id>", methods=["PUT"])
def update_pokemon(id):
    pokemon = Pokemon.query.get_or_404(id)
    data = request.json
    pokemon.name = data.get("name", pokemon.name)
    pokemon.type = data.get("type", pokemon.type)
    pokemon.description = data.get("description", pokemon.description)
    db.session.commit()
    return jsonify(pokemon.serialize())


@app.route("/pokemons/<int:id>", methods=["DELETE"])
def delete_pokemon(id):
    pokemon = Pokemon.query.get_or_404(id)
    db.session.delete(pokemon)
    db.session.commit()
    return jsonify({"message": "Pokemon deleted"})


@app.route("/pokeballs", methods=["GET"])
def get_pokeballs():
    pokeballs = Pokeball.query.all()
    return jsonify([p.serialize() for p in pokeballs])


@app.route("/pokeballs/<int:id>", methods=["GET"])
def get_pokeball(id):
    pokeball = Pokeball.query.get_or_404(id)
    return jsonify(pokeball.serialize())


@app.route("/pokeballs", methods=["POST"])
def create_pokeball():
    data = request.json
    pokeball = Pokeball(
        name=data["name"],
        effect=data.get("effect")
    )
    return commit_and_serialize(pokeball)


@app.route("/pokeballs/<int:id>", methods=["PUT"])
def update_pokeball(id):
    pokeball = Pokeball.query.get_or_404(id)
    data = request.json
    pokeball.name = data.get("name", pokeball.name)
    pokeball.effect = data.get("effect", pokeball.effect)
    db.session.commit()
    return jsonify(pokeball.serialize())


@app.route("/pokeballs/<int:id>", methods=["DELETE"])
def delete_pokeball(id):
    pokeball = Pokeball.query.get_or_404(id)
    db.session.delete(pokeball)
    db.session.commit()
    return jsonify({"message": "Pokeball deleted"})




@app.route("/users/<int:user_id>/favorite/pokemon/<int:pokemon_id>", methods=["POST"])
def add_favorite_pokemon(user_id, pokemon_id):
    user = User.query.get_or_404(user_id)
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    exists = FavoritePokemon.query.filter_by(
        user_id=user_id, pokemon_id=pokemon_id).first()
    if exists:
        return jsonify({"message": "Pokemon already in favorites"}), 400
    fav = FavoritePokemon(user_id=user_id, pokemon_id=pokemon_id)
    return commit_and_serialize(fav)


@app.route("/users/<int:user_id>/favorite/pokeball/<int:pokeball_id>", methods=["POST"])
def add_favorite_pokeball(user_id, pokeball_id):
    user = User.query.get_or_404(user_id)
    pokeball = Pokeball.query.get_or_404(pokeball_id)
    exists = FavoritePokeball.query.filter_by(
        user_id=user_id, pokeball_id=pokeball_id).first()
    if exists:
        return jsonify({"message": "Pokeball already in favorites"}), 400
    fav = FavoritePokeball(user_id=user_id, pokeball_id=pokeball_id)
    return commit_and_serialize(fav)


@app.route("/users/<int:user_id>/favorite/pokemon/<int:pokemon_id>", methods=["DELETE"])
def remove_favorite_pokemon(user_id, pokemon_id):
    fav = FavoritePokemon.query.filter_by(
        user_id=user_id, pokemon_id=pokemon_id).first()
    if not fav:
        return jsonify({"message": "Favorite Pokemon not found"}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "Favorite Pokemon removed"})


@app.route("/users/<int:user_id>/favorite/pokeball/<int:pokeball_id>", methods=["DELETE"])
def remove_favorite_pokeball(user_id, pokeball_id):
    fav = FavoritePokeball.query.filter_by(
        user_id=user_id, pokeball_id=pokeball_id).first()
    if not fav:
        return jsonify({"message": "Favorite Pokeball not found"}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "Favorite Pokeball removed"})



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
