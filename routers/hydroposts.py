import configparser

from fastapi import APIRouter, Depends
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from crud.hydroposts import hydroposts_crud
from models.hydroposts_requests import CreateHydropostRequest

router = APIRouter()

# Создание новой роли
@router.post("/new_hydropost", tags=["hydroposts"])
async def new_role(hydropost: CreateHydropostRequest):
    await hydroposts_crud.create_hydropost(hydropost.region, hydropost.river, hydropost.latitude, hydropost.longitude)
    return {"detail": "success"}
