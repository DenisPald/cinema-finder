import dotenv
import flask
from data import db_session
from flask_restful import Api
from resources import users, watch_items

config = dotenv.dotenv_values('.env')

app = flask.Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = config['SECRET_KEY']
api.add_resource(watch_items.WatchListItemResource, "/watch_items/<int:id>/")
api.add_resource(watch_items.WatchListResource, "/watch_items/")
api.add_resource(users.UserResource, "/users/<int:id>/")
api.add_resource(users.UserListResource, "/users/")


def main():
    db_session.global_init(config['DB_USER'], config['DB_PASSWORD'],
                           config['DB_HOST'], config['DB_PORT'],
                           config['DB_FILE_NAME'])
    app.run(debug=False, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
