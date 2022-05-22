import pydantic
import json
from crud.base import BaseCrud
from fastapi import HTTPException
from db.models import hydroposts
from tortoise.contrib.pydantic import pydantic_model_creator
from models.hydroposts_requests import CreateHydropostRequest

class HydropostsCrud(BaseCrud):
    pydantic_model = pydantic_model_creator(hydroposts, name="hydroposts")
    target_model = hydroposts

    async def create_hydropost(self, req: CreateHydropostRequest):
        return await hydroposts.create(**{'region': req.region, 'river': req.river, 'latitude': req.latitude, 'longitude': req.longitude})
