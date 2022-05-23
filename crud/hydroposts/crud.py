import pydantic
import json
from crud.base import BaseCrud
from fastapi import HTTPException
from db.models import hydroposts
from tortoise.expressions import Q
from tortoise.contrib.pydantic import pydantic_model_creator
from models.hydroposts_requests import CreateHydropostRequest, GetHydropostByRectRequest

class HydropostsCrud(BaseCrud):
    pydantic_model = pydantic_model_creator(hydroposts, name="hydroposts")
    target_model = hydroposts

    async def create_hydropost(self, req: CreateHydropostRequest):
        return await hydroposts.create(**{'region': req.region, 'post_id': req.post_id, 'river': req.river, 'latitude': req.latitude, 'longitude': req.longitude})

    async def get_hydroposts_by_rect(self, x0: float, y0: float, x1: float, y1: float):
        result = await hydroposts.filter(Q(Q(latitude__gte=x0), Q(latitude__lte=x1), Q(longitude__gte=y0), Q(longitude__lte=y1), join_type="AND"))
        response = list()
        for item in result:
            response.append({
                'post_id': item.post_id,
                'region': item.region,
                'river': item.river,
                'latitude': item.latitude,
                'longitude': item.longitude
            })
            
        return response
