from flask import Flask, render_template, request, redirect, url_for
from datamanager.sqlite_data_manager import SQLiteDataManager
from models import User, Movie

app = Flask(__name__)
data_manager = SQLiteDataManager(app, 'moviwebapp.db')  # Pass the app instance and the database path

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def hello_world():
    return "Welcome to MovieWeb App!"

@app.route('/users')
def list_users():
    try:
        users = data_manager.get_all_users()
    except Exception as e:
        app.logger.error(f"Error fetching users: {e}")
        return render_template('error.html', message="Error fetching users"), 500
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>')
def user_movies(user_id):
    try:
        user = data_manager.get_user(user_id)
        movies = data_manager.get_user_movies(user_id)
    except Exception as e:
        app.logger.error(f"Error fetching user or movies: {e}")
        return render_template('error.html', message="Error fetching user or movies"), 500
    return render_template('user_movies.html', user=user, movies=movies)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        new_user = User(user_id=None, name=name)
        try:
            data_manager.add_user(new_user)
        except Exception as e:
            app.logger.error(f"Error adding user: {e}")
            return render_template('error.html', message="Error adding user"), 500
        return redirect(url_for('list_users'))
    return render_template('add_user.html')

@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        name = request.form['name']
        director = request.form['director']
        year = request.form['year']
        rating = request.form['rating']
        new_movie = Movie(movie_id=None, name=name, director=director, year=year, rating=rating)
        try:
            data_manager.add_movie(user_id, new_movie)
        except Exception as e:
            app.logger.error(f"Error adding movie: {e}")
            return render_template('error.html', message="Error adding movie"), 500
        return redirect(url_for('user_movies', user_id=user_id))
    return render_template('add_movie.html', user_id=user_id)

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    if request.method == 'POST':
        name = request.form['name']
        director = request.form['director']
        year = request.form['year']
        rating = request.form['rating']
        updated_movie = Movie(movie_id=movie_id, name=name, director=director, year=year, rating=rating)
        try:
            data_manager.update_movie(user_id, movie_id, updated_movie)
        except Exception as e:
            app.logger.error(f"Error updating movie: {e}")
            return render_template('error.html', message="Error updating movie"), 500
        return redirect(url_for('user_movies', user_id=user_id))
    try:
        movie = data_manager.get_movie(user_id, movie_id)
    except Exception as e:
        app.logger.error(f"Error fetching movie: {e}")
        return render_template('error.html', message="Error fetching movie"), 500
    return render_template('update_movie.html', user_id=user_id, movie=movie)

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    try:
        data_manager.delete_movie(user_id, movie_id)
    except Exception as e:
        app.logger.error(f"Error deleting movie: {e}")
        return render_template('error.html', message="Error deleting movie"), 500
    return redirect(url_for('user_movies', user_id=user_id))

if __name__ == '__main__':
    app.run()