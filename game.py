from random import randint

class Game:

    def __init__(self, game_id, game_name ="Unnamed Game", player_name_a = "Player A", player_name_b="Player B"):
        self.game_id = game_id
        self.game_name = game_name
        self.player_name_a = player_name_a
        self.player_name_b = player_name_b
        self._points = [[0, 0], [0, 0], [0, 0]]

    #increase points of set (0 for first set, 1 for second, 2 for third set)
    # for selected team (0 means Player A, 1 means Player B)
    def add_point(self, set, player):
        #increase counter by 1 point
        self._points[set][player] = self._points[set][player] + 1

    def remove_point(self, set, player):
        # increase counter by 1 point
        self._points[set][player] = self._points[set][player] - 1

    def set_point(self, set, player, points):
        #increase counter by 1 point
        self._points[set][player] = points

    @property
    def info(self):
        game_info = {
            "game_id": self.game_id,
            "game_name": self.game_name,
            "player_a": self.player_name_a,
            "player_b": self.player_name_b,
            "points": self._points
        }
        return game_info

    def generate_test_points(self):
        for set_points in self._points:
            set_points[0] = randint(0, 21)
            set_points[1] = randint(0, 21)
        return self

    @property
    def points(self):
        return self._points


def row_object_to_game(row_object) -> Game:
    #read values from row object
    game_id = row_object['game_id']
    game_name = row_object['game_name']
    player_a = row_object['player_name_a']
    player_b = row_object['player_name_b']
    pts_a_1 = row_object['points_a_1']
    pts_a_2 = row_object['points_a_2']
    pts_a_3 = row_object['points_a_3']
    pts_b_1 = row_object['points_b_1']
    pts_b_2 = row_object['points_b_2']
    pts_b_3 = row_object['points_b_3']
    # create new game object
    new_game = Game(game_id, game_name, player_a, player_b)
    new_game._points = [[pts_a_1, pts_b_1], [pts_a_2, pts_b_2], [pts_a_3, pts_b_3]]
    # new_game.set_point(0, 0, pts_a_1)
    # new_game.set_point(1, 0, pts_a_2)
    # new_game.set_point(2, 0, pts_a_3)
    # new_game.set_point(0, 1, pts_b_1)
    # new_game.set_point(1, 1, pts_b_2)
    # new_game.set_point(2, 1, pts_b_3)
    return new_game