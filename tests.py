from unittest import TestCase, main
from app import create_app
import json

app = create_app()

class FlaskTest(TestCase):

	# Successful Login
	def test_valid_login(self):
		tester = app.test_client(self)
		res = tester.post('/register', json={"username":"aftab", "password":"hello"})
		self.assertEqual("x-access-token" in res.json, True)

	# Unsuccessful Login - Incorrect Password
	def test_invalid_login(self):
		tester = app.test_client(self)
		res = tester.post('/register', json={"username":"aftab", "password":"incorrect-password"})
		self.assertEqual("error" in res.json, True)

	# User has no collections 
	# Testing the collections end point
	def get_collections(self):
		tester = app.test_client(self)
		response = tester.get("/collection")
		status_code = response.status_code
		self.assertEqual(status_code, 204) # No content

	def create_collection(self):
		tester = app.test_client(self)
		response = tester.post("/collection", json={"title":"test-collection", "description":"collection-description", "movies" :[ {
		"description": "50 years after decriminalisation of homosexuality in the UK, director Daisy Asquith mines the jewels of the BFI archive to take us into the relationships, desires, fears and expressions of gay men and women in the 20th century.",
		"genres": "",
		"title": "Queerama",
		"uuid": "57baf4f4-c9ef-4197-9e4f-acf04eae5b4d"
		}]})
		status_code = response.status_code
		self.assertEqual(status_code, 201)

	# Checks the movie route
	def test_movie(self):
		tester = app.test_client(self)
		response = tester.get("/movies")
		status_code = response.status_code
		self.assertEqual(status_code, 200)
		self.assertEqual(response.content_type, "application/json")

if __name__ == '__main__':
	main()

