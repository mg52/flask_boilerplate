"""Application routes."""
from datetime import datetime as dt
from flask import request
from .. import api, name_space4
from flask_restx import Resource, fields
from ..models.actor_movie_relations import db, ActorMovieRelationsModel
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

actor_movie_model = api.model('ActorMovieRelationModel', {
    'actor_id': fields.Integer(required=True, description='Actor Id'),
    'movie_id': fields.Integer(required=True, description='Movie Id')
})

parser = api.parser()
parser.add_argument('Authorization', location='headers')


@name_space4.route('/actor_movies')
@name_space4.expect(parser)
class ActorMovieRelationClass(Resource):
    @name_space4.expect(actor_movie_model)
    # @name_space4.doc(security=[{'oauth2': ['read', 'write']}])
    @jwt_required
    def post(self):
        """Create ActorMovieRelation Object"""
        if request.is_json:
            data = request.get_json()
            print('Authorization', request.headers.get('Authorization'))
            new_actor_movie = ActorMovieRelationsModel(actor_id=api.payload['actor_id'],
                                                       movie_id=api.payload['movie_id'])

            db.session.add(new_actor_movie)
            db.session.commit()

            return {"message": f"ActorMovieRelation {new_actor_movie.id} has been created successfully."}, 201
        else:
            return {"error": "The request payload is not in JSON format"}

    @jwt_required
    def get(self):
        """Get ActorMovieRelation Object"""
        the_header = request.headers.get('Authorization')
        print('Authorization', the_header)
        current_user = get_jwt_identity()
        print(current_user)
        actor_movies = ActorMovieRelationsModel.query.all()

        # filter example:
        # actor_movies = ActorMovieRelationsModel.query.filter(ActorMovieRelationsModel.model == 'r343f')

        results = [
            {
                "id": actor_movie.id,
                "actor_id": actor_movie.actor_id,
                "movie_id": actor_movie.movie_id,
                "actor": {"actor_name": actor_movie.actor.name, "actor_age": actor_movie.actor.age},
                "movie": {"movie_name": actor_movie.movie.name, "movie_year": actor_movie.movie.year}
            } for actor_movie in actor_movies]

        return {"count": len(results), "actor_movies": results, "message": "success"}


@name_space4.route('/actor_movies/<actor_movie_id>')
class ActorMovieRelationClass2(Resource):
    @jwt_required
    def get(self, actor_movie_id):
        actor_movie = ActorMovieRelationsModel.query.get_or_404(actor_movie_id)
        response = {
            "id": actor_movie.id,
            "actor_id": actor_movie.actor_id,
            "movie_id": actor_movie.movie_id,
            "actor": {"actor_name": actor_movie.actor.name, "actor_age": actor_movie.actor.age},
            "movie": {"movie_name": actor_movie.movie.name, "movie_year": actor_movie.movie.year}
        }
        return {"message": "success", "actor_movie": response}

    @jwt_required
    @name_space4.expect(actor_movie_model)
    def put(self, actor_movie_id):
        actor_movie = ActorMovieRelationsModel.query.get_or_404(actor_movie_id)
        data = request.get_json()
        actor_movie.actor_id = data['actor_id']
        actor_movie.movie_id = data['movie_id']

        db.session.add(actor_movie)
        db.session.commit()

        return {"message": f"actor_movie {actor_movie.name} successfully updated"}

    @jwt_required
    def delete(self, actor_movie_id):
        actor_movie = ActorMovieRelationsModel.query.get_or_404(actor_movie_id)
        db.session.delete(actor_movie)
        db.session.commit()

        return {"message": f"ActorMovieRelation {actor_movie.name} successfully deleted."}
