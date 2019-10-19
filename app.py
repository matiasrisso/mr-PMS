from environs import Env
from flask import Flask
from db.models import db
from db.seed import *
from routes import routes_blueprint

# Load pre defined enviroment variables
env = Env()
env.read_env()

# Flask sqlalchemy configurations
app = Flask(__name__, instance_relative_config=True)
if env("ENV") == "dev":
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = env("SQLALCHEMY_DATABASE_URI")
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.app = app
db.init_app(app)

# Create the database tables and delete previous data
db.reflect()
db.drop_all()
db.create_all()

# Connect routes to app
app.register_blueprint(routes_blueprint)

if __name__ == '__main__':
    # Add initial data to the tables
    seed_all()

    # Run the app
    app.run(host='0.0.0.0', port=8000)
