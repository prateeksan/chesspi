import pgn
from app import db, models

class GameParser:
    """Init with a pgn to parse into an object that is db ready.
    Populate the Game table with parsed games.
    Unparse games and return them as pgns or strings."""

    def __init__(self, pgn=None, game_id=None):
        """Init the GameParser either with a pgn string or with a game id.
        Game id should correspond with the Game.id in the database."""

        self.pgn = pgn
        self.game_id = game_id
        self.parsed_games = pgn.loads(self.pgn) if self.pgn else None

    def add_games(self):
        """If pgn was provided and parsed, adds games from pgn to the db"""

        if self.parsed_games:
            for game in parsed_games:
                self.__add_game(game)

    def __add_game(self, game):
        """Takes a single game object and adds it to the Game table in the db"""

        moves_string = (',').join(game.moves)
        db_game = models.Game(
                event=game.event,
                site=game.site,
                date=game.date,
                match_round=game.round,
                result=game.result,
                white_elo=game.whiteelo,
                black_elo=game.blackelo,
                moves=game.moves
            )
        db.session.add(db_game)
        db.session.commit()
