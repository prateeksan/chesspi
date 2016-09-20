# Code for database models
import pgn

print('loading games')
games_input = open('sample_data/kasparov.pgn', encoding = "ISO-8859-1").read()
games = pgn.loads(games_input)