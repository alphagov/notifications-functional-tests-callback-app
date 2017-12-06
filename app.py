import sqlite3
from flask import Flask, g, request, abort

app = Flask('notifications-functional-test-callback-app')
DATABASE = 'database.db'


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    db.commit()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def index():
    return 'Functional Test Callback App is running'


@app.route('/get-response/<notification_id>')
def get_response(notification_id):

    result = query_db(
        'select * from delivery_receipt_callbacks where id = ?',
        [notification_id],
        one=True
    )

    if not result:
        abort(404)

    return result['id']


@app.route('/create-response', methods=['POST'])
def create_response():
    response = request.get_json()
    response_id = response.get('id')

    query_db("INSERT INTO delivery_receipt_callbacks (id) VALUES (?)", [response_id])

    return 'The receipt for  notification {} has been received'.format(response_id)


init_db()
