"""Application routes."""
from datetime import datetime as dt
from flask import request
from .. import api, name_space3
from flask_restx import Resource, fields
from ..models.movies import db, MoviesModel
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

movie_model = api.model('MovieModel', {
    'name': fields.String(readOnly=True, description='The name of the Movie'),
    'year': fields.Integer(required=True, description='The year of the Movie')
})

parser = api.parser()
parser.add_argument('Authorization', location='headers')


@name_space3.route('/movies')
@name_space3.expect(parser)
class MovieClass(Resource):
    @name_space3.expect(movie_model)
    # @name_space3.doc(security=[{'oauth2': ['read', 'write']}])
    @jwt_required
    def post(self):
        """Create Movie Object"""
        if request.is_json:
            data = request.get_json()
            print('Authorization', request.headers.get('Authorization'))
            new_movie = MoviesModel(name=api.payload['name'], year=api.payload['year'])

            db.session.add(new_movie)
            db.session.commit()

            return {"message": f"Movie {new_movie.name} has been created successfully."}, 201
        else:
            return {"error": "The request payload is not in JSON format"}

    @jwt_required
    def get(self):
        """Get Movie Object"""
        the_header = request.headers.get('Authorization')
        print('Authorization', the_header)
        current_user = get_jwt_identity()
        print(current_user)
        movies = MoviesModel.query.all()

        # filter example:
        # movies = MoviesModel.query.filter(MoviesModel.model == 'r343f')

        results = [
            {
                "id": movie.id,
                "name": movie.name,
                "year": movie.year,
            } for movie in movies]

        return {"count": len(results), "movies": results, "message": "success"}


@name_space3.route('/movies/<movie_id>')
class MovieClass2(Resource):
    @jwt_required
    def get(self, movie_id):
        movie = MoviesModel.query.get_or_404(movie_id)
        response = {
            "name": movie.name,
            "year": movie.year
        }
        return {"message": "success", "movie": response}

    @jwt_required
    @name_space3.expect(movie_model)
    def put(self, movie_id):
        movie = MoviesModel.query.get_or_404(movie_id)
        data = request.get_json()
        movie.name = data['name']
        movie.year = data['year']

        db.session.add(movie)
        db.session.commit()

        return {"message": f"movie {movie.name} successfully updated"}

    @jwt_required
    def delete(self, movie_id):
        movie = MoviesModel.query.get_or_404(movie_id)
        db.session.delete(movie)
        db.session.commit()

        return {"message": f"Movie {movie.name} successfully deleted."}
