# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
# from lib2to3.fixer_util import String
# from contextlib import nullcontext
# from http.client import responses

from flask import Flask, request, send_from_directory, jsonify
from game import Game

# Flask constructor takes the name of 
# current module (__name__) as argument.
counter_app = Flask(__name__)

api_endpoint_prefix = "/scb_counter_api/v1"
flutter_app_location = "flutter/v2"

#API ENDPOINTS
# /
# /[static_files]
# /game/<game_id>/
# /game/new?game_name=GAME&player_a_name=A&player_b_name=B
# /game/<game_id>/delete
# /game/<game_id>/add_point?set=0&player=0
# /game/<game_id>/remove_point?set=0&player=0
# /game/<game_id>/set_points?set=0&player=0&points=0
# /game/<game_id>/rename?game_name=GAME&player_a_name=A&player_b_name=B
# /games/
# /games/delete_all/

games = []
test_game = Game(0, "Test GAMEEE", "Lukas", "Tobias").generate_test_points()
test_game2 = Game(1, "Test GAME 2", "Lukas2", "Tobias2").generate_test_points()
test_game3 = Game(2, "Test GAMEEE 3", "Lukas3", "Tobias3").generate_test_points()
games.append(test_game)
games.append(test_game2)
games.append(test_game3)

last_game_id = len(games)-1 #counter for generating runtime-unique game ids


# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@counter_app.route('/')
# ‘/’ URL is bound with hello_world() function.
def serve_landing_page():
    # return 'Welcome to the SCB Game Point Counter Webservice!'
    return send_from_directory(flutter_app_location, "index.html")

@counter_app.route('/<path:path>')
def serve_static_flutter_files(path):
    return send_from_directory(flutter_app_location, path)

@counter_app.route(api_endpoint_prefix + '/game/<game_id>/')
def get_game_info(game_id):
    #cast parameter from str to int
    game_id = int(game_id)
    # set default value (no content), if game_id is not found
    response_body = {"err": "Invalid game_id."}
    #look for game with correct id in list
    for game in games:
        if game.game_id == game_id:
            response_body = game.info
            break
    response = jsonify(response_body)
    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@counter_app.route(api_endpoint_prefix + '/game/<game_id>/delete')
def delete_game(game_id):
    #cast parameter from str to int
    game_id = int(game_id)
    # set default value (no content), if game_id is not found
    response_body = {"err": "Invalid game_id."}
    #look for game with correct id in list
    for game in games:
        if game.game_id == game_id:
            #remove game from list
            games.remove(game)
            response_body = {"msg": "Game successfully deleted."}
            break
    response = jsonify(response_body)
    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@counter_app.route(api_endpoint_prefix + '/game/new', methods=['GET', 'POST'])
def create_new_game():
    # receive params for new game
    if request.method == 'GET':
        game_name = str(request.args.get('game_name'))
        player_a_name = str(request.args.get('player_a_name'))
        player_b_name = str(request.args.get('player_b_name'))
    elif request.method == 'POST':
        game_name = str(request.form.get('game_name'))
        player_a_name = str(request.form.get('player_a_name'))
        player_b_name = str(request.form.get('player_b_name'))
    #--> if method is something else flask will throw an error anyway (I think)
    else:
        game_name = ""
        player_a_name = ""
        player_b_name = ""
    # create and save new game (increase global counter for runtime-unique ids)
    global last_game_id
    last_game_id += 1
    new_game = Game(last_game_id, game_name, player_a_name, player_b_name)
    games.append(new_game)
    response = jsonify(new_game.info)
    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@counter_app.route(api_endpoint_prefix + '/game/<game_id>/add_point', methods=['GET', 'POST'])
def add_point(game_id):
    # cast parameter from str to int
    game_id = int(game_id)
    # receive params from request
    if request.method == 'GET':
        set = int(request.args.get('set'))
        player = int(request.args.get('player'))
    elif request.method == 'POST':
        set = int(request.form.get('set'))
        player = int(request.form.get('player'))
    # --> if method is something else flask will throw an error anyway (I think)
    else:
        set = 0
        player = 0
    response_body = {"err": "Invalid game_id."}
    # select correct game for point addition
    for game in games:
        if game.game_id == game_id:
            # add point
            game.add_point(set, player)
            # output game info (with updated values)
            response_body = game.info
            break
    response = jsonify(response_body)
    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@counter_app.route(api_endpoint_prefix + '/game/<game_id>/remove_point', methods=['GET', 'POST'])
def remove_point(game_id):
    # cast parameter from str to int
    game_id = int(game_id)
    #receive params from request
    if request.method == 'GET':
        set = int(request.args.get('set'))
        player = int(request.args.get('player'))
    elif request.method == 'POST':
        set = int(request.form.get('set'))
        player = int(request.form.get('player'))
    #--> if method is something else flask will throw an error anyway (I think)
    else:
        set = 0
        player = 0
    response_body = {"err": "Invalid game_id."}
    # select correct game for point removal
    for game in games:
        if game.game_id == game_id:
            # remove point
            game.remove_point(set, player)
            # output game info (with updated values)
            response_body = game.info
            break
    response = jsonify(response_body)
    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@counter_app.route(api_endpoint_prefix + '/game/<game_id>/set_points', methods=['GET', 'POST'])
def set_point(game_id):
    # cast parameter from str to int
    game_id = int(game_id)
    # receive params from request
    if request.method == 'GET':
        set = int(request.args.get('set'))
        player = int(request.args.get('player'))
        points = int(request.args.get('points'))
    elif request.method == 'POST':
        set = int(request.form.get('set'))
        player = int(request.form.get('player'))
        points = int(request.form.get('points'))
    # --> if method is something else flask will throw an error anyway (I think)
    else:
        set = 0
        player = 0
        points = 0
    response_body = {"err": "Invalid game_id."}
    # select correct game for points to set
    for game in games:
        if game.game_id == game_id:
            # add point
            game.set_point(set, player, points)
            # output game info (with updated values)
            response_body = game.info
            break
    response = jsonify(response_body)
    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@counter_app.route(api_endpoint_prefix + '/game/<game_id>/rename', methods=['GET', 'POST'])
def modify_game(game_id):
    # cast parameter from str to int
    game_id = int(game_id)
    # receive params for new game
    if request.method == 'GET':
        game_name = str(request.args.get('game_name'))
        player_a_name = str(request.args.get('player_a_name'))
        player_b_name = str(request.args.get('player_b_name'))
    elif request.method == 'POST':
        game_name = str(request.form.get('game_name'))
        player_a_name = str(request.form.get('player_a_name'))
        player_b_name = str(request.form.get('player_b_name'))
    # --> if method is something else flask will throw an error anyway (I think)
    else:
        game_name = ""
        player_a_name = ""
        player_b_name = ""
    response_body = {"err": "Invalid game_id."}
    #select correct game for modification
    for game in games:
        if game.game_id == game_id:
            #set new/ modified values
            game.game_name = game_name
            game.player_name_a = player_a_name
            game.player_name_b = player_b_name
            #output game info (with updated values)
            response_body = game.info
            break
    response = jsonify(response_body)
    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@counter_app.route(api_endpoint_prefix + '/games/')
def get_games():
    all_games_info = []
    for game in games:
        all_games_info.append(game.info)
    response = jsonify(all_games_info)
    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@counter_app.route(api_endpoint_prefix + '/games/delete_all')
def delete_all_games():
    #empty games list
    games.clear()
    # set info message to response body
    response_body = response_body = {"msg": "All games successfully deleted."}
    response = jsonify(response_body)
    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
