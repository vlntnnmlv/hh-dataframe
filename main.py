import pickle
import os
from vacancy.extract import getVacanciesID, getVacancies, updateAreas
from vacancy.transform import toDataFrame
from vacancy.utility import timestamp
import argparse
import os

def main():

    parser = argparse.ArgumentParser(description="Create .csv dataset on given area")
    parser.add_argument("area", metavar="area", type=str)
    parser.add_argument("backstep", metavar="backstep", type=int)
    args = parser.parse_args()

    areas = updateAreas(save=True)
    try:
        area = areas[args.area]
    except KeyError as k:
        print(f"{args.area} nor found in areas dictionary. Area is set to 1")
        area = 1

    backstep = args.backstep
    print("Extracting ids...")
    if (os.path.isfile(f"./vacancy/{timestamp()}_{area}_{backstep}_ids.pickle")):
        print("Found cached ids.")
        with open(f"./vacancy/{timestamp()}_{area}_{backstep}_ids.pickle", "rb") as inp:
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