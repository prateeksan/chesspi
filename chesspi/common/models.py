# Code for database models
import pgn

print('loading games')
games_input = open('sample_data/kasparov.pgn').read()
games = pgn.loads(games_input)