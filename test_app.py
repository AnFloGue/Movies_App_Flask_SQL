# test_app.py
import unittest
from app import app

class RouteTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Home Page', response.data)

    def test_add_user_route(self):
        response = self.app.get('/add_user')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add User', response.data)

    def test_add_movie_route(self):
        response = self.app.get('/users/1/add_movie')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add Movie', response.data)

class EdgeCaseTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_non_existent_user_movies(self):
        response = self.app.get('/users/999')
        self.assertEqual(response.status_code, 404)

    def test_update_non_existent_movie(self):
        response = self.app.post('/users/1/update_movie/999', data=dict(name='New Title'))
        self.assertEqual(response.status_code, 404)

class FormValidationTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_empty_form_submission(self):
        response = self.app.post('/add_user', data=dict(name=''))
        self.assertIn(b'This field is required.', response.data)

    def test_invalid_data_submission(self):
        response = self.app.post('/users/1/add_movie', data=dict(name='A'*101, director='Director', year='2023', rating='5'))
        self.assertIn(b'Field cannot be longer than 100 characters.', response.data)

if __name__ == '__main__':
    unittest.main()