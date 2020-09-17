from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from app.config import Config

db  = SQLAlchemy()

def create_app(config=Config):
	app = Flask(__name__)
	app.config.from_object(config)
	db.init_app(app)
	from app.auth.views import auth
	from app.collections.views import coll
	from app.movies.views import movie
	app.register_blueprint(auth)
	app.register_blueprint(coll)
	app.register_blueprint(movie)
	with app.app_context():
		db.create_all()
	return app
