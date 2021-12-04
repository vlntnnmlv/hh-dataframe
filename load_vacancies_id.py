from datetime import datetime, timedelta
import requests
import logging
import pickle

# hh.ru API domain
main_domain = "https://api.hh.ru/"

# logger object
logger = logging.getLogger("hhparser")
logger.setLevel(logging.INFO)

def getPageJSON(date_from=None, date_to=None, area=1, page=0, per_page=100, url=None):
    """ 
    Returns JSON with per_page amount of vacancies from the given area on given 'page'

    date_from, date_to - strings in ISO format
    area - where vacancies are published
    """

    requests.get()
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
        url = main_domain + f"vacancies?area={area}"
    return requests.get(
            url,
            headers=headers,
            params=params
        ).json()

def getVacanciesID(area=1):
    """ Returns list of all vacancies ids in given area """
    ids = []
    start_date = (datetime.now() - timedelta(days=30)).replace(day = 14)
    end_date = datetime.now()
    step = timedelta(minutes=30)
    i = 0
    logging.info("Started request loop")
    while start_date + (i + 1) * step <= end_date:
        logger.info(
            f'got response on dates: {(start_date + i * step).isoformat()} - {(start_date + (i + 1) * step).isoformat()}'
            )
        r = getPageJSON((start_date + i * step).isoformat(), (start_date + (i + 1) * step).isoformat(), area=area)
        if 'errors' in r.keys():
            logger.error('Unexpected response from the server')
            logger.error(r)
            break
        if 'items' in r.keys():
            logger.info('extracting alternate urls...')
            new_ids = [item['alternate_url'] for item in r['items']]
            ids += new_ids
            logger.info(f'added {len(new_ids)} new alternate urls')

        if 'pages' in r.keys():
            logger.info('got more than one page, extracting remained alternate urls...')
            for j in range(1, r['pages']):
                r_p = getPageJSON(
                        (start_date + i * step).isoformat(),
                        (start_date + (i + 1) * step).isoformat(),
                        page = j
                    )
                if 'items' in r_p.keys():
                    new_ids = [item['alternate_url'] for item in r_p['items']]
                    ids += new_ids
                    logger.info(f'added {len(new_ids)} new alternate urls')
        i += 1
    
    for i in range(len(ids)):
        ids[i] = ids[i].split('/')[-1]
    return ids

if __name__ == "__main__":
    data = getVacanciesID()
    with open("02_12_2021_vacancies_id", "wb") as out:
        pickle.dump(data, out)
