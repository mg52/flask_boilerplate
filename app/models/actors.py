"""Data models."""
from .. import db
from .actor_movie_relations import ActorMovieRelationsModel
import json


class ActorsModel(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    age = db.Column(db.Integer())
    actor_movie_relations = db.relationship("ActorMovieRelationsModel", backref="actorsModel", lazy='dynamic')

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"<Actor {self.name}>"

