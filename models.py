class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.movies = []

class Movie:
    def __init__(self, movie_id, name, director, year, rating):
        self.movie_id = movie_id
        self.name = name
        self.director = director
        self.year = year
        self.rating = rating