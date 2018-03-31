from flask import Blueprint, request, jsonify
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from db import db

users = Blueprint('users', __name__)

url = '/api/user'


@users.route(url + '/all', methods=['GET'])
@jwt_required
def get_all_users():
    users = []
    for user in db.users.find().sort('_id', -1):
        users.append(user)
    return jsonify({'users': users}), 200


@users.route(url + '/<int:id>', methods=['GET'])
@jwt_required
def get_one_user(id):
    return jsonify(db.users.find_one({'_id': id})), 200


@users.route(url + '/add', methods=['POST'])
def add_user():
    user = request.get_json()
    user['password'] = sha256.hash(user['password'])
    db.users.insert(user)
    return jsonify({'msg': 'user added'}), 200


@users.route(url + '/update/<int:id>', methods=['PUT'])
@jwt_required
def update_user(id):
    db.users.find_one_and_replace({'_id': id}, request.get_json())
    return jsonify({'msg': 'user updated'}), 200


@users.route(url + '/delete/<int:id>', methods=['DELETE'])
@jwt_required
def delete_user(id):
    db.users.remove({'_id': id})
    return jsonify({'msg': 'user deleted'}), 200


@users.route(url + '/login', methods=['POST'])
def login():
    request_body = request.get_json()
    username = request_body.get('username')
    user = db.users.find_one({'username': username})
    if user is not None:
        if sha256.verify(request_body.get('password'), user['password']):
            access_token = create_access_token(user)
            return jsonify({'Authorization': access_token}), 200
    return jsonify({'msg': 'bad credentials'}), 401


@users.route(url + '/current', methods=['GET'])
@jwt_required
def get_current_user():
    user = dict(get_jwt_identity())
    del user['password']
    return jsonify(user), 200
