from tortoise import fields
from tortoise.models import Model

class hydroposts(Model):
    id = fields.IntField(pk = True)
    post_id = fields.IntField()
    region = fields.TextField()
    river = fields.TextField()
    latitude = fields.FloatField()
    longitude = fields.FloatField()

