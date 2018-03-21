from flask import Blueprint
from pymongo import MongoClient

database = Blueprint('database', __name__)

client = MongoClient('localhost:27017')
db = client.tasker_db
