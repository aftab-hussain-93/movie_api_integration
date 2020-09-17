# MOVIE_API_INTEGRATION

## DO THE FOLLOWING STEPS TO GET STARTED

```
pip install -r requirements.txt
```

```
python3 run.py
```


## API - ENDPOINTS  
  
  To access secured endpoints, you will need to provide an access token. The register route is the only unprotected route. It will register your user and provide your access token valid for the next 60 minutes.  
  Subsequently add the field "x-access-token" to your request headers to access these protected routes.
  
  ```
	http://127.0.0.1:5000/register  - POST

	Request Payload:
	{
	 “username”: <desired username>,
	 “password”: <desired password>
	}

	Response:
	{
	 “access_token”: <Access Token>
	}

  Get list of all the movies. Token required.

	http://127.0.0.1:5000/movies  - GET

	Response:
	{
	 “count”: <total number of movies>,
	 “next”: <link for next page, if present>,
	 “previous”: <link for previous page>,
	 “data”: [
	 {
	 “title”: <title of the movie>,
	 “description”: <a description of the movie>,
	 “genres”: <a comma separated list of genres, if
	present>,
	 “uuid”: <a unique uuid for the movie>
	 },
	 ...
	 ]
	}

	List of User's collection along with the favourite genres

	GET http://localhost:8000/collection/

	{
	 “is_success”: True,
	 “data”: {
	 “collections”: [
		 {
			 “title”: “<Title of my collection>”,
			 “uuid”: “<uuid of the collection name>”
			 “description”: “My description of the collection.”
		 },
		 ...
		 ],
	 “favourite_genres”: “<My top 3 favorite genres based on the
		movies I have added in my collections>.”
	 }
	}

	Add collection and movies

	POST http://localhost:8000/collection/
	Request payload:
	{
		 “title”: “<Title of the collection>”,
		 “description”: “<Description of the collection>”,
		 “movies”: [
			 {
			 “title”: <title of the movie>,
			 “description”: <description of the movie>,
			 “genres”: <generes>,
			 “uuid”: <uuid>
			 }, ...
		 ]
	}

	Response payload:
	{
	 “collection_uuid”: <uuid of the collection item>
	}

	Update the collection with uuid = <collection_uuid>

	PUT http://localhost:8000/collection/<collection_uuid>/

	Request:
	{
	 “title”: <Optional updated title>,
	 “description”: <Optional updated description>,
	 “movies”: <Optional movie list to be updated>,
	}

	Get all the details of the specified collection, including movies list
	
	GET http://localhost:8000/collection/<collection_uuid>/

	Response:
	{
	 “title”: <Title of the collection>,
	 “description”: <Description of the collection>,
	 “movies”: <Details of movies in my collection>
	}

	DELETE http://localhost:8000/collection/<collection_uuid>/

	{
	    "message": "Collection deleted successfully"
	}

	Impletementing the request counte
	GET http://localhost:8000/request-count/
	Response:
	{
	 “requests”: <number of requests served by this server till now>.
	}

	Implementing the request count reset
	POST http://localhost:8000/request-count/reset/
	Response:
	{
	 “message”: “request count reset successfully”
	}


  ``` 