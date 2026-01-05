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
from models import db, User, Characters, Planets, Vehicles, FavoriteCharacters, FavoritePlanets, FavoriteVehicles
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


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

#                                                                       //-----User Routes-----//


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())

    return jsonify({'users': users_serialized}), 200


@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user == None:
        return jsonify({'msg': 'User does not exist'})
    else:
        serialized_user = user.serialize()
    return jsonify({'data': serialized_user}), 200


@app.route('/users', methods=['POST'])
def add_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'You must add information in the body'}), 400
    if 'email' not in body:
        return jsonify({'msg': 'Email is required'})
    if 'password' not in body:
        return jsonify({'msg': 'Password is required'})
    if 'username' not in body:
        return jsonify({'msg': 'Username is required'})
    if 'first_name' not in body:
        return jsonify({'msg': 'First name is required'})
    if 'last_name' not in body:
        return jsonify({'msg': 'Last name is required'})

    new_user = User()
    new_user.email = body['email'],
    new_user.password = body['password'],
    new_user.username = body['username'],
    new_user.first_name = body['first_name'],
    new_user.last_name = body['last_name']
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'msg': 'User added successfully'}), 201


@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'msg': 'User not found'}), 404

    body = request.get_json(silent=True)
    if 'email' in body:
        user.email = body['email']
    if 'password' in body:
        user.password = body['password']
    if 'username' in body:
        user.username = body['username']
    if 'first_name' in body:
        user.first_name = body['first_name']
    if 'last_name' in body:
        user.last_name = body['last_name']
    db.session.commit()
    return jsonify({'msg': 'User updated successfully'})


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'msg': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': 'User deleted successfully'})

#                                                                       //-----Character Routes-----//


@app.route('/people', methods=['GET'])
def get_characters():
    characters = Characters.query.all()
    characters_serialized = []
    for character in characters:
        characters_serialized.append(character.serialize())

    return jsonify({'characters': characters_serialized}), 200


@app.route('/people/<int:id>', methods=['GET'])
def get_character(id):
    character = Characters.query.get(id)
    if character == None:
        return jsonify({'msg': 'character does not exist'})
    else:
        serialized_character = character.serialize()
    return jsonify({'data': serialized_character}), 200


@app.route('/people', methods=['POST'])
def add_character():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'You must add information in the body'}), 400
    if 'name' not in body:
        return jsonify({'msg': 'Name is not optional'})
    if 'gender' not in body:
        body['gender'] = 'N/A'
    if 'height' not in body:
        return jsonify({'msg': 'Height is not optional'})
    if 'weight' not in body:
        return jsonify({'msg': 'Weight is not optional'})
    if 'birthdate' not in body:
        body['birthdate'] = 'N/A'

    new_character = Characters()
    new_character.name = body['name'],
    new_character.gender = body['gender'],
    new_character.height = body['height'],
    new_character.weight = body['weight'],
    new_character.birthdate = body['birthdate']
    db.session.add(new_character)
    db.session.commit()
    return jsonify({'msg': 'Charcater added succesfully'}), 201


@app.route('/people/<int:id>', methods=['PUT'])
def update_character(id):
    character = Characters.query.get(id)
    if character is None:
        return jsonify({'msg': 'Character not found'}), 404

    body = request.get_json(silent=True)
    if 'name' in body:
        character.name = body['name']
    if 'gender' in body:
        character.gender = body['gender']
    if 'height' in body:
        character.height = body['height']
    if 'weight' in body:
        character.weight = body['weight']
    if 'birthdate' in body:
        character.birthdate = body['birthdate']
    db.session.commit()
    return jsonify({'msg': 'Character updated successfully'}), 200


@app.route('/people/<int:id>', methods=['DELETE'])
def delete_character(id):
    character = Characters.query.get(id)
    if character is None:
        return jsonify({'msg': 'Character not found'}), 404
    db.session.delete(character)
    db.session.commit()
    return jsonify({'msg': 'Character deleted successfully'})

#                                                                       //-----Planet Routes-----//


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planets_serialized = []
    for planet in planets:
        planets_serialized.append(planet.serialize())

    return jsonify({'planets': planets_serialized}), 200


@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    planet = Planets.query.get(id)
    if planet == None:
        return jsonify({'msg': 'Planet does not exist'}), 404
    else:
        serialized_planet = planet.serialize()
        return jsonify({'data': serialized_planet})


@app.route('/planets', methods=['POST'])
def add_planet():
    body = request.get_json(silent=True)
    if 'planet_name' not in body:
        return jsonify({'msg': 'Planet name is required'})
    if 'climate' not in body:
        body['climate'] = 'N/A'
    if 'terrain' not in body:
        body['terrain'] = 'N/A'
    if 'day_length_hours' not in body:
        body['day_length_hours'] = 0
    if 'year_length_days' not in body:
        body['year_length_days'] = 0
    if 'population' not in body:
        body['population'] = 0

    new_planet = Planets()
    new_planet.planet_name = body['planet_name'],
    new_planet.climate = body['climate'],
    new_planet.terrain = body['terrain'],
    new_planet.day_length_hours = body['day_length_hours'],
    new_planet.year_length_days = body['year_length_days'],
    new_planet.population = body['population'],
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({'msg': 'Planet added successfully'}), 201


@app.route('/planets/<int:id>', methods=['PUT'])
def update_planet(id):
    planet = Planets.query.get(id)
    if planet is None:
        return jsonify({'msg': 'Planet not found'}), 404

    body = request.get_json(silent=True)
    if 'planet_name' in body:
        planet.planet_name = body['planet_name']
    if 'climate' in body:
        planet.climate = body['climate']
    if 'terrain' in body:
        planet.terrain = body['terrain']
    if 'day_length_hours' in body:
        planet.day_length_hours = body['day_length_hours']
    if 'year_length_days' in body:
        planet.year_length_days = body['year_length_days']
    if 'population' in body:
        planet.population = body['population']
    db.session.commit()
    return jsonify({'msg': 'Planet updated successfully'})


@app.route('/planets/<int:id>', methods=['DELETE'])
def delete_planet(id):
    planet = Planets.query.get(id)
    if planet is None:
        return jsonify({'msg': 'Planet not found'}), 404
    db.session.delete(planet)
    db.session.commit()
    return jsonify({'msg': 'Planet deleted successfully'})

#                                                                       //-----Vehicle Routes-----//


@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicles.query.all()
    vehicles_serialized = []
    for vehicle in vehicles:
        vehicles_serialized.append(vehicle.serialize())
    return jsonify({'vehicles': vehicles_serialized}), 200


@app.route('/vehicles/<int:id>', methods=['GET'])
def get_vehicle(id):
    vehicle = Vehicles.query.get(id)
    if vehicle == None:
        return jsonify({'msg': 'Vehicle does not exist'}), 404
    else:
        vehicle_serialized = vehicle.serialize()
        return jsonify({'data': vehicle_serialized})


@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    body = request.get_json(silent=True)
    if 'vehicle_name' not in body:
        return jsonify({'msg': 'Vehicle name is required'}), 400
    if 'cargo_capacity' not in body:
        body['cargo_capacity'] = 0
    if 'number_passengers' not in body:
        body['number_passengers'] = 0
    if 'number_crew' not in body:
        body['number_crew'] = 1
    if 'model' not in body:
        body['model'] = 'N/A'
    if 'cost' not in body:
        body['cost'] = 0

    new_vehicle = Vehicles()
    new_vehicle.vehicle_name = body['vehicle_name'],
    new_vehicle.cargo_capacity = body['cargo_capacity'],
    new_vehicle.number_passengers = body['number_passengers'],
    new_vehicle.number_crew = body['number_crew'],
    new_vehicle.model = body['model'],
    new_vehicle.cost = body['cost']

    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify({'msg': 'Vehicle added successfully'}), 201


@app.route('/vehicles/<int:id>', methods=['PUT'])
def update_vehicle(id):
    vehicle = Vehicles.query.get(id)
    if vehicle is None:
        return jsonify({'msg': 'Vehicle not found'}), 404

    body = request.get_json(silent=True)
    if 'vehicle_name' in body:
        vehicle.vehicle_name = body['vehicle_name']
    if 'cargo_capacity' in body:
        vehicle.cargo_capacity = body['cargo_capacity']
    if 'number_passengers' in body:
        vehicle.number_passengers = body['number_passengers']
    if 'number_crew' in body:
        vehicle.number_crew = body['number_crew']
    if 'model' in body:
        vehicle.model = body['model']
    if 'cost' in body:
        vehicle.cost = body['cost']
    db.session.commit()
    return jsonify({'msg': 'Vehicle updated successfully'})


@app.route('/vehicles/<int:id>', methods=['DELETE'])
def delete_vehicle(id):
    vehicle = Vehicles.query.get(id)
    if vehicle is None:
        return jsonify({'msg': 'Vehicle not found'}), 404
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({'msg': 'Vehicle deleted successfully'})


#                                                                       //-----Favorite Characters-----//


@app.route('/favorite/people/<int:people_id>/user/<int:user_id>', methods=['POST'])
def add_favorite_character(user_id, people_id):
    user = User.query.get(user_id)
    character = Characters.query.get(people_id)
    if user is None:
        return jsonify({'msg': 'User doesnt exist'}), 404
    if character is None:
        return jsonify({'msg': 'Character doesnt exist'}), 404
    favorites = FavoriteCharacters.query.filter_by(
        user_id=user_id, character_id=people_id).all()
    if len(favorites) > 0:
        return jsonify({'msg': 'Favorite already exists'})
    new_favorite = FavoriteCharacters()
    new_favorite.user_id = user_id
    new_favorite.character_id = people_id
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({'msg': 'Favorite character added'})


@app.route('/favorite/people/<int:people_id>/user/<int:user_id>', methods=['DELETE'])
def delete_favorite_character(people_id, user_id):
    user = User.query.get(user_id)
    character = Characters.query.get(people_id)
    if user is None:
        return jsonify({'msg': 'User doesnt exist'}), 404
    if character is None:
        return jsonify({'msg': 'Character doesnt exist'}), 404
    favorites = FavoriteCharacters.query.filter_by(
        character_id=people_id, user_id=user_id).all()
    if len(favorites) == 0:
        return jsonify({'msg': 'Favorite doesnt exist'})
    db.session.delete(favorites[0])
    db.session.commit()
    return jsonify({'msg': 'Favorite character deleted successfully'})


#                                                                       //-----Favorite Planets-----//

@app.route('/favorite/planets/<int:planet_id>/user/<int:user_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    planet = Characters.query.get(planet_id)
    if user is None:
        return jsonify({'msg': 'User doesnt exist'}), 404
    if planet is None:
        return jsonify({'msg': 'Character doesnt exist'}), 404
    favorites = FavoritePlanets.query.filter_by(
        user_id=user_id, planet_id=planet_id).all()
    if len(favorites) > 0:
        return jsonify({'msg': 'Favorite already exists'})
    new_favorite = FavoritePlanets()
    new_favorite.user_id = user_id
    new_favorite.planet_id = planet_id
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({'msg': 'Favorite planet added'})


@app.route('/favorite/planets/<int:planet_id>/user/<int:user_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id, user_id):
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)
    if user is None:
        return jsonify({'msg': 'User doesnt exist'}), 404
    if planet is None:
        return jsonify({'msg': 'planet doesnt exist'}), 404
    favorites = FavoritePlanets.query.filter_by(
        planet_id=planet_id, user_id=user_id).all()
    if len(favorites) == 0:
        return jsonify({'msg': 'Favorite does not exist'}), 404
    db.session.delete(favorites[0])
    db.session.commit()
    return jsonify({'msg': 'Favorite planet deleted successfully'})


#                                                                       //-----Favorite Vehicles-----//

@app.route('/favorite/vehicles/<int:vehicle_id>/user/<int:user_id>', methods=['POST'])
def add_favorite_vehicle(user_id, vehicle_id):
    user = User.query.get(user_id)
    vehicle = Characters.query.get(vehicle_id)
    if user is None:
        return jsonify({'msg': 'User doesnt exist'}), 404
    if vehicle is None:
        return jsonify({'msg': 'Vehicle doesnt exist'}), 404
    favorites = FavoriteVehicles.query.filter_by(
        user_id=user_id, vehicle_id=vehicle_id).all()
    print(favorites)
    if len(favorites) > 0:
        return jsonify({'msg': 'Favorite already exists'})

    new_favorite = FavoriteVehicles()
    new_favorite.user_id = user_id
    new_favorite.vehicle_id = vehicle_id
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({'msg': 'Favorite vehicle added'})


@app.route('/favorite/vehicles/<int:vehicle_id>/user/<int:user_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id, user_id):
    user = User.query.get(user_id)
    vehicle = Vehicles.query.get(vehicle_id)
    if user is None:
        return jsonify({'msg': 'User doesnt exist'}), 404
    if vehicle is None:
        return jsonify({'msg': 'vehicle doesnt exist'}), 404
    favorites = FavoriteVehicles.query.filter_by(
        vehicle_id=vehicle_id, user_id=user_id).all()
    if len(favorites) == 0:
        return jsonify({'msg': 'Favorite doesnt exist'})
    db.session.delete(favorites[0])
    db.session.commit()
    return jsonify({'msg': 'Favorite vehicle deleted successfully'})


#                                                                       //-----All favorites-----//

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'User not found'}), 404
    favorite_characters_serialized = []
    for favorite in user.favorite_characters:
        favorite_characters_serialized.append(favorite.character.serialize())
    favorite_planets_serialized = []
    for favorite in user.favorite_planets:
        favorite_planets_serialized.append(favorite.planet.serialize())
    favorite_vehicles_serialized = []
    for favorite in user.favorite_vehicles:
        favorite_vehicles_serialized.append(favorite.vehicle.serialize())
    return jsonify({'favorite_characters': favorite_characters_serialized,
                   'favorite_planets': favorite_planets_serialized,
                    'favorite_vehicles': favorite_vehicles_serialized}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
