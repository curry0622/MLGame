import os
import pickle
import numpy as np

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedShuffleSplit

if __name__ == "__main__":
  platform_x = []
  predict_ball_x = []
  motion = []
  motion_num = []

  for i in range(1, 14):
    with open(os.path.join(os.path.dirname(__file__), "./records/2P/win/good/" + str(i) + ".pickle"), "rb") as f:
      data = pickle.load(f)
      platform_x = data["platform_x"]
      predict_ball_x = data["predict_ball_x"]
      motion = data["motion"]

  for i in range(0, len(motion)):
    if motion[i] == "MOVE_LEFT":
      motion_num.append(-1)
    elif motion[i] == "MOVE_RIGHT":
      motion_num.append(1)
    else:
      motion_num.append(0)

  numpy_data = np.array([
    platform_x,
    predict_ball_x
  ])

  X = np.transpose(numpy_data)
  y = motion_num

  x_train, x_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=9
  )

  # parameter interval
  param_grid = {'n_neighbors': [1, 2, 3]}

  # cross validation
  cv = StratifiedShuffleSplit(n_splits=2, test_size=0.3, random_state=12)
  grid = GridSearchCV(KNeighborsClassifier(), param_grid,
                      cv=cv, verbose=10, n_jobs=-1)
  grid.fit(x_train, y_train)
  grid_predictions = grid.predict(x_test)

  # print result
  print("Best parameter: ")
  print(grid.best_params_)
  print()
  print("Prediction: ")
  print(grid_predictions)
  print()
  print("Confusion Matrix: ")
  print(confusion_matrix(y_test, grid_predictions))
  print()
  print("Classification Report: ")
  print(classification_report(y_test, grid_predictions))

  # store model
  with open(os.path.join(os.path.dirname(__file__), 'model_2P_win_good.pickle'), 'wb') as f:
    pickle.dump(grid, f)
