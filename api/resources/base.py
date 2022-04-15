import flask
from data import db_session
from flask_restful import Resource, reqparse


class BaseResource(Resource):
    """Base class for single resource

    Change __init__ method with your values
    """

    def __init__(self):
        """Change this values:

        self.entity = SQLAlchemy model class
        self.columns_to_response = set(Columns to response on get request)
        self.put_parser_args = set(Args for put request)
        """
        self.entity = None
        self.columns_to_response = set()
        self.put_parser_args = set()

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

    def put(self, id):
        session = db_session.create_session()

        parser = reqparse.RequestParser()

        for i in self.put_parser_args:
            parser.add_argument(i)

        try:
            args = parser.parse_args()
        except Exception as e:
            return flask.jsonify({"error": f"incomplete data: {e}"})

        try:
            item = session.query(self.entity).get(id)
        except Exception as e:
            return flask.jsonify({"error": f"db error: {e}"})

        try:
            for arg in args.items():
                setattr(item, arg[0], arg[1])
            session.commit()
        except Exception as e:
            return flask.jsonify({"error": e})

        return flask.jsonify({"error": ""})


class BaseListResource(Resource):
    """Base class for list of resource

    Change __init__ method with your values
    """

    def __init__(self):
        """Change this values:

        self.entity = SQLAlchemy model class
        self.columns_to_response = set(Columns to response on get request)
        self.post_parser_args = set(Args for post request)
        """
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
            return flask.jsonify({"error": str(e)})

    def post(self):
        session = db_session.create_session()
        parser = reqparse.RequestParser()

        for i in self.post_parser_args:
            parser.add_argument(i)

        try:
            args = parser.parse_args()
            # TODO delete this PLS
            # args['telegram_id'] = int(args['telegram_id'])
            print("\n\n\n\n", args)
        except Exception as e:
            return flask.jsonify({"error": f"incomplete data: {e}"})

        try:
            item = self.entity(**args)
        except Exception as e:
            return flask.jsonify({"error": str(e)})

        try:
            session.add(item)
            session.commit()
        except Exception as e:
            return flask.jsonify({"error": f"some db error: {e}"})

        return flask.jsonify({"id": item.id})
