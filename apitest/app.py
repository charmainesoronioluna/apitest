from flask import Flask, request, jsonify, render_template

import uuid

app = Flask(__name__)

data = []

@app.route('/')
def home():
    return render_template('apitestui.html')

@app.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return jsonify(data)
    elif request.method == 'POST':
        new_user = request.json
        new_user['id'] = str(uuid.uuid4())  # generate unique id
        data.append(new_user)
        return jsonify({"message": "User added", "user": new_user}), 201

@app.route('/api/users/<user_id>', methods=['PUT', 'DELETE'])
def user_detail(user_id):
    global data
    user = next((u for u in data if u['id'] == user_id), None)
    if not user:
        return jsonify({"message": "User not found"}), 404

    if request.method == 'PUT':
        updated_data = request.json
        user.update(updated_data)
        return jsonify({"message": "User updated", "user": user})

    if request.method == 'DELETE':
        data = [u for u in data if u['id'] != user_id]
        return jsonify({"message": "User deleted"})

@app.route('/api/users/<user_id>', methods=['PATCH'])
def patch_user(user_id):
    user = next((u for u in data if u['id'] == user_id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    patch_data = request.get_json()
    if not patch_data:
        return jsonify({"error": "Invalid input"}), 400

    user.update(patch_data)
    return jsonify({"message": "User partially updated", "user": user}), 200