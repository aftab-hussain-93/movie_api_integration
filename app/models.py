import uuid, jwt, datetime
from app import db
from werkzeug.security import generate_password_hash
from flask import current_app as app

class Base(db.Model):
	__abstract__ = True

	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Users(Base):
	name = db.Column(db.String, unique=True, nullable=False)
	password = db.Column(db.String, nullable=False)
	public_id = db.Column(db.String, nullable=False, unique=True)

	collections = db.relationship('Collections', backref='user', lazy=True)

	@classmethod
	def add_user(cls, username, password):
		hashed_password = generate_password_hash(password, method='sha256')
		user = cls(name = username, password = hashed_password, public_id = uuid.uuid4().hex)
		db.session.add(user)
		db.session.commit()
		return user.generate_jwt_token()

	def generate_jwt_token(self):
		token = jwt.encode({'public_id' : self.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY']).decode('UTF-8')
		return token

	def __str__(self):
		return f"User - {self.username}"

	def __repr__(self):
		return f"<{self.id}> - <{self.username}>"

collection_movies = db.Table('collection_movies',
    db.Column('coll_id', db.Integer, db.ForeignKey('collections.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True)
)

class Collections(Base):
	title = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)
	uuid = db.Column(db.String, unique=True, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	
	movies = db.relationship('Movies', 
		secondary=collection_movies, 
		lazy='subquery', 
		backref= db.backref('collections', lazy=True))

	@classmethod
	def create_collection(cls, title, description, user_id):
		new_coll = cls(title=title, description=description, uuid=uuid.uuid4().hex, user_id=user_id)
		db.session.add(new_coll)
		db.session.commit()
		return new_coll

	def add_new_movies(self, movie_dict):
		"""
		Function to add new movies into this particular collection.
		input - 
		movie_dict - movie dictionary containing all the details
		"""
		try:
			movie_uuid = movie_dict['uuid']
			movie_title = movie_dict['title']
			movie_description = movie_dict["description"]
			movie_genre_list = movie_dict['genres']
		except (KeyError, TypeError) as e:
			return {"error": f"Missing movie input data {e}. Please enter title, description, uuid and genre list of the movie."}, 400
		else:
			mov = Movies.query.filter(Movies.uuid == movie_uuid).first()
			if mov:
				if mov in self.movies:
					app.logger.info(f"Movie {movie_title} already exists in collection. Returning...")
					return True
				else:
					self.movies.append(mov)
					app.logger.info(f"Movie {movie_title} added to collection..")
			else:
				app.logger.info(f"Inserting a new movie {movie_title} into database...")
				mov = Movies.add_movie(title=movie_title , description=movie_description, uuid= movie_uuid, genre_list=movie_genre_list)
				self.movies.append(mov)
				app.logger.info(f"Movie {movie_title} added to collection..")
		db.session.commit()
		return True

	def get_movies_genres(self):
		"""
		Function to get a list of genres of the movies in this collection.
		"""
		result = []
		for movie in self.movies:
			mr = [genre.name for genre in movie.genres]
			result.extend(mr)
		return result

	def __str__(self):
		return f"Collection name {self.title}"

	def __repr__(self):
		return f"<{self.uuid}> - <{self.title}>"

movies_genre = db.Table('movies_genre',
	db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
	db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True))

class Movies(Base):
	title = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)
	uuid = db.Column(db.String, unique=True, nullable=False)

	genres = db.relationship('Genres', 
		secondary=movies_genre,
		lazy='subquery',
		backref=(db.backref('movies', lazy=True)))

	@classmethod
	def add_movie(cls, title, description, uuid, genre_list):
		movie = cls(title=title, description=description, uuid=uuid)
		db.session.add(movie)
		db.session.commit()
		for genre in genre_list.split(','):
			g = Genres.query.filter_by(name=genre.lower()).first()
			if g:
				movie.genres.append(g)
			else:
				g = Genres(name=genre.lower())
				db.session.add(g)
				db.session.commit()
				movie.genres.append(g)
		db.session.commit()
		return movie

	def __str__(self):
		return f"Movie name {self.title}"

	def __repr__(self):
		return f"<{self.uuid}> - <{self.title}>"

class Genres(Base):
	name = db.Column(db.String, unique=True, nullable = False)

	def __repr__(self):
		return f"Genre name {self.name}"
