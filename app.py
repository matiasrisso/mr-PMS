from environs import Env
from flask import Flask
from db.models import db
from db.seed import *
from routes import routes_blueprint
from flask_cors import CORS


# Swagger config
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'


# Load pre defined environment variables
env = Env()
env.read_env()

# Flask sqlalchemy configurations
app = Flask(__name__, instance_relative_config=True)
CORS(app)
if env("ENV") == "dev":
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = env("SQLALCHEMY_LOCAL_DATABASE_URI")
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = env("SQLALCHEMY_REMOTE_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.app = app
db.init_app(app)

# Create the database tables and delete previous data
db.reflect()
db.drop_all()
db.create_all()
# Add initial data to the tables
seed_all()

# Connect routes to app
app.register_blueprint(routes_blueprint)

if env("ENV") == "dev":
    from flask_swagger_ui import get_swaggerui_blueprint
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Best-PMS-ever"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    # Run the app
    app.run(host='0.0.0.0', port=8000)
