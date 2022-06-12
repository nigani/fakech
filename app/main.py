from typing import Union
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Form, File, UploadFile

app = FastAPI()


@app.get("/news/{news_id}")
def read_item(news_id: int, q: Union[str, None] = None):
    return {"news_id": news_id, "q": q}


@app.post("/login/")
async def login(username: str = Form("user"), password: str = Form("pwd")):
    return {"username": username, "password": password}


@app.post("/files/")
async def create_file(file: bytes = File("")):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    return {"filename": file.filename, "file_size": len(contents)}


@app.get("/")
def root():
    return HTMLResponse("<b>Hello world</b>")