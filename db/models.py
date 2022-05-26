from tortoise import fields
from tortoise.models import Model

class hydroposts(Model):
    id = fields.IntField(pk = True)
    post_id = fields.IntField()
    region = fields.TextField()
    river = fields.TextField()
    latitude = fields.FloatField()
    longitude = fields.FloatField()
    post_type = fields.IntField() # 0 - метео, 1 - гидро, 2 - снег

