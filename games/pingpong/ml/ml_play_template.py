"""
The template of the script for the machine learning process in game pingpong
"""

"""
Some constants for calculations
"""
BALL_SIDE = 5
BALL_HALF_SIDE = 2.5

PLATFORM_WIDTH = 40
PLATFORM_HALF_WIDTH = 20
PLATFORM_HEIGHT = 30

BLOCKER_WIDTH = 30
BLOCKER_HALF_WIDTH = 15
BLOCKER_HEIGHT = 20
BLOCKER_HALF_HEIGHT = 10
BLOCKER_TOP_BOUND = 240 - BALL_SIDE
BLOCKER_BOTTOM_BOUND = 240 + BLOCKER_HEIGHT

TREMBLE_WIDTH = 5

GAME_WIDTH = 200
GAME_HALF_WIDTH = 100
GAME_HEIGHT = 500
GAME_HALF_HEIGHT = GAME_HEIGHT / 2
GAME_TOP_BOUND = 80
GAME_BOTTOM_BOUND = 420 - BALL_SIDE
GAME_RIGHT_BOUND = GAME_WIDTH - BALL_SIDE
GAME_LEFT_BOUND = 0

def point_slope_formula_return_x(point1, point2, y):
    """
    Calculate x for specific y on the line
    """
    if point1 == point2:
        return point2[1]
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]
    new_delta_y = y - point2[1]
    return delta_x * new_delta_y / delta_y + point2[0]

def point_slope_formula_return_y(point1, point2, x):
    """
    Calculate x for specific y on the line
    """
    if point1 == point2:
        return point2[0]
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]
    new_delta_x = x - point2[0]
    return delta_y * new_delta_x / delta_x + point2[1]

def correction(last_pos, new_pos, target_y):
    """
    Correction of ball's predict position
    """
    x = point_slope_formula_return_x(last_pos, new_pos, target_y)
    if x < 0:
        collide_y = point_slope_formula_return_y(last_pos, new_pos, GAME_LEFT_BOUND)
        delta_y = collide_y - last_pos[1]
        x = correction((GAME_LEFT_BOUND, collide_y), (last_pos[0], last_pos[1] + 2 * delta_y), target_y)
    elif x > GAME_WIDTH - BALL_SIDE:
        collide_y = point_slope_formula_return_y(last_pos, new_pos, GAME_RIGHT_BOUND)
        delta_y = collide_y - last_pos[1]
        x = correction((GAME_RIGHT_BOUND, collide_y), (last_pos[0], last_pos[1] + 2 * delta_y), target_y)
    return x


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
        if self.last_ball == self.scene_info["ball"]:
            self.predict_ball_x = GAME_HALF_WIDTH - BALL_HALF_SIDE
            return

        self.set_ball_dir()

        # 1P is at the bottom
        if self.side == "1P":
            # if ball is flying up, reset predict_ball_x of 1P to the middle
            if self.ball_dir == 3 or self.ball_dir == 4:
                if self.scene_info["ball"][1] > BLOCKER_BOTTOM_BOUND:
                    collide_x = correction(self.last_ball, self.scene_info["ball"], BLOCKER_BOTTOM_BOUND)
                    delta_x = collide_x - self.scene_info["ball"][0]
                    self.predict_ball_x = correction((collide_x, BLOCKER_BOTTOM_BOUND), (self.scene_info["ball"][0] + 2 * delta_x, self.scene_info["ball"][1]), GAME_BOTTOM_BOUND)
                else:
                    self.predict_ball_x = GAME_HALF_WIDTH - BALL_HALF_SIDE
            # if ball is flying down but it's above middle, first detect whether it'll collide with blocker's side or not
            else:
                self.predict_ball_x = correction(self.last_ball, self.scene_info["ball"], GAME_BOTTOM_BOUND)
        # 2P is at the top
        else:
            # if ball is flying down, reset predict_ball_x of 2P to the middle
            if self.ball_dir == 1 or self.ball_dir == 2:
                if self.scene_info["ball"][1] < BLOCKER_TOP_BOUND:
                    collide_x = correction(self.last_ball, self.scene_info["ball"], BLOCKER_TOP_BOUND)
                    delta_x = collide_x - self.scene_info["ball"][0]
                    self.predict_ball_x = correction((collide_x, BLOCKER_TOP_BOUND), (self.scene_info["ball"][0] + 2 * delta_x, self.scene_info["ball"][1]), BLOCKER_TOP_BOUND)
                self.predict_ball_x = GAME_HALF_WIDTH - BALL_HALF_SIDE
            else:
                self.predict_ball_x = correction(self.last_ball, self.scene_info["ball"], GAME_TOP_BOUND)

        # update last ball position
        self.last_ball = self.scene_info["ball"]

    def motion(self):
        """
        Return motion for the platform
        """
        # if the ball is already out of top bottom bound, it means gameover
        if self.scene_info["ball"][1] < GAME_TOP_BOUND or self.scene_info["ball"][1] > GAME_BOTTOM_BOUND:
            return "NONE"

        self.predict()
        curr_x = self.scene_info["platform_1P"][0] if self.side == "1P" else self.scene_info["platform_2P"][0]
        if abs(curr_x + PLATFORM_HALF_WIDTH - self.predict_ball_x) < TREMBLE_WIDTH:
            return "NONE"
        if (curr_x + PLATFORM_HALF_WIDTH) < self.predict_ball_x:
            return "MOVE_RIGHT"
        if (curr_x + PLATFORM_HALF_WIDTH) > self.predict_ball_x:
            return "MOVE_LEFT"
