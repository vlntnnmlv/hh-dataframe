import pickle
import pandas as pd

with open("02_12_2021_vacancies", "rb") as inp:
    raw_data = pickle.load(inp)

print(len(raw_data))

df = pd.DataFrame(raw_data)
