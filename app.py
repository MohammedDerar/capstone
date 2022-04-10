
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  # CORS(app)
  CORS(
    app,
    origins='*',
    methods=['GET', 'POST', 'DELETE', 'PATCH'],
    allow_headers=['Authorization', 'Content-Type']
)

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods',
                            'GET,PATCH,POST,DELETE')
      return response
  # to check if app is running
  @app.route('/')
  def health():
    return jsonify({'health': 'Running!!'}), 200

  # Get All Movies
  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies(payload):
    movies=Movie.query.all()
    if not movies:
      abort(404)
    movies_list=[]
    for movie in movies:
      movies_list.append(movie.format())
    return jsonify({
        'success':True,
        'movies':movies_list
    }), 200

  # Post a New Movie
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movie')
  def create_new_movie(payload):
    body = request.get_json()
    if 'title' not in body or 'release_date' not in body: #((body['title'] is None) or (body['release_date'] is None)):
      abort(400)
    new_title = body.get('title')
    new_date = body.get('release_date')
    try:
      new_movie = Movie(title=new_title, release_date=new_date)
      new_movie.insert()
      return jsonify({
      'success':True,
      'movies':new_movie.format()
       }), 200
    except:
      abort(422)


  # Update a Movie
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movie')
  def update_movie(payload, movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()
    if movie is None:
      abort(404)
    try:
      body = request.get_json()
      updated_title = body.get('title')
      updated_date = body.get('release_date')
      if updated_title:
        movie.title = updated_title
      if updated_date:
        movie.release_date = updated_date
      movie.update()
      return jsonify({
      'success': True,
      'movies': movie.format()
       }), 200
    except:
      abort(422)
    
    
  # Delete Movie
  @app.route('/movies/<int:movie_id>',methods=['DELETE'])
  @requires_auth('delete:movie')
  def delete_movie(payload,movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()
    if movie is None:
      abort(404)
    try:
        movie.delete()
        return jsonify({
            'success':True,
            'deleted':movie_id
        }), 200

    except:
        abort(422)


  # Get All Actors
  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors(payload):
    actors=Actor.query.all()
    if not actors:
      abort(404)
    actors_list=[]
    for actor in actors:
      actors_list.append(actor.format())
    return jsonify({
        'success':True,
        'actors':actors_list
    }), 200

  # Post a New Actor
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actor')
  def create_new_actor(payload):
    body = request.get_json()
    if 'name' not in body or 'age' not in body or 'gender' not in body: 
      abort(400)
    new_name = body.get('name')
    new_age = body.get('age')
    new_gender = body.get('gender')
    try:
      new_actor = Actor(name=new_name, age=new_age, gender=new_gender)
      new_actor.insert()
      return jsonify({
      'success':True,
      'actors':new_actor.format()
       }), 200
    except:
      abort(422)


  # Update Actor
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actor')
  def update_actor(payload, actor_id):
    print(actor_id)
    actor = Actor.query.filter_by(id=actor_id).first()
    if actor is None:
      abort(404)
    try:
      body = request.get_json()
      updated_name = body.get('name')
      updated_age = body.get('age')
      updated_gender = body.get('gender')
      if updated_name:
        actor.name = updated_name
      if updated_age:
        actor.age = updated_age
      if updated_gender:
        actor.gender = updated_gender
      actor.update()
      return jsonify({
      'success': True,
      'actors': actor.format()
       }), 200
    except:
      abort(422)
    
    
  # Delete Actor
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actor')
  def delete_actor(payload, actor_id):
    actor = Actor.query.filter_by(id=actor_id).first()
    if actor is None:
      abort(404)
    try:
        actor.delete()
        return jsonify({
            'success':True,
            'deleted':actor_id
        }), 200

    except:
        abort(422)

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
      }), 422



  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
      }), 404

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
      }), 400

  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "method not allowd"
      }), 405



  @app.errorhandler(AuthError)
  def auth_error(error):
      return jsonify({
          "success": False,
          "error": error.status_code,
          "message": error.error['description']
      }), error.status_code


  


  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='127.0.0.1', port=8080, debug=True)