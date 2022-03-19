import flask
from data import db_session
from data._all_models import *
from flask_restful import Resource, reqparse


class WatchListItemResource(Resource):

    def get(self, id):
        try:
            session = db_session.create_session()
            watch_list_item = session.query(WatchListItem).get(id)
        except:
            return flask.jsonify(
                {"error": "cant create session most likely the db has fallen"})

        if watch_list_item is None:
            return flask.jsonify({"error": "wrong item id"})

        return flask.jsonify({
            "info":
            watch_list_item.to_dict(only=('id', 'user_id', 'imdb_id')),
            "error":
            ""
        })

    def delete(self, id):
        try:
            session = db_session.create_session()
            item = session.query(WatchListItem).get(id)
        except:
            return flask.jsonify(
                {"error": "cant create session most likely the db has fallen"})

        if item is None:
            return flask.jsonify({"error": "wrong item id"})

        try:
            session.delete(item)
            session.commit()
        except:
            return flask.jsonify({"error": "some db error"})

        return flask.jsonify({"error": ""})


class WatchListResource(Resource):

    def get(self):
        try:
            session = db_session.create_session()
            watch_list = session.query(WatchListItem).all()
        except:
            return flask.jsonify(
                {"error": "cant create session most likely the db has fallen"})

        return flask.jsonify({
            "items":
            [i.to_dict(only=('id', 'imdb_id', 'user_id')) for i in watch_list]
        })

    def post(self):
        session = db_session.create_session()
        parser = reqparse.RequestParser()
        parser.add_argument('imdb_id', required=True)
        parser.add_argument('user_id', required=True)

        try:
            args = parser.parse_args()
        except:
            return flask.jsonify({"error": "incomplete data"})

        watch_list_item = WatchListItem(imdb_id=args["imdb_id"],
                                        user_id=args["user_id"])
        try:
            session.add(watch_list_item)
            session.commit()
        except:
            return flask.jsonify({"error": "some db error"})

        return flask.jsonify({"id": watch_list_item.id})
