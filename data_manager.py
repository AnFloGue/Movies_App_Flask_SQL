import json
from datamanager.data_manager_interface import DataManagerInterface
from models import User, Movie

class DataManager(DataManagerInterface):
    def __init__(self, data_file):
        self.data_file = data_file
        self.users = self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                users = []
                for user_data in data:
                    user = User(user_data['id'], user_data['name'])
                    for movie_data in user_data['movies']:
                        movie = Movie(movie_data['id'], movie_data['name'], movie_data['director'], movie_data['year'], movie_data['rating'])
                        user.movies.append(movie)
                    users.append(user)
                return users
        except FileNotFoundError:
            return []

    def save_data(self):
        data = []
        for user in self.users:
            user_data = {
                'id': user.user_id,
                'name': user.name,
                'movies': [{'id': movie.movie_id, 'name': movie.name, 'director': movie.director, 'year': movie.year, 'rating': movie.rating} for movie in user.movies]
            }
            data.append(user_data)
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)

    def get_all_users(self):
        return self.users

    def get_user_movies(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user.movies
        return []

    def add_user(self, user):
        self.users.append(user)
        self.save_data()

    def add_movie(self, user_id, movie):
        for user in self.users:
            if user.user_id == user_id:
                user.movies.append(movie)
                self.save_data()
                return
        raise ValueError("User not found")

    def update_movie(self, user_id, movie_id, updated_movie):
        for user in self.users:
            if user.user_id == user_id:
                for i, movie in enumerate(user.movies):
                    if movie.movie_id == movie_id:
                        user.movies[i] = updated_movie
                        self.save_data()
                        return
        raise ValueError("Movie not found")

    def delete_movie(self, user_id, movie_id):
        for user in self.users:
            if user.user_id == user_id:
                user.movies = [movie for movie in user.movies if movie.movie_id != movie_id]
                self.save_data()
                return
        raise ValueError("Movie not found")