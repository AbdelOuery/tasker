from flask import Blueprint, request, jsonify
from db import db

tasks = Blueprint('tasks', __name__)

url = '/api/task'


@tasks.route(url + '/<int:user_id>', methods=['GET'])
def get_user_tasks(user_id):
    user = {}
    user_tasks = []
    user = db.users.find_one({'_id': user_id})
    user_tasks = user.get('tasks', [])
    return jsonify({'user_tasks': user_tasks}), 200


@tasks.route(url + '/add', methods=['POST'])
def add_user_task():
    request_body = request.get_json()
    user_id = request_body.get('user_id', None)
    task = request_body.get('task', None)
    # Add the task
    db.users.update_one(
        {'_id': user_id},
        {'$push': {'tasks': task}})
    return jsonify({'msg': 'task added'}), 200


@tasks.route(url + '/update', methods=['POST'])
def update_user_task():
    request_body = request.get_json()
    user_id = request_body.get('user_id', None)
    task_label = request_body.get('task_label')
    task = request_body.get('task')
    # Update the task
    db.users.update_one({
        '_id': user_id,
        'tasks.label': task_label},
        {'$set': {'tasks.$': task}})
    return jsonify({'msg': 'task updated'}), 200


@tasks.route(url + '/delete', methods=['DELETE'])
def delete_user_task():
    request_body = request.get_json()
    user_id = request_body.get('user_id', None)
    task_label = request_body.get('task_label')
    # Delete the task
    db.users.update_one({
        '_id': user_id},
        {'$pull': {'tasks': {'label': task_label}}})
    return jsonify({'msg': 'task deleted'}), 200
