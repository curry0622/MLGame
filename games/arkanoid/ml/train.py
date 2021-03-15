import os
import pickle
import numpy as np

def predict(curr_x, curr_y, last_x, last_y, platform_x, bricks_list):
    # upward
        if curr_y < last_y:
            # ceiling doesn't exist
            if not find_ceiling(curr_x, curr_y, last_x, last_y, bricks_list):
                return 80

            # if ball is too high
            if curr_y <= 200:
                return 80

            # ceiling exists
            result = curr_x - (395 - curr_y) * (last_x - curr_x) / (last_y - curr_y)
            # right
            if curr_x > last_x:
                result = platform_x + 36 if result <= platform_x + 35 else result
            # left
            if curr_x < last_x:
                result = platform_x - 1 if result <= platform_x  else result
            return correct(result, False, curr_x, curr_y, last_x, last_y, bricks_list)

        # downward
        if curr_y > last_y:
            result = ((curr_x - last_x) * (395 - curr_y)) / (curr_y - last_y) + curr_x
            return correct(result, True, curr_x, curr_y, last_x, last_y, bricks_list)

        # default
        return -1

def find_wall(curr_x, curr_y, last_x, last_y, bricks_list):
    # sort method
    def sort_by_first(elem):
        return elem[0]

    # moving right
    if curr_x > last_x:
        bricks_list.sort(key=sort_by_first)
        for brick in bricks_list:
            if brick[0] >= curr_x + 5 and brick[1] >= curr_y + 5:
                collide_x = brick[0] - 5
                collide_y = (collide_x - curr_x) * (curr_y - last_y) / (curr_x - last_x) + curr_y
                if collide_y >= brick[1] - 5 and collide_y < brick[1] + 10:
                    return collide_x
        return 195

    # moving left
    if curr_x < last_x:
        bricks_list.sort(key=sort_by_first, reverse=True)
        for brick in bricks_list:
            if brick[0] + 25 <= curr_x and brick[1] >= curr_y + 5:
                collide_x = brick[0] + 25
                collide_y = (collide_x - curr_x) * (curr_y - last_y) / (curr_x - last_x) + curr_y
                if collide_y >= brick[1] - 5 and collide_y <= brick[1] + 10:
                    return collide_x
        return 0

def find_ceiling(curr_x, curr_y, last_x, last_y, bricks_list):
    # sort method
    def sort_by_first(elem):
        return elem[0]

    # flying right
    if curr_x > last_x:
        bricks_list.sort(key=sort_by_first)
        for brick in bricks_list:
            if brick[0] >= curr_x and brick[1] + 10 <= curr_y:
                collide_y = brick[1] + 10
                collide_x = (curr_x - last_x) * (curr_y - collide_y) / (last_y - curr_y) + curr_x
                if collide_x >= brick[0] - 5 and collide_x < brick[0] + 25:
                    return True

    # flying left
    if curr_x < last_x:
        bricks_list.sort(key=sort_by_first, reverse=True)
        for brick in bricks_list:
            if brick[0] + 25 <= curr_x and brick[1] + 10 <= curr_y:
                collide_y = brick[1] + 10
                collide_x = (curr_x - last_x) * (curr_y - collide_y) / (last_y - curr_y) + curr_x
                if collide_x >= brick[0] - 5 and collide_x < brick[0] + 25:
                    return True
    return False

def correct(result, first_time, curr_x, curr_y, last_x, last_y, bricks_list):
    if first_time:
        # get wall value
        wall = find_wall(curr_x, curr_y, last_x, last_y, bricks_list)

        # moving right
        if curr_x > last_x:
            if result > wall:
                result = wall - (result - wall)
            return correct(result, False, curr_x, curr_y, last_x, last_y, bricks_list)

        # moving left
        if curr_x < last_x:
            if result < wall:
                result = wall + (wall - result)
            return correct(result, False, curr_x, curr_y, last_x, last_y, bricks_list)
    else:
        # over left boundary
        if result < 0:
            return correct(0 - result, False, curr_x, curr_y, last_x, last_y, bricks_list)

        # over right boundary
        if result > 195:
            return correct(195 - (result - 195), False, curr_x, curr_y, last_x, last_y, bricks_list)

        return result

if __name__ == "__main__":
    scene_info = []
    command = []

    for i in range(1, 21):
        with open(os.path.join(os.path.dirname(__file__), './models/model' + str(i) + '.pickle'), 'rb') as f:
            data = pickle.load(f)
            scene_info = scene_info + data['ml']['scene_info']
            command = command + data['ml']['command']

    curr_x = []
    curr_y = []
    last_x = []
    last_y = []
    direction = []
    platform_x = []
    predict_x = []
    command_num = []

    for i in range(1, len(scene_info) - 1):
        # info
        last_info = scene_info[i - 1]
        curr_info = scene_info[i]

        # append current and last ball position
        last_x.append(last_info['ball'][0])
        last_y.append(last_info['ball'][1])
        curr_x.append(curr_info['ball'][0])
        curr_y.append(curr_info['ball'][1])

        # append direction
        if curr_info['ball'][0] > last_info['ball'][0] and curr_info['ball'][1] > last_info['ball'][1]:
            # (+, +)
            direction.append(1)
        if curr_info['ball'][0] < last_info['ball'][0] and curr_info['ball'][1] > last_info['ball'][1]:
            # (-, +)
            direction.append(2)
        if curr_info['ball'][0] < last_info['ball'][0] and curr_info['ball'][1] < last_info['ball'][1]:
            # (-, -)
            direction.append(3)
        if curr_info['ball'][0] > last_info['ball'][0] and curr_info['ball'][1] < last_info['ball'][1]:
            # (+, -)
            direction.append(4)

        # append platform x
        platform_x.append(curr_info['platform'][0])

        # append predict x
        predict_by_rule = predict(
            curr_info['ball'][0],
            curr_info['ball'][1],
            last_info['ball'][0],
            last_info['ball'][1],
            curr_info['platform'][0],
            curr_info['bricks'] + curr_info['hard_bricks']
        )
        predict_x.append(predict_by_rule)

        # append command
        if command[i] == 'NONE':
            command_num.append(0)
        elif command[i] == 'MOVE_LEFT':
            command_num.append(-1)
        else:
            command_num.append(1)

    # print(direction)

    numpy_data = np.array([
        curr_x,
        curr_y,
        last_x,
        last_y,
        # direction
        platform_x,
        predict_x
    ])

    X = np.transpose(numpy_data)
    y = command_num

    # print(len(curr_x), len(curr_y))

    # train data
    from sklearn.neighbors import KNeighborsClassifier

    model = KNeighborsClassifier(n_neighbors=3)
    print(model.fit(X, y))
    print(model.score(X, y))

    # store model
    with open(os.path.join(os.path.dirname(__file__), 'model.pickle'), 'wb') as f:
        pickle.dump(model, f)