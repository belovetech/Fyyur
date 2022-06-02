from datetime import datetime
from config import db
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Venue(db.Model):
  __tablename__ = 'Venue'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  city = db.Column(db.String(120), nullable=False)
  state = db.Column(db.String(120), nullable=False)
  address = db.Column(db.String(120), nullable=False)
  phone = db.Column(db.String(120), nullable=True)
  image_link = db.Column(db.String(500), nullable=True)
  genres = db.Column(db.ARRAY(db.String), nullable=False)
  facebook_link = db.Column(db.String(120), nullable=True)
  website_link = db.Column(db.String(120),nullable=True)
  seeking_talent = db.Column(db.Boolean, default=False)
  seeking_description = db.Column(db.String(), nullable=True)
  show = db.relationship('Show', backref='venue', lazy="joined")

  def __repr__(self):
    return f'<Venue {self.id} {self.name} {self.city} {self.state}>'
    

# TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    website_link = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(), nullable=True)
    show = db.relationship('Show', backref='artist', lazy="joined")

    # def num_upcoming_shows(self):
    #   return self.query.join(Show).filter_by(artist_id=self.id).filter(Show.start_time > datetime.now()).count()

    # def num_past_show(self):
    #   return self.query.join(Show).filter_by(artist_id=self.id).filter(Show.start_time < datetime.now()).count()

    # def upcoming_shows(self):
    #   return Show.get_upcoming_by_artist(Artist, self.id)

    # def past_shows(self):
    #   return Show.get_past_by_artist(Artist, self.id)

    # def show_details(self):
      # return {
      #   'venue_id': self.id,
      #   'venue_name': self.name,
      #   'venue_image_link': self.image_link,
      #   'start_time': str(self.show.start_time)
      # }

    def __repr__(self):
        return f'<Artist {self.id} {self.name} {self.city} {self.state}>'



# TODO: implement any missing fields, as a database migration using Flask-Migrate
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'),  nullable=False)
  start_time = db.Column(db.DateTime(), nullable=False)


  # def get_past_by_artist(cls, artist_id):
  #   shows = cls.query.filter_by(artist_id=artist_id).filter(Show.start_time < datetime.now()).all()
  #   return [show.show_details() for show in shows]

  # def get_upcoming_by_artist(cls, artist_id):
  #   shows = cls.query.filter_by(artist_id=artist_id).filter(Show.start_time > datetime.now()).all()
  #   return [show.show_details() for show in shows]


    
 

  # db.create_all()