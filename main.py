from typing import Union
import uvicorn
from fastapi import FastAPI
from routers import hydroposts
from tortoise.contrib.fastapi import register_tortoise
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

DB_URL = config['DATABASE']['DatabaseType']+"://"+config['DATABASE']['Username']+":"+config['DATABASE']['Password']+"@"+config['DATABASE']['Hostname'] + ":" + config['DATABASE']['Port'] + "/" + config['DATABASE']['DatabaseName']


app = FastAPI()


app.include_router(hydroposts.router)


"""
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
"""

register_tortoise(
    app,
    db_url=DB_URL,
    modules={"models": ["db.models"]},
    generate_schemas=True,
)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="localhost", reload=True)
