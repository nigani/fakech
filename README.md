# FakeCheck

Fake news checking

---

## Ресурсы
В ходе работы над проектом опробовано применение следующих моделей:

| Name                 | Documentation                                   | Description                                                                                     |
|----------------------|-------------------------------------------------|-------------------------------------------------------------------------------------------------|
| DeepPavlov           | https://deeppavlov.ai                           | An open source conversational AI framework                                                      |
| TensorFlow           | https://www.tensorflow.org                      | TensorFlow is an end-to-end open source platform for machine learning                           |
| LaBSE                | https://tfhub.dev/google/LaBSE                  | Language-agnostic BERT sentence embedding model supporting 109 languages                        |
| spaCy                | https://spacy.io                                | Industrial-strength Natural Language Processing (NLP) with Python and Cython                    |
| FastAPI              | https://fastapi.tiangolo.com                    | FastAPI framework, high performance, easy to learn, fast to code, ready for production          |
| SentenceTransformers | https://www.sbert.net                           | Sentence Embeddings using Siamese BERT-Networks for state-of-the-art, text and image embeddings |
| Natasha              | https://natasha.github.io                       | Проект Natasha — набор Python-библиотек для обработки текстов на естественном русском языке     |
| Dostoevsky           | https://github.com/bureaucratic-labs/dostoevsky | Sentiment analysis library for russian language                                                 |
---

## Запуск на локальной машинне

Для запуска на локальной машине исполните следующий код:
```
cd ./fakech
uvicorn app.main:app --reload
```
Интерактивная документация по API в соответствии со стандартом OpenAPI UI здесь - http://localhost:8000/docs
Альтернативное представление документации расположено по адресу - http://localhost:8000/redoc

## Формирование образа docker
```
docker build -t myimage ./
docker run -d --name mycontainer -p 80:80 myimage
```
В результате получаем оптимизированный веб-сервис FastAPI в контейнере Docker. 
Он автоматически подстраивается под мощности текущего сервера и количество ядер ЦП.
Подробнее - https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker

## Структура проекта
```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── tools.py
├── Dockerfile
└── requirements.txt
```

## Подход к решению задачи

Структура решения - три подзадачи:
1. Сборщик новостей из авторитетных источников. Работает постоянно в фоне. Требует список авторитетных источников и алгоритм разбора страниц для сбора текста новостей. В целях хакатона база данных новостей будет собрана с mos.ru за 9 месяцев
2. API. Работает по запросу На входе текст, на выходе оценка достоверности новости (1-100 баллов)
3. Интерфейс для демонстрации работы API

Сборщик новостей с mos.ru реализован.
Интерфейс для демонстрации работы API автоматизирован средствами фреймворка
API реализован только в части сбора новостей, проверка на фейки не реализована

Описание алгоритма определения фейковой новости

Формируем для каждой новости набор метрик/оценок:
- тональность заголовка
- схожесть семантик заголовка и текста новости
- тональность текста новости
- количество опечаток

Находим первоисточник

Проводим сравнение с первоисточником

Базовые метрики:
- семантическая близость заголовков
- семантическая близость первых абзацев (там обычно суть новости)
- семантическая близость текстов без первого абзаца
- близость по тональности заголовков
- близость по тональности первых абзацев
- близость по тональности текстов без первого абзаца

Дополнительные метрики рассчитываются после выявления в тексте новости и первоисточника именованных сущностей (NER) - 
персоналий, организаций, мест, числительных:
- Отсутствие лишних упоминаний по сравнению с источником
- Полнота всех упоминаний по сравнению с источником
- Соответствие связей между сущностями в первоисточнике и новости
- Соответствие тональности упоминаний сущностей в первоисточнике и новости

Базовый стек и модели: python, Natasha, FastText, FastAPI, dostoevsky, transformers, LaBSE

Метрики опробованы, наилучший результат получен на модели sentence-transformers/LaBSE.

