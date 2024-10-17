import json
import sqlite3

from Tools.scripts.win_add2path import modify
from flask import g

from game import Game, row_object_to_game

DATABASE = 'persistence/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    # print("get_db() called.")
    return db

# @app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        # print("DB closed.")

def init_db(app):
    with app.app_context():
        db = get_db()
        with app.open_resource('persistence/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def insert_testdata(app):
    with app.app_context():
        db = get_db()
        with app.open_resource('persistence/testdata.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def register_db_teardown(app):
    app.teardown_appcontext(close_connection)

#Helper Function for easier querying #see https://flask.palletsprojects.com/en/3.0.x/patterns/sqlite3/
def query_db(query, args=(), one=False, modify=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    if modify: db.commit()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def update_game_single_column(game_id, column, value):
    return query_db("UPDATE games "
             "SET " + str(column) + " = ? "
             "WHERE game_id = ?",
             [value, game_id],
             modify=True)

def update_game(game_id, columns: (), values: ()):
    # prepare query string for setting the columns
    set_columns_string = ""
    for column in columns:
        set_columns_string = set_columns_string + str(column) + " = ?, "
    # remove last to characters from string ", "
    set_columns_string = set_columns_string[:-2]
    #prepare args list for query (import all values for columns and add game_id as last argument)
    args = []
    for value in values:
        args.append(value)
    args.append(game_id)
    return query_db("UPDATE games "
             "SET " + set_columns_string + ""
             "WHERE game_id = ?",
             args,
             modify=True)

def add_point(game_id : int, set : int, player : int):
    # find correct column to set new value
    if set == 0 and player == 0: set_column = "points_a_1"
    elif set == 1 and player == 0: set_column = "points_a_2"
    elif set == 2 and player == 0: set_column = "points_a_3"
    elif set == 0 and player == 1: set_column = "points_b_1"
    elif set == 1 and player == 1: set_column = "points_b_2"
    elif set == 2 and player == 1: set_column = "points_b_3"
    else:
        return #wrong params, abort function
    return query_db("UPDATE games "
             "SET " + set_column + " = " + set_column + " + 1 "
             "WHERE game_id = ?",
             [game_id],
             modify=True)

def remove_point(game_id, set : int, player : int):
    # find correct column to set new value
    if set == 0 and player == 0: set_column = "points_a_1"
    elif set == 1 and player == 0: set_column = "points_a_2"
    elif set == 2 and player == 0: set_column = "points_a_3"
    elif set == 0 and player == 1: set_column = "points_b_1"
    elif set == 1 and player == 1: set_column = "points_b_2"
    elif set == 2 and player == 1: set_column = "points_b_3"
    else:
        return #wrong params, abort function
    return query_db("UPDATE games "
             "SET " + set_column + " = " + set_column + " - 1 "
             "WHERE game_id = ?",
             [game_id],
             modify=True)

def print_all_games_from_db(app):
    with app.app_context():
        for game in query_db('SELECT * FROM games'):
            # print(game['game_name'], 'has the player A', game['player_name_a'])
            # print(json.dumps(a, indent=4))
            # print(dict(game))
            print(row_object_to_game(game).info)

def get_games():
    return query_db('SELECT * FROM games')

def get_game(game_id : int):
    return query_db('SELECT * FROM games WHERE game_id = ?', str(game_id), one=True)

def add_game(game : Game):
    #add game to db (note that game_id from game_id is irrelevant; id will be given by db)
    return query_db("INSERT INTO games (game_name, player_name_a, player_name_b, points_a_1, points_a_2, points_a_3, points_b_1, points_b_2, points_b_3)"
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
                    [game.game_name, game.player_name_a, game.player_name_b, game.points[0][0], game.points[1][0], game.points[2][0], game.points[0][1], game.points[1][1], game.points[2][1] ],
                    modify=True)

def delete_game(game_id : int):
    return query_db('DELETE FROM games WHERE game_id = ?', str(game_id), modify=True)
