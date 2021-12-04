from asyncio.tasks import FIRST_EXCEPTION
from asyncio.windows_events import NULL
import requests
import pickle
import logging

from concurrent.futures import ThreadPoolExecutor, wait, FIRST_EXCEPTION
from lxml.html import fromstring
from itertools import cycle
from time import sleep

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
        # raise Exception
        executor.shutdown()

def getVacancies(ids, prev_vcs):
    vcs = prev_vcs
    if prev_vcs:
        i = ids.index(prev_vcs[-1]["id"]) + 1
    else:
        i = 0
    print(f"Starting index is {i} in id {ids[i]}")

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

            # print(f"Got response on id {ids[i]}")
            # if res.status_code == 200:
            #     print("Got nice reponse, processing...")
            #     vcs.append(res.json())
            # elif res.status_code == 403:
            #     print("Got 403 status code")
            #     return vcs
            
            sleep(0.1)
            i+=1
    
    print("Waiting for created futures to complete...")
    wait(futures, return_when=FIRST_EXCEPTION)
    print("Done!")
    return vcs
if __name__ == '__main__':
    print("Loading ids...")
    with open("02_12_2021_vacancies_id", "rb") as inp:
        ids = pickle.load(inp)
        print("Sorting ids...")
        ids.sort()

    print("Loading local vacancies...")
    try:
        with open("02_12_2021_vacancies", "rb") as inp:
            vcs = pickle.load(inp)
    except Exception:
        vcs = []

    print("Found local vacancies") if vcs else print("Local vacancies are empty")

    vcs = getVacancies(ids, vcs)

    with open("02_12_2021_vacancies", "wb") as out:
        pickle.dump(vcs, out)