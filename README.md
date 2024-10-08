# Application Structure

## User Interface (UI)

### Flask
Handles routing and rendering HTML templates.

### HTML
`index.html` and other templates provide the necessary forms and links for user interactions.

## Data Management

### Python Class
`SQLiteDataManager` class in `sqlite_data_manager.py` handles operations related to the data source, such as getting users and their movies, adding, updating, and deleting movies.

### Database File

#### SQLite
Using an SQLite database (`moviwebapp.db`) to store user and movie data.

# Core Functionalities

## User Selection

### Route
`/users` route lists all users, allowing for user selection.

## Movie Management

### Add a Movie
`/users/<int:user_id>/add_movie` 

### Delete a Movie
`/users/<int:user_id>/delete_movie/<int:movie_id>`


### Update a Movie
`/users/<int:user_id>/update_movie/<int:movie_id>`


### List All Movies
`/users/<int:user_id>` 

## Data Source Management

### SQLiteDataManager
This class manages interactions with the SQLite database, including CRUD operations for users and movies.