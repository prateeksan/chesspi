from app import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pgn = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<Game %r>' % (self.id)