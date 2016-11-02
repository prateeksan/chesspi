#!flask/bin/python
import os
import unittest
import sys
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
        """Docstring here"""

    def test_format_game(self):
        """Docstring here"""

    def test_format_games(self):
        """Docstring here"""

    def test_get_games(self):
        """Docstring here"""

    def test_get_game(self):
        """Docstring here"""

if __name__ == '__main__':
    unittest.main()