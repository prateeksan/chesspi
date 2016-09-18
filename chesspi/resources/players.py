from flask_restful import Resource
import pgn

# Import games list
from chesspi import games

# Player
# Shows a single eco code
class Player(Resource):
    def get(self):
        # TODO: implement this if we have more detailed info on
        #       the individual players
        return {'name': games[0].black}

# PlayerList
# Shows a list of players and number of games in the database
class PlayerList(Resource):
    def get(self):

        # Loop through games and add each player to a counting dictionary
        player_dict = {} #key = player name, value = number of games
        for game in games:
            player_dict = add_player(player_dict, game.black)
            player_dict = add_player(player_dict, game.white)

        # Generate the output list
        player_list = []
        for key in player_dict:
            model = {}
            model['games_in_database'] = player_dict[key]

            names = key.split(',', 1)
            model['last_name'] = names[0].strip()
            
            if len(names) == 2:
                model['first_name'] = names[1].strip()
            else:
                model['first_name'] = ''

            player_list.append(model)

        # Sort list by last name
        player_list = sorted(player_list, key=lambda k: k['last_name'])

        return player_list

# Add player to counting dictionary
def add_player(players, name):
    if name in players:
        players[name] = players[name] + 1
    else:
        players[name] = 1

    return players