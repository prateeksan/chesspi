class GameParser:
    """Init with a pgn to parse into an object that is db ready.
    Populate the Game table with parsed games.
    Unparse games and return them as pgns or strings."""

    def __init__(self, pgn=None, game_id=None):
        """Init the GameParser either with a pgn string or with a game id.
        Game id should correspond with the Game.id in the database."""

        self.pgn = pgn
        self.game_id = game_id
        self.parsed_games = []

