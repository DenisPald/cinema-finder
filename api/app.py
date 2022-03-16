import dotenv
import flask

from data import db_session
from data._all_models import User, WatchListItem

config = dotenv.dotenv_values('.env')

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = config['SECRET_KEY']


@app.route('/')
def index():
    session = db_session.create_session()
    watch_lists = session.query(WatchListItem).all()
    return flask.jsonify({
        "watch_items": [
            item.to_dict(only=("id", "imdb_id", "user_id", "user.id"))
            for item in watch_lists
        ]
    })


def main():
    db_session.global_init(config['DB_USER'], config['DB_PASSWORD'],
                           config['DB_HOST'], config['DB_PORT'],
                           config['DB_FILE_NAME'])
    app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
