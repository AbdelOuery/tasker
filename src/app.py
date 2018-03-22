from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from db import database
from resources.users import users
from resources.tasks import tasks

app = Flask(__name__)

# Allow Cross-Origin-Resource-Sharing
CORS(app)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'My-Ultra-Super-Secret-String'
jwt = JWTManager(app)

# Register flask blueprints
app.register_blueprint(database)
app.register_blueprint(users)
app.register_blueprint(tasks)

if __name__ == '__main__':
    app.run()
