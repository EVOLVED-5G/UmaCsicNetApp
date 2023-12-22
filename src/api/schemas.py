from marshmallow import fields
from src import ma

# Serialization of a cell
class CellSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    cell_num = fields.String()

# Serialization of a cell with detail
class CellSchemaVerbose(ma.Schema):
    id = fields.Integer(dump_only=True)
    cell_num = fields.String()
    historics = fields.Nested('HistoricSchema', many=True)

# Serialization of a historic
class HistoricSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    timestamp = fields.DateTime()
    HS10_0 = fields.Float()
    HS10_1 = fields.Float()
    HS10_2 = fields.Float()
    HS30_0 = fields.Float()
    HS30_1 = fields.Float()
    HS30_2 = fields.Float()
    HS50_0 = fields.Float()
    HS50_1 = fields.Float()
    HS50_2 = fields.Float()
    FullBR = fields.Float()
    AirTC = fields.Float()
    RH = fields.Float()
    Pressure_1 = fields.Float()
    Pressure_2 = fields.Float()