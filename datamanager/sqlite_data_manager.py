from flask_sqlalchemy import SQLAlchemy
from datamanager.data_manager_interface import DataManagerInterface
from models import User


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app):
        self.db = SQLAlchemy(app)
        self.db.create_all()

    def get_all_users(self):
        return User.query.all()

    def get_user_movies(self, user_id):
        user = User.query.get(user_id)
        if user:
            return user.movies
        return []

    def add_user(self, user):
        self.db.session.add(user)
        self.db.session.commit()

    def add_movie(self, user_id, movie):
        user = User.query.get(user_id)
        if user:
            user.movies.append(movie)
            self.db.session.commit()
        else:
            raise ValueError("User not found")

    def update_movie(self, user_id, movie_id, updated_movie):
        user = User.query.get(user_id)
        if user:
            movie = next((m for m in user.movies if m.movie_id == movie_id), None)
            if movie:
                movie.name = updated_movie.name
                movie.director = updated_movie.director
                movie.year = updated_movie.year
                movie.rating = updated_movie.rating
                self.db.session.commit()
            else:
                raise ValueError("Movie not found")
        else:
            raise ValueError("User not found")

    def delete_movie(self, user_id, movie_id):
        user = User.query.get(user_id)
        if user:
            movie = next((m for m in user.movies if m.movie_id == movie_id), None)
            if movie:
                user.movies.remove(movie)
                self.db.session.commit()
            else:
                raise ValueError("Movie not found")
        else:
            raise ValueError("User not found")