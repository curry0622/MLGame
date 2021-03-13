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

            # update last position
            self.last_x = scene_info["ball"][0]
            self.last_y = scene_info["ball"][1]

            command = "NONE"
        else:
            # update current position
            self.curr_x = scene_info["ball"][0]
            self.curr_y = scene_info["ball"][1]

            predict = self.predict()
            print(predict, (scene_info["platform"][0] + 20))

            if predict == -1:
                command = "NONE"
            elif predict > scene_info["platform"][0] + 20:
                command = "MOVE_RIGHT"
            elif predict < scene_info["platform"][0] + 20:
                command = "MOVE_LEFT"
            else:
                command = "NONE"

            # update last position
            self.last_x = self.curr_x
            self.last_y = self.curr_y

        return command

    def predict(self):
        # upward
        if self.curr_y < self.last_y:
            result = self.curr_x - (399 - self.curr_y) * (self.last_x - self.curr_x) / (self.last_y - self.curr_y)
            return self.correct(result)

        # downward
        if self.curr_y > self.last_y:
            result = self.curr_x + (399 - self.curr_y) * (self.last_x - self.curr_x) / (self.curr_y - self.last_y)
            return self.correct(result)

        # default
        return -1

    def correct(self, result):
        # over left
        if result < 0:
            return self.correct(0 - result)

        # over right
        if result > 200:
            return self.correct(200 - (result - 200))

        return result

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
