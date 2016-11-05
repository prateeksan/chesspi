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

SAMPLE_GAMES = pgn.loads(SAMPLE_GAMES_STRING)

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
    sample_game = SAMPLE_GAMES[0]
    game = models.Game(
      event=sample_game.event,
      site=sample_game.site,
      date=sample_game.date,
      match_round=sample_game.round,
      result=sample_game.result,
      white_elo=sample_game.whiteelo,
      black_elo=sample_game.blackelo,
      eco=sample_game.eco,
      )
    db.session.add(game)
    db.session.commit()
    game_from_db = models.Game.query.get(1)
    print('\n===========================================================')
    print("\nShould add 1 game to db.")
    print('\n===========================================================\n')
    assert (
      game_from_db and
      game_from_db.id == 1 and
      game_from_db.eco == sample_game.eco
    )

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

  def test_create_pairing(self):
    """Create a pairing entry in db"""

  def test_pairing_backrefs(self):
    """Check backrefs for both Player and Game in a pairing"""

  def test_delete_pairing(self):
    """Delete a pairing from the db"""

if __name__ == '__main__':
  unittest.main()