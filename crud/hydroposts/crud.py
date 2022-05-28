from pdb import post_mortem
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
    endpoint_url='http://minio:9000',
    aws_access_key_id='admin',
    aws_secret_access_key='minio123',   
)

class HydropostsCrud(BaseCrud):
    pydantic_model = pydantic_model_creator(hydroposts, name="hydroposts")
    target_model = hydroposts

    # Получение csv из s3
    def get_csv_by_id(self, region: str, post_id: int):
        posts_histories = s3.list_objects(Bucket = 'meteo-data', Prefix=f'/{ region }/')
        filename = ''
        for post in posts_histories.get('Contents'):
            if post["Key"].split('-')[0] == 'Amur/' + str(post_id):
                filename = post["Key"]

        if filename == '':
            raise HTTPException(status_code=404, detail="Item not found")

        return s3.get_object(Bucket='meteo-data', Key = filename)['Body'].read().decode("utf-8")

    # Создание нового гидропоста в базе данных
    async def create_hydropost(self, req: CreateHydropostRequest):
        return await hydroposts.create(**{'region': req.region, 'post_id': req.post_id, 'river': req.river, 'latitude': req.latitude, 'longitude': req.longitude, 'post_type': req.post_type})

    # Получение гидропоста по заданной области
    async def get_hydroposts_by_rect(self, x0: float, y0: float, x1: float, y1: float):
        result = await hydroposts.filter(Q(Q(latitude__gte=x0), Q(latitude__lte=x1), Q(longitude__gte=y0), Q(longitude__lte=y1), join_type="AND"))
        response = list()
        for item in result:
            response.append({
                'post_id': item.post_id,
                'region': item.region,
                'river': item.river,
                'latitude': item.latitude,
                'longitude': item.longitude,
                'post_type': item.post_type
            })
        return response


    # Получение истории по заданному гидропосту в заданный момент времени
    def get_history(self, region: str, post_id: int, year: int, month: int, day: int):
        decoded_data = self.get_csv_by_id(region=region, post_id=post_id)
        for line in decoded_data.split('\n'):
            if (f'{year:04}'+'-'+f'{month:02}'+'-'+f'{day:02}' in line):
                return int(line.split(';')[1])
        raise HTTPException(status_code=404, detail="Item not found")

    # Получение всех гидропостов по дате в заданной области
    async def get_hydroposts_by_date_and_rect(self, x0: float, y0: float, x1: float, y1: float, year:int, month:int, day:int):
        result = await hydroposts.filter(Q(Q(latitude__gte=x0), Q(latitude__lte=x1), Q(longitude__gte=y0), Q(longitude__lte=y1), join_type="AND"))
        response = list()
        print(result)
        for item in result:
            data = {
                'post_id': item.post_id,
                'region': item.region,
                'river': item.river,
                'latitude': item.latitude,
                'longitude': item.longitude,
                'post_type': item.post_type}
            try:
                data['value'] = self.get_history('Amur', item.post_id,year, month, day)
                data['status'] = 200
            except:
                data['value'] = 0
                data['status'] = 404
            response.append(data)
        return response

    # Получение информации о гидропосте по его id
    async def get_hydropost_by_id(self, pid: int):
        result = await hydroposts.filter(post_id = pid)
        return result

    # Получение данных всех показаний ао определенному гидропосту
    def get_calendar(self, region: str, post_id: int):
        decoded_data = self.get_csv_by_id(region=region, post_id=post_id)
        print(decoded_data.split('\n')), 
        response1 = [line.split(';')[0] for line in decoded_data.split('\n') if (not "Time" in line) and len(line)>0]       
        response2 = [line.split(';')[1] for line in decoded_data.split('\n') if (not "Time" in line) and len(line)>0]

        return [response1, response2]