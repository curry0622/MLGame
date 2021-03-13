"""
The template of the main script of the machine learning process
"""

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
            self.last_x = scene_info["ball"][0]
            self.last_y = scene_info["ball"][1]
            command = "SERVE_TO_LEFT"
        else:
            self.scene_info = scene_info
            self.curr_x = scene_info["ball"][0]
            self.curr_y = scene_info["ball"][1]
            predict_x = self.predict()
            print(predict_x)
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
        # return (self.scene_info["platform"][0] + self.curr_x) / 2 if self.curr_y >= 320 else -1
        # if self.curr_x > self.last_x and self.curr_y >= 300:
        #     return 150
        # if self.curr_x < self.last_x and self.curr_y >= 300:
        #     return 50
        if self.curr_y - self.last_y < 0:
            return self.upward_predict()
        return -1

    def correct(self, result):
        # if result >= 0 and result <= 200:
        #     return result
        # elif result < 0:
        #     result = 0 - result
        #     return self.correct(result)
        # elif result > 200:
        #     result = 200 - (result - 200)
        #     return self.correct(result)
        wall = self.find_wall()
        # print(wall)
        if self.curr_x > self.last_x:
            if result > wall:
                result = wall - (result - wall)
                return result if result < 200 else 200 - (result - 200)
            return result
        if self.curr_x < self.last_x:
            if result < wall:
                result = wall + (wall - result)
                return result if result > 0 else 0 - result
            return result

    def find_wall(self):
        # only for dropping
        # case 1: drop to right
        if self.curr_x > self.last_x:
            for blk in self.scene_info["bricks"]:
                if blk[0] > self.curr_x:
                    collide_x = blk[0]
                    collide_y = (collide_x - self.curr_x) * (self.curr_y - self.last_y) / (self.curr_x - self.last_x) + self.curr_y
                    if blk[1] >= collide_y and blk[1] <= collide_y + 10:
                        # print(blk)
                        return blk[0]
            return 200
        # case 2: drop to left
        if self.curr_x < self.last_x:
            for blk in self.scene_info["bricks"]:
                if blk[0] < self.curr_x:
                    collide_x = blk[0] + 25
                    collide_y = (collide_x - self.curr_x) * (self.curr_y - self.last_y) / (self.curr_x - self.last_x) + self.curr_y
                    if blk[1] >= collide_y and blk[1] <= collide_y + 10:
                        # print(blk)
                        return blk[0]
            return 0

    def upward_predict(self):
        result = self.curr_x - (399 - self.curr_y) * (self.last_x - self.curr_x) / (self.last_y - self.curr_y)
        return self.correct(result)

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
