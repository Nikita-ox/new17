# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api.app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 4}

movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

    def __repr__(self):
        return self.title


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


db.create_all()


@movies_ns.route('/')
class MovieView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        movies = Movie.query

        if director_id:
            movies = movies.filter(Movie.director_id == director_id)
        if genre_id:
            movies = movies.filter(Movie.genre_id == genre_id)
        movies = movies.all()
        return MovieSchema(many=True).dump(movies), 200

    def post(self):
        data = request.get_json()
        new_movie = Movie(**data)
        db.session.add(new_movie)
        db.session.commit()
        db.session.close()

        return '', 201


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        try:
            movie = Movie.query.get(mid)
            return MovieSchema().dump(movie), 200
        except Exception:
            return "", 404

    def put(self, mid):
        data = request.get_json()
        movie = Movie.query.get(mid)
        movie.id = data['id']
        movie.title = data['title']
        movie.description = data['description']
        movie.year = data['year']
        movie.rating = data['rating']
        movie.genre_id = data['genre_id']
        movie.director_id = data['director_id']

        db.session.add(movie)
        db.session.commit()
        db.session.close()

    def delete(self, mid):
        movie = Movie.query.get(mid)

        db.session.delete(movie)
        db.session.commit()
        db.session.close()


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = Director.query.all()
        return DirectorSchema(many=True).dump(directors), 200

    def post(self):
        data = request.get_json()
        new_director = Director(**data)
        db.session.add(new_director)
        db.session.commit()
        db.session.close()

        return '', 201


@directors_ns.route('/<int:did>')
class DirectorsView(Resource):
    def get(self, did):
        try:
            director = Director.query.get(did)
            return DirectorSchema().dump(director), 200
        except Exception:
            return "", 404

    def put(self, mid):
        data = request.get_json()
        director = Movie.query.get(mid)
        director.id = data['id']
        director.name = data['name']


        db.session.add(movie)
        db.session.commit()
        db.session.close()



    def delete(self, mid):
        director = Director.query.get(mid)

        db.session.delete(director)
        db.session.commit()
        db.session.close()



@genres_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        genres = Genre.query.all()
        return DirectorSchema(many=True).dump(genres), 200

    def post(self):
        data = request.get_json()
        new_genres = Genre(**data)
        db.session.add(new_genres)
        db.session.commit()
        db.session.close()

        return '', 201


@genres_ns.route('/<int:did>')
class DirectorsView(Resource):
    def get(self, did):
        try:
            genres = Director.query.get(did)
            return DirectorSchema().dump(genres), 200
        except Exception:
            return "", 404

    def put(self, mid):
        data = request.get_json()
        genres = Genre.query.get(mid)
        genres.id = data['id']
        genres.name = data['name']


        db.session.add(genres)
        db.session.commit()
        db.session.close()



    def delete(self, mid):
        genres = Genre.query.get(mid)

        db.session.delete(genres)
        db.session.commit()
        db.session.close()


if __name__ == '__main__':
    app.run(debug=True)
