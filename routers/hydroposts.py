import configparser
import csv
import json
from fastapi import APIRouter, Depends
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from crud.hydroposts import hydroposts_crud
from models.hydroposts_requests import CreateHydropostRequest, GetHydropostByRectRequest
import pandas as pd
from fastapi import FastAPI, File, UploadFile
import io 

router = APIRouter()

# Создание новой роли
@router.post("/new_hydropost", tags=["hydroposts"])
async def new_hydropost(hydropost: CreateHydropostRequest):
    await hydroposts_crud.create_hydropost(hydropost)
    return {"detail": "success"}

@router.post("/load_hydroposts", tags=["hydroposts"])
async def load_hydroposts(json_file: bytes = File()):
    data = json.loads(json_file.decode("utf-8") )
    points_data = data['aaData']
    for i, point in enumerate(points_data):
        try:    #TODO: Написать обертку
            await hydroposts_crud.create_hydropost(CreateHydropostRequest(**{'id':i, 'post_id': point[7], 'region': point[3], 'river': point[4], 'latitude': point[8], 'longitude': point[9], 'post_type': 0}))
        except:
            pass
    return {"detail": "success"}

def cord_transform(line):
    res = ""
    i = 0
    while not line[i].isdigit():
        i+=1
    while line[i].isdigit() or line[i] == '-':
        res += line[i]
        i+=1
    while not line[i].isdigit():
        i+=1
    secres = ""
    while i < len(line) and (line[i].isdigit() or line[i] == '-'):
        secres += line[i]
        i+=1
    print(res,secres)
    return float(secres)/60 + float(res)
    
@router.post("/load_meteostations", tags=["hydroposts"])
async def load_meteostations(post_type: int, csv_file: bytes = File()):
    csv = pd.read_csv(io.StringIO(csv_file.decode("utf-8")))
    print(csv['post_id'])
    for i, row in csv.iterrows():
        await hydroposts_crud.create_hydropost(CreateHydropostRequest(**{'id':i, 'post_id': row["post_id"], 'region': row["name"], 'river': row["name"], 'latitude': cord_transform(row["latitude"]), 'longitude': cord_transform(row["longitude"]), 'post_type': post_type}))
    return {"detail": "success"}

@router.get("/get_hydroposts_by_rect", tags=["hydropost"])
async def get_hydroposts_by_rect(x0: float, y0: float, x1: float, y1: float):
    return await hydroposts_crud.get_hydroposts_by_rect(x0, y0, x1, y1)

@router.get("/get_hydroposts_by_date_and_rect", tags=["hydropost"])
async def get_hydroposts_by_date_and_rect(x0: float, y0: float, x1: float, y1: float, year: int, month: int, day: int):
    return await hydroposts_crud.get_hydroposts_by_date_and_rect(x0, y0, x1, y1, year, month, day)

@router.get("/get_hydroposts_history", tags=["hydropost"])
async def get_hydroposts_history(post_id: int, year: int, month: int, day: int):
    return hydroposts_crud.get_history(region='Amur', post_id=post_id, year=year, month=month, day=day)
    
@router.get("/get_hydroposts_calendar", tags=["hydropost"])
async def get_hydroposts_calendar(post_id: int):
    return hydroposts_crud.get_calendar(region='Amur', post_id=post_id)