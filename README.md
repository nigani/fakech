# FakeCheck

Fake news checking

---

## Resources
This project has some key dependencies:

| Dependency Name      | Documentation                                   | Description                                                                                     |
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

## Run

```
cd ./fakecheck
bash ./create_virtualenv.sh
uvicorn app.api:app --reload
```
Open your browser to http://localhost:8000/docs to view the OpenAPI UI.
For an alternate view of the docs navigate to http://localhost:8000/redoc