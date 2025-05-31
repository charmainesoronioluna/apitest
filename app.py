from flask import Flask, request, jsonify, render_template
from uuid import uuid4

app = Flask(__name__)
users = {}

@app.route('/')
def index():
    return render_template("/apitest/apitestui.html")

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values()))

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    user_id = str(uuid4())
    users[user_id] = {"id": user_id, "name": data['name'], "email": data['email']}
    return jsonify(users[user_id]), 201

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    if user_id in users:
        users[user_id].update(data)
        return jsonify(users[user_id])
    return jsonify({"error": "User not found"}), 404

@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        deleted = users.pop(user_id)
        return jsonify(deleted)
    return jsonify({"error": "User not found"}), 404
