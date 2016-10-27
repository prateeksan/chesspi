# Script to import the sample games into the database.

from app.common.game_parser import GameParser
from app import models, db
from sample_data.games_string import SAMPLE_GAMES_STRING

# Reset Game and Pairing Table
# Comment this out if you don't want to reset your games
try:
    num_pairings = models.Pairing.query.delete()
    num_games = models.Game.query.delete()
    db.session.commit()
    print('Deleted {} Games and {} Pairings'.format(num_games, num_pairings))
except:
    db.session.rollback()

# Import sample games used for tests
gp = GameParser(pgn_string=SAMPLE_GAMES_STRING, verbose=True)
gp.add_games()

# Import the first 20 games in kasparov.pgn
# TODO: Optimize the GameParser because it takes way too
#       long to parse large numbers of games
with open('sample_data/kasparov.pgn', 'r', encoding = "ISO-8859-1") as myfile:
    games_data=''.join(myfile.readlines()[0:341])

gp = GameParser(pgn_string=games_data, verbose=True)
gp.add_games()


