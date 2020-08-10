"""Application routes."""
from datetime import datetime as dt
from flask import request
from .. import api, name_space2
from flask_restx import Resource, fields
from ..models.actors import db, ActorsModel
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

actor_model = api.model('ActorModel', {
    'name': fields.String(readOnly=True, description='The name of the Actor'),
    'age': fields.Integer(required=True, description='The age of the Actor')
})

parser = api.parser()
parser.add_argument('Authorization', location='headers')


@name_space2.route('/actors')
@name_space2.expect(parser)
class ActorClass(Resource):
    @name_space2.expect(actor_model)
    # @name_space2.doc(security=[{'oauth2': ['read', 'write']}])
    @jwt_required
    def post(self):
        """Create Actor Object"""
        if request.is_json:
            data = request.get_json()
            print('Authorization', request.headers.get('Authorization'))
            new_actor = ActorsModel(name=api.payload['name'], age=api.payload['age'])

            db.session.add(new_actor)
            db.session.commit()

            return {"message": f"Actor {new_actor.name} has been created successfully."}, 201
        else:
            return {"error": "The request payload is not in JSON format"}

    @jwt_required
    def get(self):
        """Get Actor Object"""
        the_header = request.headers.get('Authorization')
        print('Authorization', the_header)
        current_user = get_jwt_identity()
        print(current_user)
        actors = ActorsModel.query.all()

        # filter example:
        # actors = ActorsModel.query.filter(ActorsModel.model == 'r343f')

        results = [
            {
                "id": actor.id,
                "name": actor.name,
                "age": actor.age,
            } for actor in actors]

        return {"count": len(results), "actors": results, "message": "success"}


@name_space2.route('/actors/<actor_id>')
class ActorClass2(Resource):
    @jwt_required
    def get(self, actor_id):
        actor = ActorsModel.query.get_or_404(actor_id)
        response = {
            "name": actor.name,
            "age": actor.age
        }
        return {"message": "success", "actor": response}

    @jwt_required
    @name_space2.expect(actor_model)
    def put(self, actor_id):
        actor = ActorsModel.query.get_or_404(actor_id)
        data = request.get_json()
        actor.name = data['name']
        actor.age = data['age']

        db.session.add(actor)
        db.session.commit()

        return {"message": f"actor {actor.name} successfully updated"}

    @jwt_required
    def delete(self, actor_id):
        actor = ActorsModel.query.get_or_404(actor_id)
        db.session.delete(actor)
        db.session.commit()

        return {"message": f"Actor {actor.name} successfully deleted."}
