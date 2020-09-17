import os

class Config:
	SECRET_KEY = 'secret key'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = r"sqlite:///movies.db"
	API_USERNAME = os.environ.get('API_USER','iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0')
	API_PWD = os.environ.get('API_PWD','Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1')