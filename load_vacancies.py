import requests
import pickle
import logging
from lxml.html import fromstring
from itertools import cycle
from time import sleep

# hh.ru API domain
main_domain = "https://api.hh.ru/"

# logger object
logger = logging.getLogger("hhparser")
logger.setLevel(logging.INFO)

def getVacancies(ids, prev_vcs):
    vcs = prev_vcs
    if prev_vcs:
        i = ids.index(prev_vcs[-1]["id"]) + 1
    else:
        i = 0
    print(f"Starting index is {i} in id {ids[i]}")
    j = 0
    print("Started request loop")
    while i < len(ids):
        res = requests.get(f"{main_domain}vacancies/{ids[i]}")
        print(f"Got response on id {ids[i]}")
        if res.status_code == 200:
            j = 0
            print("Got nice reponse, processing...")
            vcs.append(res.json())
        elif res.status_code == 403:
            print("Got 403 status code")
            return vcs
        
        sleep(0.1)
        i+=1

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

    if vcs:
        print("Found local vacancies")
    else:
        print("Local vacancies are empty")

    vcs = getVacancies(ids, vcs)

    with open("02_12_2021_vacancies", "wb") as out:
        pickle.dump(vcs, out)