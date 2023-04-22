import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
    return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
    return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show_summary', methods=['POST'])
def show_summary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)
    except IndexError:
        flash('Sorry, that email was not found')
        return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchase_places', methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    date = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
    book_authorized = True  # bolean to ckeck if the book is authorized
    if date < datetime.now():
        flash('You can\'t book for a past competition')
        book_authorized = False
    if places_required > int(competition['numberOfPlaces']):
        flash('No enough places for this competition')
        book_authorized = False
    if places_required > 12:
        flash('You can\'t book more than 12 points')
        book_authorized = False
    if int(club['points']) < places_required:
        flash('You don\'t have enough points')
        book_authorized = False
    if book_authorized:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-places_required
        club['points'] = int(club['points'])-places_required
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/show_points', methods=['GET'])
def show_points():
    return render_template('pointTable.html', clubs=clubs, competitions=competitions)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
