"""
The template of the script for the machine learning process in game pingpong
"""

"""
Some constants for calculations
"""
PLATFORM_WIDTH = 40
PLATFORM_HALF_WIDTH = 20
PLATFORM_HEIGHT = 30

BLOCKER_WIDTH = 30
BLOCKER_HALF_WIDTH = 15
BLOCKER_HEIGHT = 20

BALL_SIDE = 5
BALL_HALF_SIDE = 2.5

TREMBLE_WIDTH = 5

class MLPlay:
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = side

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        self.scene_info = scene_info
        if self.scene_info["status"] != "GAME_ALIVE":
            print(self.scene_info["ball_speed"])
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            return "SERVE_TO_LEFT"
        else:
            return self.motion()

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False

    def predict(self):
        """
        Predict ball position depends on side
        """
        if self.side == "1P":
            self.predict_x = 100 - BALL_HALF_SIDE
        else:
            self.predict_x = 100 - BALL_HALF_SIDE

    def motion(self):
        """
        Return motion for the platform
        """
        self.predict()
        curr_x = self.scene_info["platform_1P"][0] if self.side == "1P" else self.scene_info["platform_2P"][0]
        if abs(curr_x + PLATFORM_HALF_WIDTH - self.predict_x) < TREMBLE_WIDTH:
            return "NONE"
        if (curr_x + PLATFORM_HALF_WIDTH) < self.predict_x:
            return "MOVE_RIGHT"
        if (curr_x + PLATFORM_HALF_WIDTH) > self.predict_x:
            return "MOVE_LEFT"
