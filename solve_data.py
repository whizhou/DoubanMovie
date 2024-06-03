# 读取 MovieInfo.csv 并对数据进行转换

import numpy as np
import pandas as pd

data = pd.read_csv('MovieInfo_str.csv', dtype=str)

# print(data.head())

for item in data.loc[0]:
    print(f"{type(item)}: {item}")

data['year'] = data['year'].map(lambda x: int(x[1:]))
# print(data['year'])

# data['writers'] = data['writers'].map(lambda x: print(type(x)))
print(data['writers'])

