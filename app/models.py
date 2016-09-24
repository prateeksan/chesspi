from app import db

class Pairing(db.Model):
    """This table creates many_to_many associations between players and games
    it also stores the colour of the player in that game as either 'W' or 'B'
    """
    __tablename__ = 'pairings'

    id = db.Column('id', db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('Game.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('Player.id'))
    color = db.Column('colour', db.String(32))

    def __repr__(self):
        return ('<Pairing: game_id: %r, player_id: %r, color: %r>' % 
                (self.game_id, self.player_id, self.color))


class Game(db.Model):
    """This table stores games with moves and other info."""

    __tablename__ = 'Game'

    id = db.Column(db.Integer, primary_key=True)
    pgn = db.Column(db.String(120), index=True, unique=True)
    players = db.relationship('Player', secondary='pairings', backref='Game')

    def __repr__(self):
        return '<Game %r>' % (self.id)

class Player(db.Model):
    """This table stores player names and other player constants."""

    __tablename__ = 'Player'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    games = db.relationship('Game', secondary='pairings', backref='Player')

    def __repr__(self):
      return '<Player %r, %r %r>' % (self.last_name, self.first_name, self.middle_name)
