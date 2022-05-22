import pydantic
from crud.base import BaseCrud
from fastapi import HTTPException
from db.models import hydroposts_model
from tortoise.contrib.pydantic import pydantic_model_creator
from models.hydroposts_requests import CreateHydropostRequest

class HydropostsCrud(BaseCrud):
    pydantic_model = pydantic_model_creator(hydroposts_model, name="hydroposts")
    target_model = hydroposts_model

    async def create_hydropost(self, req: CreateHydropostRequest):
        return await hydroposts_model.create(**{'region': req.region, 'river': req.river, 'latitude': req.latitude, 'longitude': req.longitude})