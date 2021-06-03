"""
The template of the script for playing the game in the ml mode
"""

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_OVER":
            return "RESET"

        # set scene info
        self.scene_info = scene_info

        # set useful info
        self.head = scene_info["snake_head"]
        self.neck = scene_info["snake_body"][1]
        self.food = scene_info["food"]
        self.set_dir()

        return self.dir
        # if snake_head[0] > food[0]:
        #     return "LEFT"
        # elif snake_head[0] < food[0]:
        #     return "RIGHT"
        # elif snake_head[1] > food[1]:
        #     return "UP"
        # elif snake_head[1] < food[1]:
        #     return "DOWN"

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
        self.dir = "RIGHT"
