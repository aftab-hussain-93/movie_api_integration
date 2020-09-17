import os

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY','secret key')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = r"sqlite:///movies.db"
	API_USERNAME = os.environ.get('API_USER')
	API_PWD = os.environ.get('API_PWD')
