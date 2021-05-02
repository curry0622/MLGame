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

            # get first blocker position
            self.last_blocker = self.scene_info["blocker"]

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

    def will_collide_with_blocker(self):
        """
        Detect whether the ball will collide with blocker or not
        """
        ERROR_DISTANCE = 2 * abs(self.scene_info["ball_speed"][0])
        collide_x = correction(self.last_ball, self.scene_info["ball"], GAME_HALF_HEIGHT)
        delta_frame = abs((GAME_HALF_HEIGHT - self.scene_info["ball"][1]) / self.scene_info["ball_speed"][1])
        displacement = 5 * delta_frame
        # print("collide_x", collide_x)
        # blocker is currently moving right
        if self.scene_info["blocker"][0] - self.last_blocker[0] > 0:
            new_blocker_x = self.scene_info["blocker"][0] + displacement
            if new_blocker_x > (GAME_WIDTH - BLOCKER_WIDTH):
                new_blocker_x = (GAME_WIDTH - BLOCKER_WIDTH) - (new_blocker_x - (GAME_WIDTH - BLOCKER_WIDTH))
            # print("new_blocker_x", new_blocker_x, "new_blocker_right_bound", new_blocker_x + BLOCKER_WIDTH)
            if collide_x > new_blocker_x - ERROR_DISTANCE and collide_x < new_blocker_x + BLOCKER_WIDTH + ERROR_DISTANCE:
                # print("collide range", (new_blocker_x - ERROR_DISTANCE, new_blocker_x + BLOCKER_WIDTH + ERROR_DISTANCE), "collide_x", collide_x)
                # print("current ball", self.scene_info["ball"])
                # print("will collide")
                return True
            # else:
                # print("collide range", (new_blocker_x - ERROR_DISTANCE, new_blocker_x + BLOCKER_WIDTH + ERROR_DISTANCE), "collide_x", collide_x)
                # print("current ball", self.scene_info["ball"])
        # blocker is currently moving left
        elif self.scene_info["blocker"][0] - self.last_blocker[0] < 0:
            new_blocker_x = self.scene_info["blocker"][0] - displacement
            if new_blocker_x < 0:
                new_blocker_x = 0 - new_blocker_x
            # print("new_blocker_x", new_blocker_x, "new_blocker_right_bound", new_blocker_x + BLOCKER_WIDTH)
            if collide_x > new_blocker_x - ERROR_DISTANCE and collide_x < new_blocker_x + BLOCKER_WIDTH + ERROR_DISTANCE:
                # print("collide range", (new_blocker_x - ERROR_DISTANCE, new_blocker_x + BLOCKER_WIDTH + ERROR_DISTANCE), "collide_x", collide_x)
                # print("current ball", self.scene_info["ball"])
                # print("will collide")
                return True
            # else:
            #     print("collide range", (new_blocker_x - ERROR_DISTANCE, new_blocker_x + BLOCKER_WIDTH + ERROR_DISTANCE), "collide_x", collide_x)
            #     print("current ball", self.scene_info["ball"])
        # print("won't collide")
        return False

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
            # if ball is flying up
            if self.ball_dir == 3 or self.ball_dir == 4:
                # if ball is below middle, pretend it'll collide with blocker's bottom
                if self.scene_info["ball"][1] > BLOCKER_BOTTOM_BOUND:
                    without_correction_x = point_slope_formula_return_x(self.last_ball, self.scene_info["ball"], BLOCKER_BOTTOM_BOUND)
                    collide_x = correction(self.last_ball, self.scene_info["ball"], BLOCKER_BOTTOM_BOUND)
                    delta_x = collide_x - self.scene_info["ball"][0]
                    self.predict_ball_x = correction((collide_x, BLOCKER_BOTTOM_BOUND), (self.scene_info["ball"][0] + 2 * delta_x, self.scene_info["ball"][1]), GAME_BOTTOM_BOUND)

                    # if ball is flying to left top and will out of left bound, correct predict_x
                    if self.ball_dir == 3 and without_correction_x < GAME_LEFT_BOUND:
                        collide_left_bound_y = point_slope_formula_return_y(self.last_ball, self.scene_info["ball"], GAME_LEFT_BOUND)
                        delta_x = collide_x - GAME_LEFT_BOUND
                        self.predict_ball_x = correction((collide_x, BLOCKER_BOTTOM_BOUND), (GAME_LEFT_BOUND + 2 * delta_x, collide_left_bound_y), GAME_BOTTOM_BOUND)

                    # if ball is flying to right top and will out of right bound, correct predict_x
                    if self.ball_dir == 4 and without_correction_x > GAME_RIGHT_BOUND:
                        collide_right_bound_y = point_slope_formula_return_y(self.last_ball, self.scene_info["ball"], GAME_RIGHT_BOUND)
                        delta_x = collide_x - GAME_RIGHT_BOUND
                        self.predict_ball_x = correction((collide_x, BLOCKER_BOTTOM_BOUND), (GAME_RIGHT_BOUND + 2 * delta_x, collide_right_bound_y), GAME_BOTTOM_BOUND)
                    # print(self.predict_ball_x)

                # if ball is above middle, reset it to middle
                else:
                    self.predict_ball_x = GAME_HALF_WIDTH - BALL_HALF_SIDE
            # if ball is flying down
            else:
                self.predict_ball_x = correction(self.last_ball, self.scene_info["ball"], GAME_BOTTOM_BOUND)

                # if ball is above middle
                if self.scene_info["ball"][1] < GAME_HALF_HEIGHT and self.will_collide_with_blocker():
                    without_correction_x = point_slope_formula_return_x(self.last_ball, self.scene_info["ball"], GAME_BOTTOM_BOUND)
                    collide_x = correction(self.last_ball, self.scene_info["ball"], GAME_HALF_HEIGHT)
                    delta_x = collide_x - self.predict_ball_x
                    self.predict_ball_x = correction((collide_x, GAME_HALF_HEIGHT), (self.predict_ball_x + 2 * delta_x, GAME_BOTTOM_BOUND), GAME_BOTTOM_BOUND)

                    # if ball is flying to left bottom and will out of left bound, correct predict_ball_x
                    if self.ball_dir == 2 and without_correction_x < GAME_LEFT_BOUND:
                        collide_left_bound_y = point_slope_formula_return_y(self.last_ball, self.scene_info["ball"], GAME_LEFT_BOUND)
                        delta_x = collide_x - GAME_LEFT_BOUND
                        self.predict_ball_x = correction((collide_x, GAME_HALF_HEIGHT), (GAME_LEFT_BOUND + 2 * delta_x, collide_left_bound_y), GAME_BOTTOM_BOUND)

                    # if ball is flying to right bottom and will out of right bound, correct predict_x
                    if self.ball_dir == 1 and without_correction_x > GAME_RIGHT_BOUND:
                        collide_right_bound_y = point_slope_formula_return_y(self.last_ball, self.scene_info["ball"], GAME_RIGHT_BOUND)
                        delta_x = collide_x - GAME_RIGHT_BOUND
                        self.predict_ball_x = correction((collide_x, GAME_HALF_HEIGHT), (GAME_RIGHT_BOUND + 2 * delta_x, collide_right_bound_y), GAME_BOTTOM_BOUND)
                    # print(self.predict_ball_x)

        # 2P is at the top
        else:
            # if ball is flying down
            if self.ball_dir == 1 or self.ball_dir == 2:
                # if ball is above middle, pretend it'll collide with blocker's top
                if self.scene_info["ball"][1] < BLOCKER_TOP_BOUND:
                    without_correction_x = point_slope_formula_return_x(self.last_ball, self.scene_info["ball"], BLOCKER_TOP_BOUND)
                    collide_x = correction(self.last_ball, self.scene_info["ball"], BLOCKER_TOP_BOUND)
                    delta_x = collide_x - self.scene_info["ball"][0]
                    self.predict_ball_x = correction((collide_x, BLOCKER_TOP_BOUND), (self.scene_info["ball"][0] + 2 * delta_x, self.scene_info["ball"][1]), GAME_TOP_BOUND)

                    # if ball is flying to left bottom and will out of left bound, correct predict_x
                    if self.ball_dir == 2 and without_correction_x < GAME_LEFT_BOUND:
                        collide_left_bound_y = point_slope_formula_return_y(self.last_ball, self.scene_info["ball"], GAME_LEFT_BOUND)
                        delta_x = collide_x - GAME_LEFT_BOUND
                        self.predict_ball_x = correction((collide_x, BLOCKER_TOP_BOUND), (GAME_LEFT_BOUND + 2 * delta_x, collide_left_bound_y), GAME_TOP_BOUND)

                    # if ball is flying to right bottom and will out of right bound, correct predict_x
                    if self.ball_dir == 1 and without_correction_x > GAME_RIGHT_BOUND:
                        collide_right_bound_y = point_slope_formula_return_y(self.last_ball, self.scene_info["ball"], GAME_RIGHT_BOUND)
                        delta_x = collide_x - GAME_RIGHT_BOUND
                        self.predict_ball_x = correction((collide_x, BLOCKER_TOP_BOUND), (GAME_RIGHT_BOUND + 2 * delta_x, collide_right_bound_y), GAME_TOP_BOUND)
                    # print(self.predict_ball_x)
                self.predict_ball_x = GAME_HALF_WIDTH - BALL_HALF_SIDE
            # if ball is flying up
            else:
                self.predict_ball_x = correction(self.last_ball, self.scene_info["ball"], GAME_TOP_BOUND)
                # print("correct prediction", self.predict_ball_x)
                # if ball is below middle
                if self.scene_info["ball"][1] > GAME_HALF_HEIGHT and self.will_collide_with_blocker():
                    without_correction_x = point_slope_formula_return_x(self.last_ball, self.scene_info["ball"], GAME_TOP_BOUND)
                    collide_x = correction(self.last_ball, self.scene_info["ball"], GAME_HALF_HEIGHT)
                    delta_x = collide_x - self.predict_ball_x
                    self.predict_ball_x = correction((collide_x, GAME_HALF_HEIGHT), (self.predict_ball_x + 2 * delta_x, GAME_TOP_BOUND), GAME_TOP_BOUND)

                    # if ball is flying to left top and will out of left bound, correct predict_x
                    if self.ball_dir == 3 and without_correction_x < GAME_LEFT_BOUND:
                        collide_left_bound_y = point_slope_formula_return_y(self.last_ball, self.scene_info["ball"], GAME_LEFT_BOUND)
                        delta_x = collide_x - GAME_LEFT_BOUND
                        self.predict_ball_x = correction((collide_x, GAME_HALF_HEIGHT), (GAME_LEFT_BOUND + 2 * delta_x, collide_left_bound_y), GAME_TOP_BOUND)

                    # if ball is flying to right top and will out of right bound, correct predict_x
                    if self.ball_dir == 4 and without_correction_x > GAME_RIGHT_BOUND:
                        collide_right_bound_y = point_slope_formula_return_y(self.last_ball, self.scene_info["ball"], GAME_RIGHT_BOUND)
                        delta_x = collide_x - GAME_RIGHT_BOUND
                        self.predict_ball_x = correction((collide_x, GAME_HALF_HEIGHT), (GAME_RIGHT_BOUND + 2 * delta_x, collide_right_bound_y), GAME_TOP_BOUND)

        # update last ball position
        self.last_ball = self.scene_info["ball"]

        # update last blocker position
        self.last_blocker = self.scene_info["blocker"]

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
