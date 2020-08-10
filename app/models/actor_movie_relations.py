"""Data models."""
from .. import db
import json


class ActorMovieRelationsModel(db.Model):
    __tablename__ = 'actor_movie_relations'

    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'))
    actor = db.relationship('ActorsModel')
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    movie = db.relationship('MoviesModel')

    def __init__(self, actor_id, movie_id):
        self.actor_id = actor_id
        self.movie_id = movie_id

    def __repr__(self):
        return f"<Actor Movie Relation {self.id}>"
