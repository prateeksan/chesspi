from app import db

class Pairing(db.Model):
    """This table creates many_to_many associations between players and games
    it also stores the colour of the player in that game as either 'W' or 'B'
    """
    __tablename__ = 'pairings'

    id = db.Column('id', db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    color = db.Column('colour', db.String(32))

    def __repr__(self):
        return ('<Pairing: game_id: %r, player_id: %r, color: %r>' % 
                (self.game_id, self.player_id, self.color))


class Game(db.Model):
    """This table stores games with moves and other info."""

    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(64))
    site = db.Column(db.String(64))
    date = db.Column(db.String(32))
    # Since round is a built-in python function, we will use match_round
    match_round = db.Column(db.Integer)
    result = db.Column(db.String)
    white_elo = db.Column(db.Integer)
    black_elo = db.Column(db.Integer)
    eco = db.Column(db.String(32))
    # TODO(limit text size for moves, sqlite3 can't do this so it needs to be done manually)
    moves = db.Column(db.Text())
    players = db.relationship('Player', secondary='pairings', backref='game')
    # TODO(add a sensible unique constraint)
    def __repr__(self):
        return '<Game %r>' % (self.id)

class Player(db.Model):
    """This table stores player names and other player constants."""

    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    games = db.relationship('Game', secondary='pairings', backref='player')

    def __repr__(self):
      return '<Player %r, %r %r>' % (self.last_name, self.first_name, self.middle_name)
