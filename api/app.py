import dotenv
import flask

from data import db_session

config = dotenv.dotenv_values("../.env")

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = config['SECRET_KEY']


@app.route('/')
def index():
    return flask.jsonify(config)


def main():
    db_session.global_init(config['DB_USER'], config['DB_PASSWORD'],
                           config['DB_HOST'], config['DB_PORT'],
                           config['DB_FILE_NAME'])
    app.run(debug=True)


if __name__ == "__main__":
    main()
