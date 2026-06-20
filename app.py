from flask import Flask, request, jsonify, send_from_directory, g
from flask_cors import CORS
from datetime import datetime
import os
import sqlite3

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)
DATABASE_FILE = 'submissions.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_FILE)
        db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.execute(
        '''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            submitted_at TEXT NOT NULL
        )
        '''
    )
    db.commit()


@app.teardown_appcontext
def close_db(error=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'message': 'Invalid JSON payload.'}), 400

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()

    if not name or not email or not message:
        return jsonify({'message': 'All fields are required.'}), 400

    submitted_at = datetime.utcnow().isoformat() + 'Z'
    db = get_db()
    db.execute(
        'INSERT INTO submissions (name, email, message, submitted_at) VALUES (?, ?, ?, ?)',
        (name, email, message, submitted_at),
    )
    db.commit()

    return jsonify({'message': 'Message received. Thank you!'})


@app.route('/submissions')
def submissions_page():
    return send_from_directory('.', 'submissions.html')


@app.route('/submissions-data')
def submissions_data():
    db = get_db()
    cursor = db.execute(
        'SELECT name, email, message, submitted_at FROM submissions ORDER BY id DESC'
    )
    rows = cursor.fetchall()
    submissions = [dict(row) for row in rows]
    return jsonify(submissions)


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True, port=5000)
