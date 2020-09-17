from flask import Blueprint, current_app, request
from app.models import Users, Collections, Movies
from app import db

coll = Blueprint('coll',__name__)

@coll.route('/collection', methods=['GET', 'POST'])
def collection():
	current_user = Users.query.first()

	if request.method == 'POST':
		data = request.json
		try:
			title = data['title']
			description = data['description']
			movies = data['movies']
			if Collections.query.filter(Collections.title == title, Collections.user == current_user).count() > 0:
				raise ValueError("You have another collection with the same title")
			current_app.logger.info(f"Creating new collection {title}...")
			new_collection = Collections.create_collection(title=title, description=description, user_id=current_user.id)
		except (KeyError, TypeError) as e:
			return {"error": f"Missing input data {e}. Please enter title, description and list of movies"}, 400
		except ValueError as e:
			return {"error" : f"Invalid input. {e}"}, 400	

		# Adding all the new movies to the collection - movie association table
		for movie in movies:
			new_collection.add_new_movies(movie)			
		return {"collection_uuid": new_collection.uuid}, 201
	
	elif request.method == 'GET':
		user_collections =  Collections.query.filter(Collections.user == current_user).all()
		collections_info = []
		genre_list = []
		for coll in user_collections:
			collections_info.append({
				"title":coll.title, 
				"uuid":coll.uuid, 
				"description":coll.description
				})
			# Getting a list of all the genres in all the movies across each collection
			genre_list.extend(coll.get_movies_genres())

		# Getting the favorite genres by calculating the genres with the highest frequncy
		# Sorting them and retrieving the first three values
		fav_genres = sorted(genre_list, key=lambda x:genre_list.count(x), reverse=True)
		seen = set()
		fav_genres = [genre for genre in fav_genres if not (genre in seen or seen.add(genre))][:3]

		return {
		"is_success": True,
		"favourite_genres" : fav_genres,
		"data": {
		"collections": collections_info
		}
		}, 200

@coll.route('/collection/<uuid>', methods=['GET','PUT','DELETE'])
def single_collection(uuid):
	current_user = Users.query.first()
	collection = Collections.query.filter(Collections.uuid == uuid, Collections.user == current_user).first()
	if not collection:
		return {
				"is_success": False,
				"error" : "Invalid collection UUID"
				}, 404

	if request.method == 'PUT':
		try:
			data = request.json
			desc = data.get('description')
			title = data.get('title')
			movies = data.get('movies')
			if not desc and not title and not movies:
				raise ValueError("Please enter atleast one of the following - movies list, title or description.")			
			if title:
				if Collections.query.filter(Collections.title == title, Collections.user == current_user).count() > 0:
					raise ValueError("You have another collection with the same title. Cannot update title.")
				else:
					collection.title = title
		except AttributeError as e:
			return {"error" : f"No JSON data provided"}, 400
		except ValueError as e:
			return {"error" : f"Invalid input. {e}"}, 400
		else:
			if desc:
				collection.description = desc
			if movies:
				for movie in movies:
					collection.add_new_movies(movie)
			db.session.commit()
			return {"message" : "Collection successfully updated."}, 201

	elif request.method == 'GET':
		return {
			"is_success": True,
			"title": collection.title,
			"description": collection.description,
			"movies": [{
				"title":movie.title, 
				"description":movie.description,
				"genres":[genre.name for genre in movie.genres],
				"uuid": movie.uuid} for movie in collection.movies]
		}, 200


	elif request.method == 'DELETE':
		collection.collection_movies = []
		db.session.delete(collection)
		db.session.commit()
		return {
		"message" : "Collection deleted successfully"
		}, 200