from datetime import time
from os import times
import pickle
from vacancy.extract import getVacanciesID, getVacancies
from vacancy.transform import toDataFrame
from vacancy.utility import timestamp
import os

def main():
    area = 14
    backstep = 30
    print("Extracting ids...")
    if (os.path.isfile(f"./{timestamp()}_{area}_{backstep}_ids.pickle")):
        print("Found cached ids")
        with open(f"./{timestamp()}_{area}_{backstep}_ids.pickle", "rb") as inp:
            ids = pickle.load(inp)
    else:
        ids = getVacanciesID(area=area, backstep=backstep, save=True)
    print(f"Got {len(ids)} ids on area {area} with backtep {backstep}")
    print("Extracting vacancies...")
    vcs = getVacancies(ids)
    print("Transforming to dataframe...")
    df = toDataFrame(vcs)
    print("Saving to .csv...")
    df.to_csv(f"{timestamp()}_{area}_{backstep}.csv", sep=';')
    print("Done! Enjoy your dataset!")

if __name__ == "__main__":
    main()