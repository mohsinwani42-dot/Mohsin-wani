from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)
DATA_FILE = 'submissions.json'

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

    entry = {
        'name': name,
        'email': email,
        'message': message,
        'submitted_at': datetime.utcnow().isoformat() + 'Z'
    }

    submissions = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                submissions = json.load(f)
        except (json.JSONDecodeError, IOError):
            submissions = []

    submissions.append(entry)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(submissions, f, indent=2)

    return jsonify({'message': 'Message received. Thank you!'})

@app.route('/submissions')
def submissions_page():
    return send_from_directory('.', 'submissions.html')

@app.route('/submissions-data')
def submissions_data():
    submissions = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                submissions = json.load(f)
        except (json.JSONDecodeError, IOError):
            submissions = []
    return jsonify(submissions)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
