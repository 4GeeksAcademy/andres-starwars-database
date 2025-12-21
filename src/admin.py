import os
from flask_admin import Admin
from models import db, User, Characters, Planets, Vehicles, FavoriteCharacters, FavoritePlanets, FavoriteVehicles
from flask_admin.contrib.sqla import ModelView


class UserModelView(ModelView):
    column_auto_select_related = True
    column_list = ['user_id', 'email', 'password', 'username', 'first_name',
                   'last_name', 'favorite_characters', 'favorite_planets', 'favorite_vehicles']


class CharactersModelView(ModelView):
    column_auto_select_related = True
    column_list = ['character_id', 'name', 'gender',
                   'height', 'weight', 'birthdate', 'favorite_by']


class PlanetsModelView(ModelView):
    column_auto_select_related = True
    column_list = ['planet_id', 'planet_name', 'climate', 'terrain',
                   'day_length_hours', 'year_length_days', 'population', 'favorite_by']


class VehiclesModelView(ModelView):
    column_auto_select_related = True
    column_list = ['vehicle_id', 'vehicle_name', 'cargo_capacity',
                   'number_passengers', 'number_crew', 'model', 'cost', 'favorite_by']


class FavoriteCharactersModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'user_id', 'user', 'character_id', 'character']


class FavoritePlanetsModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'user_id', 'user', 'planet_id', 'planet']


class FavoriteVehiclesModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'user_id', 'user', 'vehicle_id', 'vehicle']


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(CharactersModelView(Characters, db.session))
    admin.add_view(PlanetsModelView(Planets, db.session))
    admin.add_view(VehiclesModelView(Vehicles, db.session))
    admin.add_view(FavoriteCharactersModelView(FavoriteCharacters, db.session))
    admin.add_view(FavoritePlanetsModelView(FavoritePlanets, db.session))
    admin.add_view(FavoriteVehiclesModelView(FavoriteVehicles, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
