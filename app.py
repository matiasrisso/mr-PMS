from environs import Env
from flask import Flask
from db.models import db
from db.seed import *
from routes import routes_blueprint

env = Env()
env.read_env()

app = Flask(__name__)
if env("ENV") == "dev":
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = env("SQLALCHEMY_DATABASE_URI")
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.app = app
db.init_app(app)

# Create the database tables.
db.reflect()
db.drop_all()
db.create_all()

app.register_blueprint(routes_blueprint)

if __name__ == '__main__':
    seed_all()
    app.run(host='0.0.0.0', port=8000)
