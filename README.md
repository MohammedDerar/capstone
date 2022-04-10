<Intro>
Full Stack Capstone Project

This  is a casting agency API allowing users to query the database for movies and actors.
Tere are three different user roles with different permissions for each.

- Casting assistant: Can view actors and movies.
- Casting director: Can view, add, modify, and delete actors; can view and modify movies.
- Casting producer: Can view, add, modify, and delete actors and movies.






<Running API>

Getting Started
- Base URL: API endpoints can be accessed via https://capstone-fsnd-varlese.herokuapp.com/.
Running localy:
- The API can be run locally on http://localhost:8080  
- Authentication: Auth0 information for endpoints that require authentication can be found in setup.sh.
To start running locally create a database (capstone), then make a virtual environment for the project as per python documaentation and from the venv install requierments using pip install -r requierments.txt and set the environment variables using 
- chmod +x setup.sh 
- source setup.sh
- flask run <!--to run app-->
- To run Tests creat a database (capstonetest) then use command python test_app.py

Error Handling
Errors are returned as JSON in the following format:

{
    "success": False,
    "error": 400,
    "message": "bad request"
}
The API will return four types of errors when requests fail:

400 – bad request
404 – resource not found
422 – unprocessable
401 - Authentication error

<Endpoints>

GET '/actors'

Fetches a JSON object with a list of actors in the database.
Request Arguments: None
Returns: An object with two keys, success with a value "True" , and actors that contains multiple objects with a series of string key pairs.
{
    "actors": [
        {
            "age": "50",
            "gender": "female",
            "id": 1,
            "name": "Angileena"
        }
    ],
    "success": true
}

GET '/movies'

Fetches a JSON object with a list of movies in the database.
Request Arguments: None
Returns: An object with two keys, success with a value "True:, and movies that contains multiple objects with a series of string key pairs.
{
    "movies": [
        {
            "id": 1,
            "release_date": "2014",
            "title": "The Equilizer"
        }
    ],
    "success": true
}
POST '/add-actor'

Posts a new actor to the database, including the name, age, gender, and actor ID, which is automatically assigned upon insertion.
Request Arguments: Requires three string arguments: name, age, gender.
Returns: An actor object with the age, gender, actor ID, and name.
{
    "actor": {
        "age": "53",
        "gender": "male",
        "id": 2,
        "name": "Denzel Washington"
    },
    "success": true
}
POST '/add-movie'

Posts a new movie to the database, including the title, release, and movie ID, which is automatically assigned upon insertion.
Request Arguments: Requires two string arguments: title, release.
Returns: A movie object with the movie ID, release, and title.
{
    "movie": {
        "id": 2,
        "release": "2011",
        "title": "Wanted"
    },
    "success": true
}
PATCH '/actors/int:actor_id'

Patches an existing actor in the database.
Request arguments: Actor ID, included as a parameter following a forward slash (/), and the key to be updated passed into the body as a JSON object. For example, to update the age for '/actors/6'
{
	"age": "57"
}
Returns: An actor object with the full body of the specified actor ID.
{
    "actor": {
        "age": "57",
        "gender": "male",
        "id": 2,
        "name": "Denzel Washington"
    },
    "success": true
}
PATCH '/movies/int:movie_id'

Patches an existing movie in the database.
Request arguments: Movie ID, included as a parameter following a forward slash (/), and the key to be updated, passed into the body as a JSON object. For example, to update the age for '/movies/5'
{
	"release_date": "2012"
}
Returns: A movie object with the full body of the specified movie ID.
{
    "movie": {
        "id": 1,
        "release_date": "2012",
        "title": "The Equilizer"
    },
    "success": true
}
DELETE '/actors/int:actor_id'

Deletes an actor in the database via the DELETE method and using the actor id.
Request argument: Actor id, included as a parameter following a forward slash (/).
Returns: ID for the deleted question and status code of the request.
{
	'delete': 2,
	'success': true
}
DELETE '/movies/int:movie_id'

Deletes a movie in the database via the DELETE method and using the movie id.
Request argument: Movie id, included as a parameter following a forward slash (/).
Returns: ID for the deleted question and status code of the request.
{
	'delete': 2,
	'success': true
}



