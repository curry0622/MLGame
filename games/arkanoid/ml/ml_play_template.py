"""
The template of the main script of the machine learning process
"""

from pygame.mixer import pre_init


class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False
        self.scene_info = {}
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

            command = "SERVE_TO_RIGHT"
        else:
            # update current information
            self.scene_info = scene_info
            self.curr_x = scene_info["ball"][0]
            self.curr_y = scene_info["ball"][1]
            print("ball: ", scene_info["ball"])

            predict = self.predict()
            print("predict: ", predict)

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
            return self.correct(result, False)

        # downward
        if self.curr_y > self.last_y:
            # result = self.curr_x + (399 - self.curr_y) * (self.last_x - self.curr_x) / (self.curr_y - self.last_y)
            result = ((self.curr_x - self.last_x) * (399 - self.curr_y)) / (self.curr_y - self.last_y) + self.curr_x
            return self.correct(result, True)

        # default
        return -1

    def find_wall(self):
        # sort method
        def sort_by_first(elem):
            return elem[0]

        # sort bricks list
        bricks_list = self.scene_info["bricks"] + self.scene_info["hard_bricks"]

        # moving right
        if self.curr_x > self.last_x:
            bricks_list.sort(key=sort_by_first)
            for brick in bricks_list:
                if brick[0] >= self.curr_x:
                    collide_x = brick[0]
                    collide_y = (collide_x - self.curr_x) * (self.curr_y - self.last_y) / (self.curr_x - self.last_x) + self.curr_y
                    if brick[1] >= collide_y and brick[1] <= collide_y + 10:
                        print("right: ", collide_x)
                        return collide_x
                    # print("brick: ", brick, ", but collide range: ", collide_y, " ~ ", collide_y + 10)
            print("wall: ", 200)
            return 200

        # moving left
        if self.curr_x < self.last_x:
            bricks_list.sort(key=sort_by_first, reverse=True)
            for brick in bricks_list:
                if brick[0] + 25 <= self.curr_x:
                    collide_x = brick[0] + 25
                    collide_y = (collide_x - self.curr_x) * (self.curr_y - self.last_y) / (self.curr_x - self.last_x) + self.curr_y
                    if brick[1] >= collide_y and brick[1] <= collide_y + 10:
                        print("left: ", collide_x)
                        return collide_x
            print("wall: ", 0)
            return 0

    def correct(self, result, first_time):
        if first_time:
            # get wall value
            wall = self.find_wall()

            # moving right
            if self.curr_x > self.last_x:
                if result > wall:
                    result = wall - (result - wall)
                return self.correct(result, False)

            # moving left
            if self.curr_x < self.last_x:
                if result < wall:
                    result = wall + (wall - result)
                return self.correct(result, False)
        else:
            # over left boundary
            if result < 0:
                return self.correct(0 - result, False)

            # over right boundary
            if result > 200:
                return self.correct(200 - (result - 200), False)

            return result

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
