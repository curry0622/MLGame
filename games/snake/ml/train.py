import os
import pickle
import numpy as np

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedShuffleSplit

if __name__ == "__main__":
  x = []
  y = []
  # p_x = []
  # p_y = []
  dir = []
  dir_num = []
  odd = []
  move = []
  move_num = []

  with open(os.path.join(os.path.dirname(__file__), "./pickles/test.pickle"), "rb") as f:
    data = pickle.load(f)
    x = data["x"]
    y = data["y"]
    # p_x = data["p_x"]
    # p_y = data["p_y"]
    dir = data["dir"]
    odd = data["odd"]
    move = data["move"]

  for i in range(0, len(move)):
    if dir[i] == "UP":
      dir_num.append(1)
    elif dir[i] == "DOWN":
      dir_num.append(2)
    elif dir[i] == "LEFT":
      dir_num.append(3)
    else:
      dir_num.append(4)

    if move[i] == "UP":
      move_num.append(1)
    elif move[i] == "DOWN":
      move_num.append(2)
    elif move[i] == "LEFT":
      move_num.append(3)
    else:
      move_num.append(4)

  numpy_data = np.array([
    x,
    y,
    # p_x,
    # p_y
    dir_num,
    odd
  ])

  X = np.transpose(numpy_data)
  Y = move_num

  x_train, x_test, y_train, y_test = train_test_split(
    X,
    Y,
    test_size=0.2,
    random_state=12
  )

  # parameter interval
  param_grid = {'n_neighbors': [1, 2, 3, 4, 5]}

  # cross validation
  cv = StratifiedShuffleSplit(n_splits=2, test_size=0.2, random_state=12)
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
  with open(os.path.join(os.path.dirname(__file__), 'test.pickle'), 'wb') as f:
    pickle.dump(grid, f)