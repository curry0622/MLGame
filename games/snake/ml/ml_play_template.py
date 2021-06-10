"""
The template of the script for playing the game in the ml mode
"""

import os
import pickle

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.reach_bottom = False
        self.record = {
            "x": [],
            "y": [],
            # "p_x": [],
            # "p_y": [],
            "dir": [],
            "odd": [],
            "move": []
        }
        self.point = 0
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_OVER":
            self.reach_bottom = False
            self.point = 0
            return "RESET"

        # reset game
        if self.point >= 31:
            return "RIGHT"

        # set scene info
        self.scene_info = scene_info

        # set useful info
        self.head = scene_info["snake_head"]
        self.neck = scene_info["snake_body"][0]
        self.food = scene_info["food"]
        self.set_dir()
        self.set_move()
        self.set_predict()
        # print(self.head, self.move, (self.predict_x, self.predict_y))

        # record point
        if self.predict_x == self.scene_info["food"][0] and self.predict_y == self.scene_info["food"][1]:
            self.point += 1

        # record info
        self.record["x"].append(self.head[0])
        self.record["y"].append(self.head[1])
        # self.record["p_x"].append(self.predict_x)
        # self.record["p_y"].append(self.predict_y)
        self.record["dir"].append(self.dir)
        self.record["odd"].append(1 if self.head[0] % 20 == 0 else 0)
        self.record["move"].append(self.move)

        # dump pickle
        # if self.scene_info["frame"] == 10000:
        #     with open(os.path.join(os.path.dirname(__file__), "./pickles/test.pickle"), "wb") as f:
        #         pickle.dump(self.record, f)
        #         print("data collected")
        #         self.record = {
        #             "x": [],
        #             "y": [],
        #             # "p_x": [],
        #             # "p_y": [],
        #             "dir": [],
        #             "odd": [],
        #             "move": []
        #         }

        return self.move

    def reset(self):
        """
        Reset the status if needed
        """
        pass

    def set_dir(self):
        if self.head[0] == self.neck[0] and self.head[1] < self.neck[1]:
            self.dir = "UP"
        elif self.head[0] == self.neck[0] and self.head[1] > self.neck[1]:
            self.dir = "DOWN"
        elif self.head[1] == self.neck[1] and self.head[0] < self.neck[0]:
            self.dir = "LEFT"
        elif self.head[1] == self.neck[1] and self.head[0] > self.neck[0]:
            self.dir = "RIGHT"

    def set_move(self):
        if self.head[1] == 290 and self.head[0] == 290:
            self.move = "LEFT"
        # at bottom && not at leftmost
        elif self.head[1] == 290 and self.head[0] != 0:
            self.move = "LEFT"
        # at bottom && at leftmost
        elif self.head[1] == 290 and self.head[0] == 0:
            self.move = "UP"
        # at top && at leftmost
        elif self.head[1] == 0 and self.head[0] == 0:
            self.move = "RIGHT"
        # at top && x is at even column
        elif self.head[1] == 0 and self.head[0] % 20 != 0:
            self.move = "DOWN"
        # at top && x is at odd column
        elif self.head[1] == 0 and self.head[0] % 20 == 0:
            self.move = "RIGHT"
        # at bottom - 1 && at even column && not rightmost
        elif self.head[1] == 280 and self.head[0] % 20 != 0 and self.head[0] != 290:
            self.move = "RIGHT"
        # at bottom - 1 && at odd column
        elif self.head[1] == 280 and self.head[0] % 20 == 0:
            self.move = "UP"
        else:
            self.move = self.dir

    def set_predict(self):
        if self.move == "UP":
            self.predict_x = self.head[0]
            self.predict_y = self.head[1] - 10
        elif self.move == "DOWN":
            self.predict_x = self.head[0]
            self.predict_y = self.head[1] + 10
        elif self.move == "LEFT":
            self.predict_x = self.head[0] - 10
            self.predict_y = self.head[1]
        else:
            self.predict_x = self.head[0] + 10
            self.predict_y = self.head[1]
