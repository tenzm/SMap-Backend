import configparser

import json
from fastapi import APIRouter, Depends
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from crud.hydroposts import hydroposts_crud
from models.hydroposts_requests import CreateHydropostRequest, GetHydropostByRectRequest

from fastapi import FastAPI, File, UploadFile

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
        print(point[7])
        try:    #TODO: Написать обертку
            await hydroposts_crud.create_hydropost(CreateHydropostRequest(**{'id':i, 'post_id': point[7], 'region': point[3], 'river': point[4], 'latitude': point[8], 'longitude': point[9]}))
        except:
            pass
    return {"detail": "success"}

@router.get("/load_hydroposts", tags=["hydropost"])
async def load_hydroposts(rect: GetHydropostByRectRequest):
    pass