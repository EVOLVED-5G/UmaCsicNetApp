from marshmallow import fields
from netapp import ma


class CellSchema(ma.Schema):
    #id = fields.Integer(dump_only=True)
    cell_num = fields.String()
    crop_type = fields.String()
    #historics = fields.Nested('HistoricSchema', many=True)

class HistoricSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    temperature = fields.String()
    humidity = fields.String()
    timestamp = fields.DateTime()
    crop = fields.String()