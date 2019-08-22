import pandas as pd
from pandas._config import display
from pandas import Series,DataFrame
ershou = pd.read_csv("ershou.csv")

ershou.info()
ershou.describe()
df = ershou.copy()
df['price'].map()