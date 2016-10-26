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
        print("\nShould init GameParser with a pgn string containing 3 games.\n")
        assert len(gp.parsed_games) == 3

    def test_add_games(self):
        """Test the add_games method after providing pgn_string"""
        gp = GameParser(pgn_string=SAMPLE_GAMES_STRING)
        gp.add_games()
        print('\n===========================================================')
        print("\nShould add 3 games to db along with players and pairings.\n")
        assert True

if __name__ == '__main__':
    unittest.main()