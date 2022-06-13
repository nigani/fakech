from datetime import datetime, timedelta, timezone
from ngutils import *
from pathlib import Path
import pandas as pd
import re
import requests
import io
import shutil


def news_load():
    MSK = timezone(timedelta(hours=+3))
    UTC = timezone.utc
    BR = '\n'

    START_DATE = datetime(2021, 9, 1, tzinfo=MSK).timestamp()  # Дата и время первой новости

    current_session = requests.Session()
    num_page = 0
    req_date = datetime.now(MSK).timestamp()
    ids_set = set()

    while req_date > START_DATE:
        num_page += 1
        get_req = f"https://www.mos.ru/api/newsfeed/v4/frontend/json/ru/articles?fields=id,date_timestamp&page="\
                  f"{num_page}&per-page=50&sort=-date"
        r = current_session.get(get_req)
        req_ids, req_dts = list(zip(*re.findall(r"""{"id":(\d.*?),"date_timestamp":"(\d.*?)"}""", r.text, re.S)))
        ids_set.update(req_ids)
        req_date = int(req_dts[0])
        print(
            f"Загружается список новостей mos.ru с 01.09.2021 г. Загружено {len(ids_set)} новостей по \
            {datetime.utcfromtimestamp(req_date).strftime('%Y-%m-%d')}.",
            end='\r', flush='True')

    urls_to_load = list("https://www.mos.ru/news/item/"
                        + pd.DataFrame(ids_set)[0].astype(int).sort_values().astype(str) + "/")

    print(len(urls_to_load))

    df = urls_to_load[-10:]

    return df
