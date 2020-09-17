import requests
from requests.models import PreparedRequest
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, current_app, request, url_for
from app.general_utils import token_required

movie = Blueprint('movie',__name__)

@movie.route('/movies')
@token_required
def all_movies(current_user):
	"""
	Provides the paginated list of all the movies. Use query string with param - "page" = <num> to get the next 
	paginated list.
	"""
	page = request.args.get('page')
	user = current_app.config['API_USERNAME']
	pwd = current_app.config['API_PWD']
	payload = {'page': page} if page else None

	# Initilization flag data_found = False
	
	data_found = False

	# Number of retries for response from the API
	request_count = 4
	for req in range(request_count):
		current_app.logger.info(f"Attempt number {req}  to access Movie API")
		res = requests.get('https://demo.credy.in/api/v1/maya/movies/', params=payload,  auth=(user, pwd), timeout=3)
		if res.status_code == 200:
			# Break out of loop if success Response received
			# Set data_found flag = True
			data_found = True
			break

	# Getting API data
	data = res.json()

	# Check data_found flag and verify if there are any errors in the response
	if data_found and not data.get('error'):		
		next_page_num =  data.get('next')

		# Creating pagination URLs that map to the APIs paginated URLs
		next_page = url_for('movie.all_movies', _external=True) + '?page=' + next_page_num.split('=')[1] if next_page_num else None
		previous_page_num =  data.get('previous')
		prev_page = url_for('movie.all_movies', _external=True) + '?page=' + previous_page_num.split('=')[1] if previous_page_num else None
		
		result = {
		"count": data['count'],
		"next" : next_page,
		"previous" : prev_page,
		"data" : data['results']
		}
		return result, 200
	else:
		return {"error": "Could not fetch API data. Please try again in a while."}, 400


