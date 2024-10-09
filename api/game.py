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
