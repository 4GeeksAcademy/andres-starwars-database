from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(20), nullable=False)
    last_name: Mapped[str] = mapped_column(String(20), nullable=False)
    favorite_characters: Mapped[list['FavoriteCharacters']] = relationship(
        back_populates='user')
    favorite_planets: Mapped[list['FavoritePlanets']
                             ] = relationship(back_populates='user')
    favorite_vehicles: Mapped[list['FavoriteVehicles']
                              ] = relationship(back_populates='user',cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'

    def serialize(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name
        }


class Characters(db.Model):
    __tablename__ = 'characters'
    character_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    gender: Mapped[str] = mapped_column(String(10))
    height: Mapped[int] = mapped_column(Integer)
    weight: Mapped[int] = mapped_column(Integer)
    birthdate: Mapped[str] = mapped_column(String(20))
    favorite_by: Mapped[list['FavoriteCharacters']
                        ] = relationship(back_populates='character',cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.name}'

    def serialize(self):
        return {
            'character_id': self.character_id,
            'name': self.name,
            'gender': self.gender,
            'height': self.height,
            'weight': self.weight,
            'birthdate': self.birthdate
        }


class Planets(db.Model):
    __tablename__ = 'planets'
    planet_id: Mapped[int] = mapped_column(primary_key=True)
    planet_name: Mapped[str] = mapped_column(String(20))
    climate: Mapped[str] = mapped_column(String(20))
    terrain: Mapped[str] = mapped_column(String(20))
    day_length_hours: Mapped[int] = mapped_column(Integer)
    year_length_days: Mapped[int] = mapped_column(Integer)
    population: Mapped[int] = mapped_column(Integer)
    favorite_by: Mapped[list['FavoritePlanets']
                        ] = relationship(back_populates='planet',cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.planet_name}'

    def serialize(self):
        return {
            'planet_id': self.planet_id,
            'planet_name': self.planet_name,
            'climate': self.climate,
            'terrain': self.terrain,
            'day_length_hours': self.day_length_hours,
            'year_length_days': self.year_length_days,
            'population': self.population
        }


class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    vehicle_id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_name: Mapped[str] = mapped_column(String(40))
    cargo_capacity: Mapped[float] = mapped_column(Float)
    number_passengers: Mapped[int] = mapped_column(Integer)
    number_crew: Mapped[int] = mapped_column(Integer)
    model: Mapped[str] = mapped_column(String(40))
    cost: Mapped[int] = mapped_column(Integer)
    favorite_by: Mapped[list['FavoriteVehicles']
                        ] = relationship(back_populates='vehicle',cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.vehicle_name}'

    def serialize(self):
        return {
            'vehicle_id': self.vehicle_id,
            'vehicle_name': self.vehicle_name,
            'cargo_capacity': self.cargo_capacity,
            'number_passengers': self.number_passengers,
            'number_crew': self.number_crew,
            'model': self.model,
            'cost': self.cost
        }


class FavoriteCharacters(db.Model):
    __tablename__ = 'favoritecharacters'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    user: Mapped['User'] = relationship(back_populates='favorite_characters')
    character_id: Mapped[int] = mapped_column(
        ForeignKey('characters.character_id'))
    character: Mapped['Characters'] = relationship(
        back_populates='favorite_by')

    def __repr__(self):
        return f'{self.user} likes {self.character}'

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'character_id': self.character_id
        }


class FavoritePlanets(db.Model):
    __tablename__ = 'favoriteplanets'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    user: Mapped['User'] = relationship(back_populates='favorite_planets')
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.planet_id'))
    planet: Mapped['Planets'] = relationship(back_populates='favorite_by')

    def __repr__(self):
        return f'{self.user} likes {self.planet}'

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'planet_id': self.planet_id
        }


class FavoriteVehicles(db.Model):
    __tablename__ = 'favoritevehicles'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    user: Mapped['User'] = relationship(back_populates='favorite_vehicles')
    vehicle_id: Mapped[int] = mapped_column(ForeignKey('vehicles.vehicle_id'))
    vehicle: Mapped['Vehicles'] = relationship(back_populates='favorite_by')

    def __repr__(self):
        return f'{self.user} likes the {self.vehicle}'

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'vehicle_id': self.vehicle_id
        }
