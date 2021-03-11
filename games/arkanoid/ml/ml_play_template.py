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
        self.last_x = 0

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
            command = "SERVE_TO_LEFT"
            self.last_x = scene_info["ball"][0]
        else:
            self.curr_x = scene_info["ball"][0]
            if self.curr_x - self.last_x > 0:
                command = "MOVE_RIGHT"
            elif self.curr_x - self.last_x < 0:
                command = "MOVE_LEFT"
            else:
                command = "NONE"
            self.last_x = scene_info["ball"][0]
        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
