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
  show = db.relationship('Show', backref='venue', lazy="joined", cascade="all, delete")

  def __repr__(self):
    return f'<Venue {self.id} {self.name} {self.city} {self.state}>'
    

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
    show = db.relationship('Show', backref='artist', lazy="joined", cascade="all, delete")

    def __repr__(self):
        return f'<Artist {self.id} {self.name} {self.city} {self.state}>'


class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'),  nullable=False)
  start_time = db.Column(db.DateTime(), nullable=False)
