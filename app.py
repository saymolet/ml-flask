from flask import Flask, render_template, redirect, url_for, request
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
import requests
import os

# Create a Flask App, add Bootstrap
app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)
Bootstrap(app)

# Create a DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# API config. https://www.themoviedb.org/
MOVIE_DB_API_KEY = os.getenv("API_KEY")
MOVIE_DB_URL = "https://api.themoviedb.org/3"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"


class AddForm(FlaskForm):
    movie_title = StringField('Movie title', validators=[DataRequired()])
    submit = SubmitField('Find')


class MovieForm(FlaskForm):
    rating = StringField('Your rating out of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField('Your review')
    submit = SubmitField('Submit')


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(300))
    img_url = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    order = db.session.query(Movies).order_by("rating").all()

    for i in range(len(order)):
        order[i].ranking = len(order) - i
    db.session.commit()

    return render_template("index.html", all_movies=order)


@app.route("/edit", methods=['POST', 'GET'])
def edit():
    movie_id = request.args.get("id")
    movie = Movies.query.get(movie_id)

    form = MovieForm()
    if form.validate_on_submit():
        if form.review.data != "":
            movie.review = form.review.data
        movie.rating = form.rating.data
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("edit.html", movie=movie, form=form)


@app.route("/delete")
def delete():
    movie_id = request.args.get("id")
    movie = Movies.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=['POST', 'GET'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        params = {
            "api_key": MOVIE_DB_API_KEY,
            "query": form.movie_title.data
        }
        response = requests.get(url=f"{MOVIE_DB_URL}/search/movie", params=params)
        movie_list = response.json()["results"]
        return render_template("select.html", movie_list=movie_list)

    return render_template("add.html", form=form)


@app.route('/select', methods=['POST', 'GET'])
def select():
    movie_id = request.args.get("id")
    if movie_id:
        response = requests.get(url=f"{MOVIE_DB_URL}/movie/{movie_id}", params={"api_key": MOVIE_DB_API_KEY})
        data = response.json()

        title = data["title"]
        year = data["release_date"].split("-")[0]
        description = data["overview"]
        img_url = f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}"

        new_film = Movies(
            title=title,
            year=year,
            description=description,
            img_url=img_url
        )
        db.session.add(new_film)
        db.session.commit()

        # find a database id of the freshly added movie and pass it to edit page
        movie = Movies.query.filter_by(title=title).first()

        return redirect(url_for('edit', id=movie.id))
    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
