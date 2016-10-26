import pgn
from app import db, models

class GameParser:
    """Init with a pgn to parse into an object that is db ready.
    Populate the Game table with parsed games.
    Unparse games and return them as pgns or strings."""

    def __init__(self, pgn_string=None, game_id=None):
        """Init the GameParser either with a pgn string or with a game id.
        Game id should correspond with the Game.id in the database."""

        self.pgn = pgn_string
        self.game_id = game_id
        self.parsed_games = pgn.loads(self.pgn) if self.pgn else None

    def unparse_game(self, return_type='json'):
        """If GameParser initialized with game_id rather than string,
        this method should return the game as a pgn string or json as per return_type.
        Default return_type is json"""
        if not self.game_id:
            return None
        game = models.Game.query.get(self.game_id)
        players = game.players
        pairing_1 = models.Pairing.query.filter_by(player_id=players[0].id,
                                            game_id=game.id).first()
        pairing_2 = models.Pairing.query.filter_by(player_id=players[1].id,
                                            game_id=game.id).first()
        if pairing_1.color == 'white':
            white_player = players[0]
            black_player = players[1]
        elif pairing_2.color == 'white':
            white_player = players[1]
            black_player = players[0]

        print('white: %s, %s'%(white_player.first_name, white_player.last_name))
        print('black: %s, %s'%(black_player.first_name, black_player.last_name))


    def add_games(self):
        """If pgn was provided and parsed, adds games from pgn to the db"""

        if self.parsed_games:
            for game in self.parsed_games:
                # Returns dict like: {white: <id>, black: <id>}
                db_player_ids = self.__add_players(white=game.white, 
                                                    black=game.black)
                db_game_id = self.__add_game(game)
                self.__add_pairings(game_id=db_game_id,
                                    player_ids=db_player_ids)
                db.session.expunge_all()

    def player_in_db(self, player, stringified=False):
        """Takes a player name and checks if player in db
        If present, it returns the player id, else returns None.
        If player is stringified, it parses the name into a dict.
        """

        if stringified:
            player = self.__parse_player_name(player)
        player_in_db = models.Player.query.filter_by(
                        first_name=player['first_name'],
                        last_name=player['last_name'])

        if player_in_db.count() > 0:
            return player_in_db.first().id
        else:
            return None

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
                moves=moves_string,
                eco = game.eco
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
                    last_name = white_parsed['last_name']
                    )
            db.session.add(db_white)

        if not black_id:
            db_black = models.Player(
                    first_name= black_parsed['first_name'],
                    last_name = black_parsed['last_name']
                    )
            db.session.add(db_black)

        db.session.commit()

        if not white_id:
            white_id = db_white.id
        if not black_id:
            black_id = db_black.id

        return {'white': white_id, 'black': black_id}


    def __parse_player_name(self, name_string):
        """Takes a player name string and returns a dict as:
        {'first_name': <string>, last_name': <string>}
        String argument excpected to follow the format:
        'LastName, FirstName M' or 'LastName, FirstName'
        first_name field includes middle name at the end.
        """
        name_dict = {}
        # Split by comma. First name may include middle name.
        name_array = name_string.split(',')
        name_dict['first_name'] = name_array[1].strip()
        name_dict['last_name'] = name_array[0].strip()
        return name_dict 

    def __add_pairings(self, game_id, player_ids):
        """Receives a game_id and a dict with player ids,
        adds two pairings for white and black"""

        black_pairing = models.Pairing(game_id=game_id,
                                        player_id=player_ids['black'],
                                        color='black')
        white_pairing = models.Pairing(game_id=game_id, 
                                        player_id = player_ids['white'],
                                        color='white')
        db.session.add(black_pairing)
        db.session.add(white_pairing)
        db.session.commit()
