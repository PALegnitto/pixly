"""Models for pixly"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)

class Image(db.Model):

    __tablename__ = "images"

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    version = db.Column(db.Integer,
                    primary_key = True,
                    nullable = False)
    photo_url = db.Column(db.Text,
                    nullable = False)
