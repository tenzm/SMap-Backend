import pydantic
import json
import boto3
import csv
from crud.base import BaseCrud
from fastapi import HTTPException
from db.models import hydroposts
from tortoise.expressions import Q
from tortoise.contrib.pydantic import pydantic_model_creator
from models.hydroposts_requests import CreateHydropostRequest, GetHydropostByRectRequest

session = boto3.session.Session()

s3 = session.client(
    service_name='s3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='admin',
    aws_secret_access_key='minio123',   
)

class HydropostsCrud(BaseCrud):
    pydantic_model = pydantic_model_creator(hydroposts, name="hydroposts")
    target_model = hydroposts

    def get_csv_by_id(self, region: str, post_id: int):
        posts_histories = s3.list_objects(Bucket = 'meteo-data', Prefix=f'/{ region }/')
        filename = ''
        for post in posts_histories.get('Contents'):
            if post["Key"].split('-')[0] == 'Amur/' + str(post_id):
                filename = post["Key"]

        if filename == '':
            raise HTTPException(status_code=404, detail="Item not found")

        return s3.get_object(Bucket='meteo-data', Key = filename)['Body'].read().decode("utf-8")

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


    def get_history(self, region: str, post_id: int, year: int, month: int, day: int):
        decoded_data = self.get_csv_by_id(region=region, post_id=post_id)
        for line in decoded_data.split('\n'):
            if (f'{year:04}'+'-'+f'{month:02}'+'-'+f'{day:02}' in line):
                return int(line.split(';')[1])
        raise HTTPException(status_code=404, detail="Item not found")
        

    def get_calendar(self, region: str, post_id: int):
        decoded_data = self.get_csv_by_id(region=region, post_id=post_id)
        response = [line.split(';')[0] for line in decoded_data.split('\n') if not "Time" in line]
        return response