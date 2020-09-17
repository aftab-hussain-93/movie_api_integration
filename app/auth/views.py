import uuid
from flask import Blueprint, request, current_app
from app.models import Users, Collections, Movies
from werkzeug.security import check_password_hash

auth = Blueprint('auth',__name__)

@auth.route('/register', methods=['POST'])
def register():
	data = request.json
	try:
		username = data['username']
		password = data['password']
		user = Users.query.filter(Users.name == username).first()
		if user:
			if check_password_hash(user.password, password):
				return {"x-access-token" : user.generate_jwt_token()}, 200
			else:
				raise AttributeError("Incorrect password")
		else:
			current_app.logger.info(f"Creating new user {username}...")
			access_token = Users.add_user(username=username, password=password)

	except (KeyError,TypeError) as e:
		return {"error" : f"Invalid input data. {e}. Please provide username and password"}
	except AttributeError as e:
		return {"error":"Invalid Login {}".format(e)}
	else:
		return {"x-access-token" : access_token}, 201

@auth.route('/request-count')
def request_count():
	return {
		"requests" : current_app.wsgi_app.get_count()
	}, 200

@auth.route('/request-count/reset')
def request_count_reset():
	current_app.wsgi_app.reset_count()
	return {
		"message" : "request count reset successfully"
	}, 200