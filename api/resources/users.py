import flask
from data import db_session
from data._all_models import *
from flask_restful import Resource, reqparse


class UserResource(Resource):

    def get(self, id):
        session = db_session.create_session()

        try:
            user = session.query(User).get(id)
        except:
            return flask.jsonify({"error": "some db error"})

        if user is None:
            return flask.jsonify({"error": "wrong user id"})

        return flask.jsonify({
            "info": user.to_dict(only=("id", )),
            "watch_list": [item.to_dict(only=("id", "imdb_id")) for item in user.watch_item],
            "error": ""
        })

    def delete(self, id):
        session = db_session.create_session()

        try:
            user = session.query(User).get(id)
        except:
            return flask.jsonify({"error": "some db error"})

        if user is None:
            return flask.jsonify({"error": "wrong user id"})

        try:
            for watch_item in user.watch_item:
                session.delete(watch_item)
            session.delete(user)
            session.commit()
        except:
            return flask.jsonify({"error": "some db error"})

        return flask.jsonify({"error": ""})


class UserListResource(Resource):

    def get(self):
        try:
            session = db_session.create_session()
            watch_list = session.query(User).all()
        except:
            return flask.jsonify(
                {"error": "cant create session most likely the db has fallen"})

        return flask.jsonify(
            {"users": [i.to_dict(only=("id", )) for i in watch_list]})

    def post(self):
        session = db_session.create_session()
        # parser = reqparse.RequestParser()
        # parser.add_argument('imdb_id', required=True)
        # parser.add_argument('user_id', required=True)

        # try:
        #     args = parser.parse_args()
        # except:
        #     return flask.jsonify({"error": "incomplete data"})

        user = User()

        try:
            session.add(user)
            session.commit()
        except:
            return flask.jsonify({"error": "some db error"})

        return flask.jsonify({"id": user.id})
