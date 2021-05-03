"""
The template of the script for the machine learning process in game pingpong
"""
"""
ml_play 程式只能交一份，且檔名為 ml_play.py
"""

class MLPlay:
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = side

        """
        load your "1P" and "2P" model here
        可以是一個檔案或是兩個檔案，但相對路徑要放好 (路徑請用相對路徑，並放在相同目錄底下)

        sample 1: (如果 "1P", "2P" 是分開 train)
        self.model_1 = 1P pickle
        self.model_2 = 2P pickle

        sample 2: (如果 "1P", "2P" train 成一個 model)
        self.model = "1P" and "2P" pickle
        """

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        """
        如果是兩個 model 可以在程式中用 side 去判斷要用哪個 model

        sample 1: (如果 "1P", "2P" 是分開 train)
        if self.side == "1P":
            # 使用 model 1 預測
        else:
            # 使用 model 2 預測

        sample 2: (如果 "1P", "2P" train 成一個 model)
        # 直接使用 model 預測
        """

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
