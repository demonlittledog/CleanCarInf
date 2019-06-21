import pandas as pd
import numpy as np
from voluptuous import Schema, Invalid, Required

users = pd.read_csv("D:/user.csv")
print(users)

old_title = users["Title"]
print(old_title)

new_title = pd.Series([])
for i, v in old_title.items():
    new_title = new_title.append(pd.Series([v.split('|')], index = [i]))
users.update(pd.DataFrame({'Title':new_title}))

print(users)