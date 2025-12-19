from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(20),nullable=False)
    last_name: Mapped[str]= mapped_column(String(20),nullable=False)
    favorite_characters:Mapped[list['FavoriteCharacters']] = relationship(back_populates='user')
    favorite_planets:Mapped[list['FavoritePlanets']] = relationship(back_populates='user')
    favorite_vehicles:Mapped[list['FavoriteVehicles']] = relationship(back_populates='user')

class Characters(db.Model):
    __tablename__ = 'characters'
    character_id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(40),nullable=False)
    gender:Mapped[str] = mapped_column(String(10))
    height:Mapped[int] = mapped_column(Integer)
    weigth:Mapped[int] = mapped_column(Integer)
    birthdate:Mapped[str] = mapped_column(String(20))
    favorite_by:Mapped[list['FavoriteCharacters']] = relationship(back_populates='character')

class Planets(db.Model):
    __tablename__ = 'planets'
    planet_id:Mapped[int] = mapped_column(primary_key=True)
    planet_name:Mapped[str] = mapped_column(String(20))
    climate:Mapped[str] = mapped_column(String(20))
    terrain:Mapped[str] = mapped_column(String(20))
    day_length_hours: Mapped[int] = mapped_column(Integer)
    year_length_days:Mapped[int] = mapped_column(Integer)
    population:Mapped[int] = mapped_column(Integer)
    favorite_by:Mapped[list['FavoritePlanets']] = relationship(back_populates='planet')

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    vehicle_id:Mapped[int] = mapped_column(primary_key=True)
    vehicle_name:Mapped[str] = mapped_column(String(40))
    cargo_capacity:Mapped[float] = mapped_column(Float)
    number_passengers:Mapped[int] = mapped_column(Integer)
    number_crew:Mapped[int] = mapped_column(Integer)
    model:Mapped[str] = mapped_column(String(40))
    cost:Mapped[int] = mapped_column(Integer)
    favorite_by:Mapped[list['FavoriteVehicles']] = relationship(back_populates='vehicle')

class FavoriteCharacters(db.Model):
    __tablename__ = 'favoritecharacters'
    id:Mapped[int]= mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    user:Mapped['User'] = relationship(back_populates='favorites')
    character_id:Mapped[int] = mapped_column(ForeignKey('characters.character_id'))
    character:Mapped['Characters'] = relationship(back_populates='favorite_by')

class FavoritePlanets(db.Model):
    __tablename__ = 'favoriteplanets'
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    user:Mapped['User'] = relationship(back_populates='favorite_planets')
    planet_id:Mapped[int] = mapped_column(ForeignKey('planets.planet_id'))
    planet:Mapped['Planets'] = relationship(back_populates='favorite_by')

class FavoriteVehicles(db.Model):
    __tablename__ = 'favoritevehicles'
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    user:Mapped['User'] = relationship(back_populates='favorite_vehicles')
    vehicle_id:Mapped[int] = mapped_column(ForeignKey('vehicles.vehicle_id'))
    vehicle:Mapped['Vehicles'] = relationship(back_populates='favorite_by')
