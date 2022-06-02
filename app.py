#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask_moment import Moment
from email.policy import default
from tokenize import String
import dateutil.parser
import babel
from flask import Flask, jsonify, render_template, request, Response, flash, redirect, url_for, abort
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy import Integer
from forms import *
import sys
from config import app, db
from models import Venue, Artist, Show
from datetime import datetime as date

moment = Moment(app)
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------


@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    areas = db.session.query(Venue.city, Venue.state).distinct()
    data = []

    for venue in areas:
        venue = dict(zip(('city', 'state'), venue))
        venue['venues'] = []
        for venue_data in Venue.query.filter_by(
            city=venue['city'],
            state=venue['state']
        ).all():
            shows = Show.query.filter_by(
                venue_id=venue_data.id
            ).all()
            venues_data = {
                'id': venue_data.id,
                'name': venue_data.name,
                'new_upcoming_shows': len(shows)
            }
            venue['venues'].append(venues_data)
        data.append(venue)

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', None)

    venues = Venue.query.filter(
        Venue.name.ilike('%{}%'.format(search_term))).all()

    if venues:
        count_venues = len(venues)

    response = {
        "count": count_venues,
        "data": venues
    }

    return render_template(
        'pages/search_venues.html',
        results=response,
        search_term=request.form.get('search_term', '')
    )


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    # venue = Venue.query.filter_by(id=venue_id).first()
    venue = Venue.query.get_or_404(venue_id)

    num_shows = Show.query.filter_by(venue_id=venue.id).all()
    upcoming_shows = []
    past_shows = []

    for show in num_shows:
        artist = Artist.query.get(show.artist_id)
        show_data = {
            'venue_id': show.artist_id,
            'venue_name': artist.name,
            'venue_image_link': artist.image_link,
            'start_time': str(show.start_time)
        }
        if show.start_time <= date.now():
            past_shows.append(show_data)
        else:
            upcoming_shows.append(show_data)

    data = {
        'id': venue_id,
        'name': venue.name,
        'genres': venue.genres,
        'address': venue.address,
        'city': venue.city,
        'state': venue.state,
        'phone': venue.phone,
        'website_link': venue.website_link,
        'facebook_link': venue.facebook_link,
        'seeking_talent': venue.seeking_talent,
        'seeking_description': venue.seeking_description,
        'image_link': venue.image_link,
        'past_shows': past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    error = False
    try:
        form = VenueForm(request.form)

        # new_venue = Venue (
        #   name = form.name.data,
        #   city = form.city.data,
        #   state = form.state.data,
        #   address = form.address.data,
        #   phone = form.phone.data,
        #   genres = form.genres.data,
        #   facebook_link = form.facebook_link.data,
        #   website_link = form.website_link.data,
        #   image_link = form.image_link.data,
        #   seeking_talent = form.seeking_talent.data,
        #   seeking_description = form.seeking_description.data
        # )
        new_venue = Venue()
        form.populate_obj(new_venue)
        
        db.session.add(new_venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    error = False
    try:
        venue = Venue.query.filter_by(id=venue_id)
        db.session.delete(venue)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    return None

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    artists = Artist.query.all()
    return render_template('pages/artists.html', artists=artists)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    search_term = request.form.get('search_term', None)

    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    artists = Artist.query.filter(
        Artist.name.ilike("%{}%".format(search_term))).all()

    if artists:
        count_artists = len(artists)

    response = {
        "count": count_artists,
        "data": artists
    }

    return render_template(
        'pages/search_artists.html',
        results=response,
        search_term=request.form.get('search_term', '')
    )


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    artist = Artist.query.get(artist_id)

    num_shows = Show.query.filter_by(artist_id=artist.id).all()
    upcoming_shows = []
    past_shows = []

    for show in num_shows:
        venue = Venue.query.get(show.venue_id)
        show_data = {
            'venue_id': show.venue_id,
            'venue_name': venue.name,
            'venue_image_link': venue.image_link,
            'start_time': str(show.start_time)
        }
        if show.start_time <= date.now():
            past_shows.append(show_data)
        else:
            upcoming_shows.append(show_data)

    data = {
        'id': artist_id,
        'name': artist.name,
        'genres': artist.genres,
        'city': artist.city,
        'state': artist.state,
        'phone': artist.phone,
        'website_link': artist.website_link,
        'facebook_link': artist.facebook_link,
        'seeking_venue': artist.seeking_venue,
        'seeking_description': artist.seeking_description,
        'image_link': artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
        
        # "past_shows": artist.past_shows(),
        # "upcoming_shows": artist.upcoming_shows(),
        # "past_shows_count": artist.num_past_show(),
        # "upcoming_shows_count": artist.num_upcoming_shows()
    }

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    error = False
    try:
        artist = Artist.query.get(artist_id)
        form = ArtistForm(request.form)

        artist.name = form.name.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.website_link = form.website_link.data
        artist.image_link = form.image_link.data
        artist.genres = form.genres.data
        artist.facebook_link = form.facebook_link.data
        artist.seeking_venue = form.seeking_venue.data
        artist.seeking_description = form.seeking_description.data

        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully edited!')
    except:
        error = True
        print(sys.exc_info())
        db.session.rollback()
        flash(
            'An error occurred. Artist '
            + request.form['name']
            + ' could not be edited.'
        )
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    # TODO: populate form with values from venue with ID <venue_id>
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    try:
        venue = Venue.query.get(venue_id)
        form = VenueForm(request.form)

        venue.name = form.name.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.phone = form.phone.data
        venue.website_link = form.website_link.data
        venue.image_link = form.image_link.data
        venue.genres = form.genres.data
        venue.facebook_link = form.facebook_link.data
        venue.seeking_talent = form.seeking_talent.data
        venue.seeking_description = form.seeking_description.data

        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully edited!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash(
            'An error occurred. Artist '
            + request.form['name']
            + ' could not be edited.'
        )
    finally:
        db.session.close

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    try:
        form = ArtistForm(request.form)
    # TODO: modify data to be the data object returned from db insertion
        # new_artist = Artist(
        #   name = form.name.data,
        #   city = form.city.data,
        #   state = form.state.data,
        #   phone = form.phone.data,
        #   website_link = form.website_link.data,
        #   image_link = form.image_link.data,
        #   genres = form.genres.data,
        #   facebook_link = form.facebook_link.data,
        #   seeking_venue = form.seeking_venue.data,
        #   seeking_description = form.seeking_description.data
        # )

        new_artist = Artist()
        form.populate_obj(new_artist)
        db.session.add(new_artist)
        db.session.commit()
    # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        # TODO: on unsuccessful db insert, flash an error instead.
        flash(
            'An error occurred. Artist '
            + request.form['name']
            + ' could not be listed.'
        )
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    shows = Show.query.all()
    data = []

    for show in shows:
        show = {
            'venue_id': show.venue_id,
            'venue_name': db.session.query(
                Venue.name
            ).filter_by(
                id=show.venue_id
            ).first()[0],
            'artist_id': show.artist_id,
            'artist_name': db.session.query(
                Artist.name
            ).filter_by(
                id=show.artist_id
            ).first()[0],
            'artist_image_link': db.session.query(
                Artist.image_link
            ).filter_by(
                id=show.artist_id
            ).first()[0],
            'start_time': str(show.start_time)
        }
        data.append(show)

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    error = False
    try:
        form = ShowForm(request.form)
        artist_id=form.artist_id.data
        venue_id=form.venue_id.data
        start_time=form.start_time.data
        show = Show(artist_id=artist_id, venue_id=venue_id,start_time=start_time)

        db.session.add(show)
        db.session.commit()
    # on successful db insert, flash success
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')

    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
