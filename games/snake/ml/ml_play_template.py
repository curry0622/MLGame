"""
The template of the script for playing the game in the ml mode
"""

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.reach_bottom = False
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_OVER":
            self.reach_bottom = False
            return "RESET"

        # set scene info
        self.scene_info = scene_info

        # set useful info
        self.head = scene_info["snake_head"]
        self.neck = scene_info["snake_body"][0]
        self.food = scene_info["food"]
        self.set_dir()
        self.set_move()

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
        else:
            print('head', self.head)
            print('neck', self.neck)
            print('all', self.scene_info["snake_body"])

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
