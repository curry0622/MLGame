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
            command = "SERVE_TO_LEFT"
        else:
            self.curr_x = scene_info["ball"][0]
            self.curr_y = scene_info["ball"][1]
            predict_x = self.predict()
            if predict_x == -1:
                command = "NONE"
            elif predict_x >= scene_info["platform"][0] + 20:
                command = "MOVE_RIGHT"
            elif predict_x <= scene_info["platform"][0] + 20:
                command = "MOVE_LEFT"
            else:
                command = "NONE"
            print("predict: ", predict_x, "platform: ", scene_info["platform"][0])
            self.last_x = self.curr_x
            self.last_y = self.curr_y
        print(command, scene_info["ball"])
        return command

    def predict(self):
        # print(self.curr_y, self.last_y)
        if self.curr_y - self.last_y > 0:
            # dropping
            # delta_x = self.curr_x - self.last_x
            # delta_y = self.curr_y - self.last_y
            # slope = abs(delta_y / delta_x)
            # result = (200 - self.curr_y + slope * self.curr_x) / slope
            result = ((self.curr_x - self.last_x) * (399 - self.curr_y)) / (self.curr_y - self.last_y) + self.curr_x
            # print("first predict: ", result)
            return self.correct(result)
        # print("up")
        return -1

    def correct(self, result):
        # print(result)
        if result >= 0 and result <= 200:
            return result
        elif result < 0:
            result = 0 - result
            return self.correct(result)
        elif result > 200:
            result = 200 - (result - 200)
            return self.correct(result)


    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
