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
                # Returns dict like: {white: <id>, black: <id>}
                db_player_ids = self.__add_players(white=game.white, 
                                                    black=game.black)
                db_game_id = self.__add_game(game)
                self.__add_pairings(game_id=db_game_id,
                                    player_ids=db_player_ids)

    def player_in_db(player):
        """Takes a player name and checks if player in db
        If present, it returns the player id,
        else returns None"""

        # TODO(complete this)

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
        return db_game.id

    def __add_players(self, white, black):
        """Adds players to db if players not in db.
        Returns dict like {'white': <id>, 'black': <id>}"""

        white_parsed = self.__parse_player_name(white)
        black_parsed = self.__parse_player_name(black)

        white_id = self.player_in_db(white_parsed)
        black_id = self.player_in_db(black_parsed)

        if not white_id:
            db_white = models.Player(
                    first_name= white_parsed['first_name'],
                    middle_name = white_parsed['middle_name'],
                    last_name = white_parsed['last_name']
                    )

        if not black_id:
            db_black = models.Player(
                    first_name= black_parsed['first_name'],
                    middle_name = black_parsed['middle_name'],
                    last_name = black_parsed['last_name']
                    )

        return {'white': white_id, 'black': black_id}


    def __parse_player_name(self, name_string):
        """Takes a player name string and returns a dict as:
        {'first_name': <string>, 'middle_name': <string>, last_name': <string>}
        """
        name_dict = {}

        # TODO(complete this)

    def __add_parings(self, game_id, player_id):
        """Receives a game_id and a dict with player ids,
        adds two pairings for white and black"""

        # TODO(complete this)
