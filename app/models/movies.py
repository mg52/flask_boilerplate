"""Data models."""
from .. import db
from .actor_movie_relations import ActorMovieRelationsModel
import json


class MoviesModel(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    year = db.Column(db.Integer)
    actor_movie_relations = db.relationship("ActorMovieRelationsModel", backref="moviesModel", lazy='dynamic')

    def __init__(self, name, year):
        self.name = name
        self.year = year

    def __repr__(self):
        return f"<Movie {self.name}>"
