"""
The template of the main script of the machine learning process
"""
import os
import pickle

import numpy as np

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False
        self.scene_info = {}
        self.curr_x = 0
        self.curr_y = 0
        self.last_x = 0
        self.last_y = 0

        # Need scikit-learn==0.22.2
        with open(os.path.join(os.path.dirname(__file__), 'model.pickle'), 'rb') as f:
            self.model = pickle.load(f)

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
                scene_info["status"] == "GAME_PASS"):
            return "RESET"

        if not self.ball_served:
            self.ball_served = True

            # update last position
            self.last_x = scene_info["ball"][0]
            self.last_y = scene_info["ball"][1]

            command = "SERVE_TO_LEFT"
        else:
            # update current information
            self.scene_info = scene_info
            self.curr_x = scene_info["ball"][0]
            self.curr_y = scene_info["ball"][1]

            direction = 1
            # calculate direction
            if self.curr_x > self.last_x and self.curr_y > self.last_y:
                direction = 1
            elif self.curr_x < self.last_x and self.curr_y > self.last_y:
                direction = 2
            elif self.curr_x < self.last_x and self.curr_y < self.last_y:
                direction = 3
            else:
                direction = 4

            # predict position by rule
            predict_x = self.predict()

            # put features into x
            x = np.array([
                self.curr_x,
                self.curr_y,
                self.last_x,
                self.last_y,
                direction,
                scene_info["platform"][0],
                predict_x,
            ]).reshape((1, -1))

            # predict command by machine learning
            y = self.model.predict(x)

            if y == 0:
                command = "NONE"
            elif y == -1:
                command = "MOVE_LEFT"
            elif y == 1:
                command = "MOVE_RIGHT"

            # update last position
            self.last_x = self.curr_x
            self.last_y = self.curr_y

        return command

    def predict(self):
        # upward
        if self.curr_y < self.last_y:
            # ceiling doesn't exist
            if not self.find_ceiling():
                return 80

            # if ball is too high
            if self.curr_y <= 200:
                return 80

            # ceiling exists
            result = self.curr_x - (395 - self.curr_y) * (self.last_x - self.curr_x) / (self.last_y - self.curr_y)
            # right
            if self.curr_x > self.last_x:
                result = self.scene_info["platform"][0] + 36 if result <= self.scene_info["platform"][0] + 35 else result
            # left
            if self.curr_x < self.last_x:
                result = self.scene_info["platform"][0] - 1 if result <= self.scene_info["platform"][0]  else result
            return self.correct(result, False)

        # downward
        if self.curr_y > self.last_y:
            result = ((self.curr_x - self.last_x) * (395 - self.curr_y)) / (self.curr_y - self.last_y) + self.curr_x
            return self.correct(result, True)

        # default
        return -1

    def find_wall(self):
        # sort method
        def sort_by_first(elem):
            return elem[0]

        # sort bricks list
        bricks_list = self.scene_info["bricks"] + self.scene_info["hard_bricks"]

        # moving right
        if self.curr_x > self.last_x:
            bricks_list.sort(key=sort_by_first)
            for brick in bricks_list:
                if brick[0] >= self.curr_x + 5 and brick[1] >= self.curr_y + 5:
                    collide_x = brick[0] - 5
                    collide_y = (collide_x - self.curr_x) * (self.curr_y - self.last_y) / (self.curr_x - self.last_x) + self.curr_y
                    if collide_y >= brick[1] - 5 and collide_y < brick[1] + 10:
                        return collide_x
            return 195

        # moving left
        if self.curr_x < self.last_x:
            bricks_list.sort(key=sort_by_first, reverse=True)
            for brick in bricks_list:
                if brick[0] + 25 <= self.curr_x and brick[1] >= self.curr_y + 5:
                    collide_x = brick[0] + 25
                    collide_y = (collide_x - self.curr_x) * (self.curr_y - self.last_y) / (self.curr_x - self.last_x) + self.curr_y
                    if collide_y >= brick[1] - 5 and collide_y <= brick[1] + 10:
                        return collide_x
            return 0

    def find_ceiling(self):
        # sort method
        def sort_by_first(elem):
            return elem[0]

        # sort bricks list
        bricks_list = self.scene_info["bricks"] + self.scene_info["hard_bricks"]

        # flying right
        if self.curr_x > self.last_x:
            bricks_list.sort(key=sort_by_first)
            for brick in bricks_list:
                if brick[0] >= self.curr_x and brick[1] + 10 <= self.curr_y:
                    collide_y = brick[1] + 10
                    collide_x = (self.curr_x - self.last_x) * (self.curr_y - collide_y) / (self.last_y - self.curr_y) + self.curr_x
                    if collide_x >= brick[0] - 5 and collide_x < brick[0] + 25:
                        return True

        # flying left
        if self.curr_x < self.last_x:
            bricks_list.sort(key=sort_by_first, reverse=True)
            for brick in bricks_list:
                if brick[0] + 25 <= self.curr_x and brick[1] + 10 <= self.curr_y:
                    collide_y = brick[1] + 10
                    collide_x = (self.curr_x - self.last_x) * (self.curr_y - collide_y) / (self.last_y - self.curr_y) + self.curr_x
                    if collide_x >= brick[0] - 5 and collide_x < brick[0] + 25:
                        return True
        return False

    def correct(self, result, first_time):
        if first_time:
            # get wall value
            wall = self.find_wall()

            # moving right
            if self.curr_x > self.last_x:
                if result > wall:
                    result = wall - (result - wall)
                return self.correct(result, False)

            # moving left
            if self.curr_x < self.last_x:
                if result < wall:
                    result = wall + (wall - result)
                return self.correct(result, False)
        else:
            # over left boundary
            if result < 0:
                return self.correct(0 - result, False)

            # over right boundary
            if result > 195:
                return self.correct(195 - (result - 195), False)

            return result

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
