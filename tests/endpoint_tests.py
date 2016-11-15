#!flask/bin/python
import os
import unittest
import sys
import json

# Set path to parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import basedir
from sample_data.games_string import SAMPLE_GAMES_STRING

from app import app, db
from app.common.game_parser import GameParser

class EndpointTests(unittest.TestCase):
  """This class tests all endpoints"""

  def setUp(self):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
    self.app = app.test_client()
    db.create_all()

    # Import sample games used for tests
    gp = GameParser(pgn_string=SAMPLE_GAMES_STRING, verbose=False)
    gp.add_games()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def test_root(self):
    """Test root endpoint"""
    rv = self.app.get('/')
    data = self.__get_json(rv)
    assert 'chesspi' in data
    assert 'sample_calls' in data

  #######################
  # Tests for /games
  #######################

  def test_get_games(self):
    """Test games endpoint"""
    rv = self.app.get('/games')
    data = self.__get_json(rv)
    assert len(data) == 3
    assert data[0]['white'] == 'Chandler, Murray G'
    assert data[2]['eco'] == 'B45'

  def test_get_games_pgn_format(self):
    """Test games endpoint pgn format"""
    rv = self.app.get('/games?format=pgn')
    data = self.__get_string(rv)
    assert '[White \\"Chandler, Murray G\\"]\\n[Black \\"Kasparov, Gary\\"]' in data
    assert '[White \\"Kasparov, Gary\\"]\\n[Black \\"Grinberg, Nir\\"]' in data

  def test_get_games_by_name(self):
    """Test games endpoint by name"""
    rv = self.app.get('/games?name=chandler')
    data = self.__get_json(rv)
    assert len(data) == 1
    assert data[0]['white'] == 'Chandler, Murray G'

  def test_get_games_by_eco(self):
    """Test games endpoint by eco"""
    rv = self.app.get('/games?eco=b45')
    data = self.__get_json(rv)
    assert len(data) == 1
    assert data[0]['eco'] == 'B45'

  def test_get_games_by_name_and_eco(self):
    """Test games endpoint by eco and name"""
    rv = self.app.get('/games?name=kasparov&eco=b45')
    data = self.__get_json(rv)
    assert len(data) == 1
    assert data[0]['eco'] == 'B45'
    assert data[0]['white'] == 'Kasparov, Gary'

  def test_get_single_game(self):
    """Test games endpoint"""
    rv = self.app.get('/games/1')
    data = self.__get_json(rv)
    assert data['date'] == '1976.08.27'
    assert data['white'] == 'Chandler, Murray G'
    assert data['black'] == 'Kasparov, Gary'

  def test_get_single_game_pgn_format(self):
    """Test games endpoint"""
    rv = self.app.get('/games/1?format=pgn')
    data = self.__get_string(rv)
    assert '[White \\"Chandler, Murray G\\"]\\n[Black \\"Kasparov, Gary\\"]' in data

  #######################
  # Tests for /players
  #######################

  def test_get_players(self):
    """Test players endpoint"""
    rv = self.app.get('/players')
    data = self.__get_json(rv)
    assert data[0]['last_name'] == 'Chandler'
    assert data[1]['last_name'] == 'Kasparov'

  def test_get_single_player(self):
    """Test players endpoint"""
    rv = self.app.get('/players/2')
    data = self.__get_json(rv)
    assert data['last_name'] == 'Kasparov'
  
  def test_search_players(self):
    """Test players endpoint"""
    rv = self.app.get('/players?name=gary')
    data = self.__get_json(rv)
    assert data[0]['last_name'] == 'Kasparov'

  #######################
  # Tests for /eco_codes
  #######################

  def test_eco_codes(self):
    """Test eco_codes endpoint"""
    rv = self.app.get('/eco_codes')
    data = self.__get_json(rv)
    assert len(data) > 0
    assert data[0] == 'B22'

  #######################
  # Utilities
  #######################

  def __get_json(self, request):
    return json.loads(self.__get_string(request))

  def __get_string(self, request):
    return request.get_data().decode('utf-8')

if __name__ == '__main__':
  unittest.main()