#!flask/bin/python
import os
import unittest
import sys
import pgn
# Set path to parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import basedir
from sample_data.games_string import SAMPLE_GAMES_STRING

from app import app, db
from app import models
from app.common.game_parser import GameParser

class GameParserTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_game_parser_init(self):
        """Test the __init__() function of GameParser"""
        gp = GameParser(pgn_string=SAMPLE_GAMES_STRING)
        print('\n===========================================================')
        print("\nShould init GameParser with a pgn string containing 3 games.")
        print('\n===========================================================\n')
        assert len(gp.parsed_games) == 3

    def test_add_games(self):
        """Test the add_games method after providing pgn_string"""
        gp = GameParser(pgn_string=SAMPLE_GAMES_STRING)
        gp.add_games()

        players = models.Player.query.all()
        players_added = len(players) == 4

        games = models.Game.query.all()
        games_added = len(games) == 3

        pairings = models.Pairing.query.all()
        pairings_added = len(pairings) == 6

        print('\n===========================================================')
        print("\nShould add 3 games to db along with players and pairings.")
        print('\n===========================================================\n')
        assert players_added and games_added and pairings_added

    def test_player_in_db(self):
        """Tests whether a player is added to db properly without duplicates.
        And whether player_in_db can return its id or None for no matches"""
        gp = GameParser(pgn_string=SAMPLE_GAMES_STRING)
        gp.add_games()
        test_player = {'first_name':'Gary', 'last_name':'Kasparov'}
        false_player = {'first_name':'Gary', 'last_name':'Carlsen'}
        player_in_db = gp.player_in_db(test_player)
        false_player_in_db = gp.player_in_db(false_player)
        test_player_count = models.Player.query.filter_by(first_name='Gary',
                                                            last_name='Kasparov').count()

        print('\n===========================================================')
        print("\nKasparov should be added to db only once.")
        print("\nGameParser(games).player_in_db method should return player id or None.")
        print('\n===========================================================\n')
        assert (player_in_db is not None and
                isinstance(player_in_db, int) and
                test_player_count == 1 and
                not false_player_in_db)

    def test_unparse_game(self):
        """Tests whether unparse_game can query the db for a game and
        return it in the correct format (see format_game tests for more semantics). 
        Also tests if it can return None when no ID provided."""
        gp = GameParser(pgn_string=SAMPLE_GAMES_STRING)
        gp.add_games()
        # Should return None
        test_no_id = gp.unparse_game()

        gp2 = GameParser(game_id=1)
        test_with_id = gp2.unparse_game(return_type='dict')

        print('\n===========================================================')
        print("\nMethod unparse_game should return None if no id provided.")
        print("\nIt should return a game in chosen format when provided a valid id")
        print('\n===========================================================\n')
        assert (test_with_id and not 
                test_no_id and
                test_with_id['eco'] == 'B22')

    def test_format_game(self):
        """Method format_game should return games in specified format.
        It should return a pgn string if format not specified."""
        gp = GameParser(pgn_string=SAMPLE_GAMES_STRING)
        gp.add_games()
        game_1 = models.Game.query.get(1)
        # Return type 'dict' and 'json' can be used interchangably
        # 'dict' has been tested in unparse_games test
        game_dict = gp.format_game(game_1, return_type='json')
        dict_check = (game_dict['event'] == 'Wch U16' and
                    game_dict['site'] == 'Wattignies' and
                    game_dict['white'] == 'Chandler, Murray G' and
                    game_dict['black'] == 'Kasparov, Gary')
        # format_game should return pgn by default
        game_pgn = gp.format_game(game_1)
        # Loads an array of games
        loaded_pgn = pgn.loads(game_pgn)
        pgn_check = (isinstance(game_pgn, str) and
                    len(loaded_pgn) == 1 and
                    loaded_pgn[0].event == 'Wch U16' and
                    loaded_pgn[0].site == 'Wattignies')
        print('\n===========================================================')
        print("\nMethod format_game should return games in specified format.")
        print("\nIt should return a pgn string if format not specified")
        print('\n===========================================================\n')
        assert (dict_check and pgn_check)

    def test_format_games(self):
        """Returns a list of formatted games in given return type"""
        gp = GameParser(pgn_string=SAMPLE_GAMES_STRING)
        gp.add_games()
        games = models.Game.query.all()
        # Should return list of pgn strings by default
        formatted_games = gp.format_games(games)
        print('\n===========================================================')
        print("\nReturns a list of formatted games in given return type.")
        print('\n===========================================================\n')
        assert (len(games) == len(formatted_games) and 
                isinstance(formatted_games[0], str))

    def test_get_games(self):
        """Docstring here"""

    def test_get_game(self):
        """Docstring here"""

if __name__ == '__main__':
    unittest.main()