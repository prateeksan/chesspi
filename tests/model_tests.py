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

class ModelTests(unittest.TestCase):
  """This class tests all models"""

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_game(self):
      """Create a Game entry in db"""

    def test_read_game(self):
      """Query a game by id and read its fields"""

    def test_update_game(self):
      """Update fields of a game in db"""

    def test_delete_game(self):
      """Delete game entry from db with game id"""

    def test_create_player(self):
      """Create a player entry in db"""

    def test_read_player(self):
      """Query a player by id and read its fields"""

    def test_update_player(self):
      """Update fields of a player in db"""

    def test_delete_player(self):
      """Delete player entry from db with game id"""

    def test_player_full_name(self):
      """Test Player.full_name method"""

  if __name__ == '__main__':
    unittest.main()