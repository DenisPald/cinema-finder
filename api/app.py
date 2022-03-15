import dotenv
import flask
from data import db_session
from data import _all_models

config = dotenv.dotenv_values('.env')

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = config['SECRET_KEY']


@app.route('/')
def index():
    session = db_session.create_session()
    users = session.query(_all_models.User).all()
    users_id = []
    for user in users:
        users_id.append(user.id)
    return flask.jsonify({"users": users_id})


def main():
    db_session.global_init(config['DB_USER'], config['DB_PASSWORD'],
                           config['DB_HOST'], config['DB_PORT'],
                           config['DB_FILE_NAME'])
    app.run(debug=True, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
