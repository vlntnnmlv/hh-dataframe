##############################################################
#                                                            #
#                VACANCY IDS  -->  VACANCIES                 #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
##############################################################

from asyncio.tasks import FIRST_EXCEPTION
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime, timedelta, date
from time import time
from utility import changeIP, timestamp

import requests
import logging
import pickle

# hh.ru API domain
main_domain = "https://api.hh.ru/"

# logger object
logger = logging.getLogger("hhparser")
logger.setLevel(logging.INFO)

### VACANCY ID

def getPage(date_from=None, date_to=None, area=1, page=0, per_page=100, url=None):
    """ 
    Returns JSON with per_page amount of vacancies from the given area on given page.

    date_from, date_to - strings in ISO format.
    area - where vacancies are published.
    """

    # header for browser
    headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}

    # request params
    params = {
            "page" : page,
            "per_page" : per_page
    }
    if date_from is not None and date_to is not None:
        params["date_from"] = date_from
        params["date_to"] = date_to

    if url is None:
        url = f"{main_domain}vacancies?area={area}"
    return requests.get(
            url,
            headers=headers,
            params=params
        )

def getVacanciesIDTask(date_from, date_to, area, ids_set, executor, page=0):
    """ Task function.
        Adds all vacancy ids to ids_set on given page. """

    r = getPage(date_from, date_to, area, page)
    if r.status_code != 200:
        print(f"Got bad response. Status code {r.status_code}")
        print("Trying to change IP...")
        if not changeIP():
            print("Could not change IP; Exiting.")
            executor.shutdown()
        else:
            getVacanciesIDTask(date_from, date_to, area, ids_set, executor, page)
    else:
        print(f"Got nice response, on {date_from}-{date_to} with {len(r.json()['items'])} items on page {page}\nextracting ids...")
        ids_set.update([item['alternate_url'] for item in r.json()['items']])

        return date_from, date_to, area, ids_set, r.json()

def getVacanciesIDDoneCallback(future):
    """ Callback function.
        If there is more than one page of vacancies,
        loops through all of them with Task function. """

    date_from, date_to, area, ids_set, page_json = future.result()
    if page_json['pages'] > 1:
        futures = []
        with ThreadPoolExecutor() as executor:
            for i in range(1, page_json['pages']):
                try:
                    futures.append(
                        executor.submit(getVacanciesIDTask, date_from, date_to, area, ids_set, executor, i)
                    )
                except Exception as e:
                    print(f"Got exception {e}; Breaking future creation loop")
                    break

        wait(futures)

def getVacanciesID(area, backstep=30, forwardstep=None, timestep=30, save=False):
    """ Returns list of vacancy id on given time period. """
    if forwardstep is None:
        forwardstep = datetime.now()

    ids = set()

    start_date = (datetime.now() - timedelta(days=backstep))
    end_date = forwardstep
    step = timedelta(minutes=timestep)

    i = 0

    futures = []

    print("Started future creation loop.")
    with ThreadPoolExecutor() as executor:
        while start_date + (i + 1) * step <= end_date:
            try:
                futures.append(
                    executor.submit(
                                getVacanciesIDTask,
                                (start_date + i * step).isoformat(),
                                (start_date + (i + 1) * step).isoformat(),
                                area,
                                ids,
                                executor,
                                )
                            )
                futures[-1].add_done_callback(getVacanciesIDDoneCallback)

            except Exception as e:
                print(f"Got exception {e}; Breaking future creation loop")
                break

            i+=1

    print("Waiting for futures to complete...")
    wait(futures, return_when=FIRST_EXCEPTION)
    print("Done!")

    ids = list(ids)
    for i in range(len(ids)):
        ids[i] = ids[i].split('/')[-1]
    if save:
        with open(f"{timestamp()}_{area}_{backstep}_ids.pickle", "wb") as out:
            pickle.dump(ids, out)
    return ids

### VACANCY

def getVacancy(id, vcs, executor):
    r = requests.get(f"{main_domain}vacancies/{id}")
    if r.status_code != 200:
        print(f"Got bad response on id {id}. Status code {r.status_code}")
        print("Trying to change IP...")
        if not changeIP():
            print("Could not change IP; Exiting.")
            executor.shutdown()
        else:
            getVacancy(id, vcs, executor)
    else:
        print(f"Got nice response on id {id}, processing...")
        vcs.append(r.json())


def getVacancies(ids):
    vcs = []
    futures = []

    print("Started future creation loop.")
    with ThreadPoolExecutor() as executor:
        for id in ids:
            try:
                futures.append(
                    executor.submit(
                        getVacancy,
                        id,
                        vcs,
                        executor
                    )
                )
            except Exception as e:
                print(f"Got exception {e}; Breaking future creation loop")
                break

    print("Waiting for futures to complete...")
    wait(futures)
    print("Done!")

    return vcs