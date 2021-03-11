"""
The template of the main script of the machine learning process
"""

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False
        self.curr_x = 0
        self.curr_y = 0
        self.last_x = 0
        self.last_y = 0

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
            self.last_x = scene_info["ball"][0]
            self.last_y = scene_info["ball"][1]
            command = "SERVE_TO_RIGHT"
        else:
            self.curr_x = scene_info["ball"][0]
            self.curr_y = scene_info["ball"][1]
            predict_x = self.predict()
            if predict_x == -1:
                command = "NONE"
            elif predict_x > scene_info["platform"][0]:
                command = "MOVE_RIGHT"
            elif predict_x < scene_info["platform"][0]:
                command = "MOVE_LEFT"
            else:
                command = "NONE"
            self.last_x = self.curr_x
            self.last_y = self.curr_y
        print(command)
        return command

    def predict(self):
        # print(self.curr_y, self.last_y)
        if self.curr_y - self.last_y > 0:
            # dropping
            delta_x = self.curr_x - self.last_x
            delta_y = self.curr_y - self.last_y
            slope = delta_y / delta_x
            # print("down")
            return (400 - self.curr_y + slope * self.curr_x) / slope
        # print("up")
        return -1

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
