import requests
from requests.models import PreparedRequest
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, current_app, request, url_for

movie = Blueprint('movie',__name__)

@movie.route('/movies')
def all_movies():
	page = request.args.get('page')
	user = current_app.config['API_USERNAME']
	pwd = current_app.config['API_PWD']
	if page:
		payload = {'page': page}
		res = requests.get('https://demo.credy.in/api/v1/maya/movies/', params=payload,  auth=(user, pwd), timeout=5)
	else:
		res = requests.get('https://demo.credy.in/api/v1/maya/movies/', auth=(user, pwd))
	try:
		res.raise_for_status()
		data = res.json()
		next_page_num =  data.get('next')
		next_page = url_for('movie.all_movies', _external=True) + '?page=' + next_page_num.split('=')[1] if next_page_num else None
		previous_page_num =  data.get('previous')
		prev_page = url_for('movie.all_movies', _external=True) + '?page=' + previous_page_num.split('=')[1] if previous_page_num else None
		
		result = {
		"count": data['count'],
		"next" : next_page,
		"previous" : prev_page,
		"data" : data['results']
		}
	except Exception as e:
		return {'error':f'Could not fetch the data {e}'}
	else:
		return result


#  url = 'http://example.com/search/'
# >>> params = {'lang':'en','tag':'python'}
# >>> req = PreparedRequest()
# >>> req.prepare_url(url, params)
# >>> print(req.url)

