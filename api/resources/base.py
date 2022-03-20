import flask
from data import db_session
from flask_restful import Resource, reqparse


class BaseResource(Resource):

    def __init__(self):
        self.entity = None
        self.columns_to_response = set()

    def get(self, id):
        session = db_session.create_session()

        try:
            item = session.query(self.entity).get(id)
        except Exception as e:
            return flask.jsonify({"error": f"db error: {e}"})

        if item is None:
            return flask.jsonify({"error": "wrong id"})

        try:
            return flask.jsonify({
                "info":
                item.to_dict(only=self.columns_to_response),
                "error":
                ""
            })
        except Exception as e:
            return flask.jsonify({"error": e})

    def delete(self, id):
        session = db_session.create_session()

        try:
            item = session.query(self.entity).get(id)
        except Exception as e:
            return flask.jsonify({"error": f"db error: {e}"})

        if item is None:
            return flask.jsonify({"error": "wrong id"})

        try:
            session.delete(item)
            session.commit()
        except Exception as e:
            return flask.jsonify({"error": f"db error: {e}"})

        return flask.jsonify({"error": ""})


class BaseListResource(Resource):

    def __init__(self):
        self.entity = None
        self.columns_to_response = set()
        self.post_parser_args = set()

    def get(self):
        try:
            session = db_session.create_session()
            entity_list = session.query(self.entity).all()
        except Exception as e:
            return flask.jsonify({"error": f"db error: {e}"})

        try:
            return flask.jsonify({
                "items": [
                    i.to_dict(only=self.columns_to_response)
                    for i in entity_list
                ],
                "error":
                ""
            })
        except Exception as e:
            return flask.jsonify({"error": e})

    def post(self):
        session = db_session.create_session()
        parser = reqparse.RequestParser()

        for i in self.post_parser_args:
            parser.add_argument(i)

        try:
            args = parser.parse_args()
        except Exception as e:
            return flask.jsonify({"error": f"incomplete data: {e}"})

        item = self.entity(**args)

        try:
            session.add(item)
            session.commit()
        except Exception as e:
            return flask.jsonify({"error": f"some db error: {e}"})

        return flask.jsonify({"id": item.id})
