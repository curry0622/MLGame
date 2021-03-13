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
            command = "NONE"
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
            self.last_x = self.curr_x
            self.last_y = self.curr_y
        return command

    def predict(self):
        # dropping
        if self.curr_y - self.last_y > 0:
            result = ((self.curr_x - self.last_x) * (399 - self.curr_y)) / (self.curr_y - self.last_y) + self.curr_x
            return self.correct(result)
        # flying up
        if self.curr_x > self.last_x:
            return 150
        if self.curr_x < self.last_x:
            return 50
        return -1

    def correct(self, result):
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
