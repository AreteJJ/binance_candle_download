from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from math import sqrt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import time
import matplotlib.pyplot as plt


# connecting separate csv files
# data from https://www.cryptodatadownload.com/data/
df = pd.DataFrame()
path = ""
for files in os.listdir(path):
    print(files)
    results = pd.read_csv(f"{path}/{files}", sep=";")
    df = pd.concat([df_merged, results], axis=1)


# converting dataframe to dictionary containing dataframes with given log return
r = 5
ret_dict = defaultdict(dict)
itr = range(0, 12, 3)
for i in range(1, r):
    l = str(i)
    ret_dict[f"df_ret_{l}"] = pd.DataFrame()
    for k in itr:
        add = df.iloc[:, k].pct_change(i).shift(-i).round(5)
        add = np.log(1 + add)
        ret_dict[f"df_ret_{l}"] = pd.concat([ret_dict[f"df_ret_{l}"], add], axis=1)
    day_time = df.iloc[:, -2:].shift(-i)
    ret_dict[f"df_ret_{l}"] = pd.concat([ret_dict[f"df_ret_{l}"], day_time], axis=1)
    ret_dict[f"df_ret_{l}"] = ret_dict[f"df_ret_{l}"].dropna()


# function creating dataframe with window slide for given crypto
def window_converter(col1, col2, wl):
    window = pd.DataFrame()
    for i in range(0, wl):
        l = wl-i
        add = ret_dict[f"df_ret_{1}"].iloc[:, col1].shift(l)
        window = pd.concat([window, add], axis=1)
    for i in range(0, wl):
        l = wl-i
        add = ret_dict[f"df_ret_{1}"].iloc[:, col2].shift(l)
        window = pd.concat([window, add], axis=1)
    add = ret_dict[f"df_ret_{1}"].iloc[:, col2].shift(l-1)
    window = pd.concat([window, add], axis=1)
    window = window.dropna()
    return window


# fitting the model and making prediction
window = window_converter(0, 2, 15)
train_windows = window.iloc[:100000, :]
test_windows = window.iloc[100000:150000, :]
lr_model = LinearRegression()
lr_model.fit(train_windows.iloc[:, :-1], train_windows.iloc[:, -1])

t0 = time.time()
lr_y = test_windows.iloc[:, -1].values
lr_y_pred = lr_model.predict(test_windows.iloc[:,:-1])
tF = time.time()


# testing results
rmse = sqrt(mean_squared_error(lr_y, lr_y_pred))
r_score = r2_score(lr_y, lr_y_pred)
print(f'Test RMSE: {rmse}')
print(f"Test R2: {r_score}")


# visualizing predictions and real values
plt.plot(lr_y[2000:2100])
plt.plot(lr_y_pred[2000:2100], color="red")
