# ChessPi

Built by @edmundlam and @prateeksan

ChessPi is simple RESTful API for chess applications built with Flask-Restful. 

Features include:

* Endpoints to query games and players
* Endpoints to add new games and players
* Parsers to import pgn files into the database

## Endpoints

**/games**

```
/games                  # List of all games in the DB
/games/16               # Show game with id 16
/games/16?format=pgn    # Show game with id 16 in pgn format
/games?name=chandler    # Filter games played by Chandler
/games?eco=b22          # Filter games opening with ECO B22
```

**/players**

```
/players                # List of all players in DB
/players/1              # List player with id=1
/players?name=chandler  # List players with name=chandler
```

**/eco_codes**

```
/eco_codes    # List of all eco codes in DB
```

## Technology stack

* Python 3.5
* Flask
* Flask-Restful
* pgnparser
* SQLite

## Status

Under construction

## Demo

Link to demo version here

## Dependencies

See requirements.txt

## Installation

1. Run `pip install -r requirements.txt`
2. Run `python db_create`
3. Run `python db_migrate`
4. Launch the server `python runserver.py`

## Credits and references

1. [lichess](https://github.com/ornicar/lila)
2.
3.

## Testing

Run the following commands from ChessPi root:

+ `$ python tests/game_parser_tests.py`
+ `$ python tests/model_tests.py`

All tests should pass.

## License

The MIT License (MIT)
Copyright (c) 2016 Edmund Lam & Prateek Sanyal

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
