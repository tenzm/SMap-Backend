from typing import Union
import uvicorn
from fastapi import FastAPI
import json

#TODO: Переделать на бд
with open('./SberMap/data/positions.txt') as json_file:
    data = json.load(json_file)
data.keys()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="localhost", reload=True)
