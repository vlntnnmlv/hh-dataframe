from asyncio.tasks import FIRST_EXCEPTION
import pandas as pd
import requests
import pickle
import sqlite3

from concurrent.futures import ThreadPoolExecutor, wait
from create_dataframe import toDataFrame
from time import sleep, time


# hh.ru API domain
main_domain = "https://api.hh.ru/"

def getVacancy(id, vacancy_list, executor):
    res = requests.get(f"{main_domain}vacancies/{id}")
    print(f"Got response on id {id}")
    if res.status_code == 200:
        print("Got nice reponse, processing...")
        vacancy_list.append(res.json())
    elif res.status_code == 403:
        print("Got 403 status code")
        executor.shutdown()

def getVacancies(ids, last_loaded_id_index):
    vcs = []
    i = last_loaded_id_index
    print(f"Starting index is {i} on id {ids[i]}")
    print("Started future creation loop")

    futures = []
    with ThreadPoolExecutor() as executor:
        while i < len(ids):
            try:
                futures.append(
                        executor.submit(getVacancy, ids[i], vcs, executor)
                    )
            except Exception as e:
                print(f"Got exception:\n{e}\nBreaking future creation loop...")
                break

            sleep(0.1)
            i+=1
    
    print("Waiting for created futures to complete...")
    wait(futures, return_when=FIRST_EXCEPTION)
    print("Done!")
    return vcs

def main():
    print("Loading ids...")
    with open("02_12_2021_vacancies_id", "rb") as inp:
        ids = pickle.load(inp)
        print("Sorting ids...")
        ids = list(ids)
        ids.sort()

    print("Loading local vacancies...")
    last_id_index = 0
    try:
        db = sqlite3.connect("hh.db")
        local_ids = pd.read_sql_query("SELECT id FROM Vacancies", db)
        last_id_index = ids.index(int(local_ids.id.values[-1]))
        print(f"Found local vacancies. Last loaded id index is {last_id_index}")
    except Exception as e:
        print("Didn't find any local vacancies. Last loaded id index is set to 0")

    vcs = getVacancies(ids, last_id_index)
    df = toDataFrame(raw_data=vcs)

    
    with open("02_12_2021_vacancies", "wb") as out:
        pickle.dump(vcs, out)

if __name__ == '__main__':
    main()
