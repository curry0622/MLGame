"""
The template of the script for the machine learning process in game pingpong
"""

"""
Some constants for calculations
"""
GAME_WIDTH = 200
GAME_HALF_WIDTH = 100

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

            # get first ball position
            self.last_ball = self.scene_info["ball"]

            return "SERVE_TO_LEFT"
        else:
            return self.motion()

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False

    def set_ball_dir(self):
        """
        Calculate and set direction of ball (1, 2, 3, 4 stands for coordinate system quadrant)
        """
        x = self.scene_info["ball"][0] - self.last_ball[0]
        y = self.scene_info["ball"][1] - self.last_ball[1]
        if x > 0 and y > 0:
            self.ball_dir = 1
        elif x < 0 and y > 0:
            self.ball_dir = 2
        elif x < 0 and y < 0:
            self.ball_dir = 3
        elif x > 0 and y < 0:
            self.ball_dir = 4
        else:
            self.ball_dir = 0

    def predict(self):
        """
        Predict ball position depends on side
        """
        self.set_ball_dir()

        # 1P is at the bottom
        if self.side == "1P":
            # if ball is flying up, reset predict_x of 1P to the middle
            if self.ball_dir == 3 or self.ball_dir == 4:
                self.predict_x = GAME_HALF_WIDTH - BALL_HALF_SIDE
            else:
                self.predict_x = self.scene_info["ball"][0]
        # 2P is at the top
        else:
            # if ball is flying down, reset predict_x of 2P to the middle
            if self.ball_dir == 1 or self.ball_dir == 2:
                self.predict_x = GAME_HALF_WIDTH - BALL_HALF_SIDE
            else:
                self.predict_x = self.scene_info["ball"][0]

        # update last ball position
        self.last_ball = self.scene_info["ball"]

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
