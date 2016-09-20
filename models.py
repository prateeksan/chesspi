from api import db

class Game(db.Model):

    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    pgn = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<Game %r>' % (self.id)