from unittest import TestCase, main
from app import create_app
import json

app = create_app()

class FlaskTest(TestCase):

	# Checks the movie route
	def test_movie(self):
		tester = app.test_client(self)
		response = tester.get("/movies")
		status_code = response.status_code
		self.assertEqual(status_code, 200)
		self.assertEqual(response.content_type, "application/json")

	# Successful Login
	def test_valid_login(self):
		tester = app.test_client(self)
		res = tester.post('/register', json={"username":"aftab", "password":"hello"})
		self.assertEqual("x-access-token" in res.json, True)

	# Unsuccessful Login - Incorrect Password
	def test_invalid_login(self):
		tester = app.test_client(self)
		res = tester.post('/register', json={"username":"aftab", "password":"hello1"})
		self.assertEqual("error" in res.json, True)

if __name__ == '__main__':
	main()

