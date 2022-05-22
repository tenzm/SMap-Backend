from tortoise import fields
from tortoise.models import Model

class hydropost_model(Model):
    id = fields.IntField(pk = True)
    region = fields.TextField()
    river = fields.TextField()
    latitude = fields.FloatField()
    longitude = fields.FloatField()

