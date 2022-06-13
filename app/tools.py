from datetime import datetime, timedelta, timezone
from ngutils import *
from pathlib import Path
import pandas as pd
import re
import requests
import io
import shutil

import torch
from transformers import AutoTokenizer, AutoModel
from transformers import pipeline


if "df_urls" not in globals():
    df_urls = pd.DataFrame(columns=['url', 'date', 'title', 'text', 'embeddings_title', 'embeddings_text'])


def news_load():
    global df_urls

    MSK = timezone(timedelta(hours=+3))
    UTC = timezone.utc
    BR = '\n'

#     start_date = datetime(2021, 9, 1, tzinfo=MSK).timestamp()  # Дата и время первой новости
    start_date = datetime(2022, 5, 1, tzinfo=MSK).timestamp()  # Дата и время первой новости

    if len(df_urls) > 0:
        try:
            start_date = max(pd.to_datetime(df_urls['date'])).replace(tzinfo=MSK).timestamp()
        except Exception:
            traceback.print_exc()

    current_session = requests.Session()
    num_page = 0
    req_date = datetime.now(MSK).timestamp()
    ids_set = set()

    while req_date > start_date:
        num_page += 1
        get_req = f"https://www.mos.ru/api/newsfeed/v4/frontend/json/ru/articles?fields=id,date_timestamp&page="\
                  f"{num_page}&per-page=50&sort=-date"
        r = current_session.get(get_req)
        req_ids, req_dts = list(zip(*re.findall(r"""{"id":(\d.*?),"date_timestamp":"(\d.*?)"}""", r.text, re.S)))
        ids_set.update(req_ids)
        req_date = int(req_dts[0])
        print(
            f"Loading mos.ru с 01.09.2021. Loaded {len(ids_set)} news to \
            {datetime.utcfromtimestamp(req_date).strftime('%Y-%m-%d')}.",
            end='\r', flush='True')

    urls_to_load = list("https://www.mos.ru/news/item/"
                        + pd.DataFrame(ids_set)[0].astype(int).sort_values().astype(str) + "/")

    print(len(urls_to_load))

    dl_urls = dict()

    err_io_stream = io.StringIO()

    def news_parser(text, url, url_source=None):
        url_source = url_source or url
        text_news = reduce_content(text)
        t_result = re.findall(
            """datetime="(.*?)".*?<h1 class="news-article-title-container__title">(.*?)<.*?"""
            """<div class="news-article__text">(.*?)<div class="news-article-footer news">""",
            text_news, re.S)[0]
        t_date = t_result[0] + ' +0300'
#         print(t_date)
        t_title = text_beautifier(t_result[1])
        t_text = text_beautifier(
            t_result[2].replace("</p>", "</p>\n").replace("</h2>", "</h2>\n").splitlines()).replace(
            "\r ", "\r").replace(" \r", "\r").replace("\r", "\n")
        news_id = url_source.split('/')[-2]
        dl_urls[news_id] = [url_source, t_date, t_title, t_text]

    read_urls_contents(urls_to_load, session=current_session, parser=news_parser, error_page_output=err_io_stream)
    if len(urls_to_load) == len(dl_urls):
        print('OK, news count:', len(dl_urls))
    else:
        print(f"Dismiss:\n{BR.join(set(urls_to_load) - set(dl_urls))}")
        print("Download errors\n", err_io_stream.getvalue())

    df_urls_new = pd.DataFrame.from_dict(dl_urls, orient='index', columns=['url', 'date', 'title', 'text'])
    df_urls_new = df_urls_new.loc[df_urls_new.index.difference(df_urls.index)]

    # tokenizer = AutoTokenizer.from_pretrained("cointegrated/LaBSE-en-ru")
    # model = AutoModel.from_pretrained("cointegrated/LaBSE-en-ru")
    #
    # sentences = list(df_urls_new['title'])
    # encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
    #
    # with torch.no_grad():
    #     model_output = model(**encoded_input)
    #
    # embeddings_title = model_output.pooler_output
    # embeddings_title = torch.nn.functional.normalize(embeddings_title)
    #
    # df_urls_new['embeddings_title'] = embeddings_title
    #
    # sentences = list(df_urls_new['text'])
    # encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
    #
    # with torch.no_grad():
    #     model_output = model(**encoded_input)
    #
    # embeddings_text = model_output.pooler_output
    # embeddings_text = torch.nn.functional.normalize(embeddings_text)

    df_urls_new['embeddings_text'] = embeddings_text

    df_urls = pd.concat([df_urls, df_urls_new])

    response = {"Всего новостей": len(df_urls)}
    response.update(
        df_urls[['url', 'date', 'title', 'text']].sort_values('date', ascending=False).head(10).to_dict('index'))

    return response


def similar_news_find(text):

    # response = df.to_dict('index'))
    response = None
    return response


# p = pipeline(
#   task='zero-shot-classification',
#   model='cointegrated/rubert-base-cased-nli-threeway'
# )
# p(
#   sequences=df_news[8],
#   candidate_labels="Хорошо, Плохо",
#   hypothesis_template="{}."
# )
