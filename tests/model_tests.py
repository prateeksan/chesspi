#!flask/bin/python
import os
import unittest
import sys
import pgn
import pdb
# Set path to parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import basedir
from sample_data.games_string import SAMPLE_GAMES_STRING

from app import app, db
from app import models

sample_games = pgn.loads(SAMPLE_GAMES_STRING)
sample_game = sample_games[0]

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
    game = self.__create_test_game()
    game_from_db = models.Game.query.get(1)
    assert (
      game_from_db == game and
      game_from_db.eco == sample_game.eco
    )

  def test_read_game(self):
    """Query a game by id and read its fields"""
    game = self.__create_test_game()
    game_from_db = models.Game.query.get(1)
    assert (
      game_from_db.event == sample_game.event and
      game_from_db.site == sample_game.site and
      game_from_db.date == sample_game.date and
      game_from_db.match_round == sample_game.round and
      game_from_db.result == sample_game.result and
      game_from_db.white_elo == sample_game.whiteelo and
      game_from_db.black_elo == sample_game.blackelo and
      game_from_db.eco == sample_game.eco
      )

  def test_update_game(self):
    """Update fields of a game in db"""
    game = self.__create_test_game()
    game_from_db = models.Game.query.get(1)
    game_from_db.site = 'Mars'
    db.session.add(game_from_db)
    # Read game from db again
    reread_game = models.Game.query.get(1)
    assert reread_game.site == 'Mars'

  def test_delete_game(self):
    """Delete game entry from db with game id"""
    game = self.__create_test_game()
    models.Game.query.filter_by(id=1).delete()
    games_count = len(models.Game.query.all())
    assert games_count == 0

  def test_create_player(self):
    """Create a player entry in db"""
    player = self.__create_mock_player()
    assert player == models.Player.query.get(1)

  def test_player_full_name(self):
    """Test Player.full_name method"""
    player = self.__create_mock_player()
    assert player.full_name() == 'Carlsen, Magnus'

  def test_update_player(self):
    """Update fields of a player in db"""
    player = self.__create_mock_player()
    player.first_name = 'Test'
    db.session.add(player)
    reread_player = models.Player.query.get(1)
    assert reread_player.first_name == 'Test'

  def test_delete_player(self):
    """Delete player entry from db with game id"""
    player = self.__create_mock_player()
    models.Player.query.filter_by(id=1).delete()
    players_count = len(models.Player.query.all())
    assert players_count == 0

  def test_create_pairing(self):
    """Create a pairing entry in db"""
    pairing = self.__create_mock_pairing()
    assert (pairing.game_id == pairing.player_id == 1 and
            pairing.color == 'white')

  def test_pairing_backrefs(self):
    """Check backrefs for both Player and Game in a pairing"""
    pairing = self.__create_mock_pairing()
    game = models.Game.query.get(1)
    player = models.Player.query.get(1)
    assert (len(game.players) == 1 and
            game.players[0] == player and
            len(player.games) == 1 and
            player.games[0] == game)

  def test_delete_pairing(self):
    """Delete a pairing from the db"""
    pairing = self.__create_mock_pairing()
    models.Pairing.query.filter_by(player_id=1, game_id=1).delete()
    game = models.Game.query.get(1)
    player = models.Player.query.get(1)
    assert len(game.players) == len(player.games) == 0

  def __create_test_game(self):
    """Creates a test game in db"""
    game = models.Game(
      event=sample_game.event,
      site=sample_game.site,
      date=sample_game.date,
      match_round=sample_game.round,
      result=sample_game.result,
      white_elo=sample_game.whiteelo,
      black_elo=sample_game.blackelo,
      eco=sample_game.eco,
      moves=(",").join(sample_game.moves),
      )
    db.session.add(game)
    db.session.commit()
    return game

  def __create_mock_player(self):
    """Creates a mock player in db"""
    player = models.Player(
      first_name='Magnus',
      last_name='Carlsen'
      )
    db.session.add(player)
    db.session.commit()
    return player

  def __create_mock_pairing(self):
    """Creates a mock pairing in db
    and calls private methods to create mock player and game"""
    player = self.__create_mock_player()
    game = self.__create_test_game()
    pairing = models.Pairing(game_id=game.id, 
                              player_id=player.id,
                              color='white')
    db.session.add(pairing)
    db.session.commit()
    return pairing

if __name__ == '__main__':
  unittest.main()