import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie


class Casting_agencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.assistant_token = os.environ['assistant_token']
        self.director_token = os.environ['director_token']
        self.producer_token = os.environ['producer_token']
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstonetest"
        self.database_path = 'postgresql://postgres:123@localhost:5432/{}'.format(self.database_name)
        setup_db(self.app, self.database_path)

        self.new_actor={
            "name":"Angilena Jolie",
            "age":50,
            "gender":"female"
        }

        self.updated_actor = {
            "age": 57
        }

        self.new_movie={
            "title":"The Equilizer",
            "release_date":"2014"
        }

        self.updated_movie={
            "release_date":"2011"
        }



        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
# Actors -----
    
# test for getting actors (Pass and Fail)


    def test_get_actors_with_token(self):
        # insert actor into database
        actor = Actor(name="Denzel Washington", age=53, gender="male")
        actor.insert()
        res=self.client().get('/actors',  headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['actors']))

    def test_get_actors_without_token(self):
        # get actors without token
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"],False)
        self.assertEqual(data["message"], "Authorization Header Not Found!")


    # test for updating actor
    def test_update_actor_info(self):
        res = self.client().patch('/actors/2', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.updated_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    #test for creating a new actor (Pass and Fail cases)   
    def test_create_new_actor(self):
        res=self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.new_actor)

        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)

    def test_400_if_send_empty_json(self):
        res=self.client().post('/actors',headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json={})

        data=json.loads(res.data)
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'bad request')


    # test of deleting actor by a spesific id (Pass and Fail)
    def test_delete_actor(self):
        res=self.client().delete('actors/1', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
        data=json.loads(res.data)

        actor=Actor.query.filter(Actor.id==1).one_or_none()

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['deleted'])
        self.assertEqual(actor, None)


    def test_404_if_resource_not_found(self):
        res=self.client().delete('/actors/1000', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })

        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')




# Movies ----

#test for getting movies (Pass and Fail)
    def test_get_movies(self):
        #insert movie into database
        movie = Movie(title="Wanted", release_date="2000")
        movie.insert()
        res=self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['movies']))



#test for creating a new movie (Pass and Fail cases)   
    def test_create_new_movie(self):
        res=self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        }, json=self.new_movie)

        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)

    def test_400_if_send_empty_json(self):
        res=self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        }, json={})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'bad request')


    # test update movie
    def test_update_movie_info(self):
        res = self.client().patch('/movies/2', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.updated_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        


    # test of deleting movie by a spesific id (Pass and Fail)
    def test_delete_movie(self):
        res=self.client().delete('movies/1', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data=json.loads(res.data)

        movie=Movie.query.filter(Movie.id==1).one_or_none()

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['deleted'])
        self.assertEqual(movie, None)


    def test_404_if_resource_not_found(self):
        res=self.client().delete('/movies/1000', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })

        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')






# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
