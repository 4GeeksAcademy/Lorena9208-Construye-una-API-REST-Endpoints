import os
from flask_admin import Admin
from models import db, User, Pokemon, Pokeball, FavoritePokemon, FavoritePokeball
from flask_admin.contrib.sqla import ModelView


class FavoritePokemonAdmin(ModelView):
    column_list = ("id", "user.first_name", "pokemon.name")
    column_labels = {
        "user.first_name": "User",
        "pokemon.name": "Pokemon"
    }
    column_searchable_list = ("user.first_name", "pokemon.name")


class FavoritePokeballAdmin(ModelView):
    column_list = ("id", "user.first_name", "pokeball.name")
    column_labels = {
        "user.first_name": "User",
        "pokeball.name": "Pokeball"
    }
    column_searchable_list = ("user.first_name", "pokeball.name")


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Pokemon, db.session))
    admin.add_view(ModelView(Pokeball, db.session))
    admin.add_view(FavoritePokemonAdmin(FavoritePokemon, db.session))
    admin.add_view(FavoritePokeballAdmin(FavoritePokeball, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
