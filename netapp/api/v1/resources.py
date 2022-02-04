from flask import request, Blueprint
from flask_restful import Resource, Api
import json
from requests import get, post, delete
import ast
import datetime
from netapp.error.error_handling import ObjectNotFound
from netapp.models import Cell, Historic
from netapp.schemas import CellSchema, HistoricSchema
from netapp import db 
from evolved5g.sdk import LocationSubscriber
from evolved5g import swagger_client
from evolved5g.swagger_client import LoginApi, User
from evolved5g.swagger_client.models import Token

bp_api = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(bp_api)

cell_schema = CellSchema()
historic_schema = HistoricSchema()

netapp_id = "myNetapp"


def get_token():
    username = "admin@my-email.com"
    password = "pass"
    configuration = swagger_client.Configuration()
    configuration.host = get_host_of_the_nef_emulator()
    api_client = swagger_client.ApiClient(configuration=configuration)
    api_client.select_header_content_type(["application/x-www-form-urlencoded"])
    api = LoginApi(api_client)
    token = api.login_access_token_api_v1_login_access_token_post("", username, password, "", "", "")
    return token

def get_host_of_the_nef_emulator() -> str:
    return "http://backend:80"

def get_location(external_id):
    token = get_token()
    host = get_host_of_the_nef_emulator()
    
    location_subscriber = LocationSubscriber(host, token.access_token)

    location_info = location_subscriber.get_location_information(
        netapp_id=netapp_id,
        external_id=external_id
    )
    return location_info
"""
def delete_subscription(self, id=None):
    token = get_token()
    host = get_host_of_the_nef_emulator()
    location_subscriber = LocationSubscriber(host, token["access_token"])

    if id is None:
        all_subscriptions = location_subscriber.get_all_subscriptions(netapp_id, 0, 100)
        for subscription in all_subscriptions:
            id = subscription.link.split("/")[-1]
            location_subscriber.delete_subscription(netapp_id, id)
    else:
        location_subscriber.delete_subscription(netapp_id, id)
"""

class CellManagement(Resource):
    def get(self, num=None):
        if num is not None:
            cell = Cell.query.filter_by(cell_num=num).first()
            if cell is None:
                raise ObjectNotFound('Cell '+ num + ' not found in database')
            result = cell_schema.dump(cell)
        else:
            cells = Cell.query.all()
            result = cell_schema.dump(cells, many=True)
        return result

    def post(self):
        cell_data = request.form
        cell = Cell(cell_num=cell_data['cell_num'],crop_type=cell_data['crop_type'])
        db.session.add(cell)
        db.session.commit()
    
    def put(self, num):
        cell_data = request.form
        cell = Cell.query.filter_by(cell_num=num).first()
        if cell is None:
            raise ObjectNotFound('Cell '+ num + 'not found in database')
        for key in cell_data:
            if key == "cell_num":
                cell.cell_num = cell_data[key]
            elif key == "crop_type":
                cell.crop_type = cell_data[key]
        db.session.commit()

    def delete(self, num):
        cell = Cell.query.filter_by(cell_num=num).first()
        if cell is None:
            raise ObjectNotFound('Cell '+ num + ' not found in database')
        historics = cell.historics.all()
        for h in historics:
            db.session.delete(h)
        db.session.delete(cell)
        db.session.commit()

class HistoricManagement(Resource):
    def get(self, external_id=None):
        if external_id is not None:
            try:
                location_info = get_location(external_id)
            except:
                raise ObjectNotFound('The UE with external_id ' + external_id + ' is not found')
            cell_num = location_info._location_info.cell_id
            cell = Cell.query.filter_by(cell_num=cell_num).first()
            if cell is None:
                raise ObjectNotFound('Cell '+ cell_num + ' not found in database')
            historics = cell.historics.all()
            result = historic_schema.dump(historics, many=True)
        else:
            historics = Historic.query.all()
            result = historic_schema.dump(historics, many=True)
        return result

    def post(self, external_id):
        historic_data = request.form
        try:
            location_info = get_location(external_id)
        except:
            raise ObjectNotFound('The UE with external_id ' + external_id + ' is not found')
        cell_num = location_info._location_info.cell_id

        cell = Cell.query.filter_by(cell_num=cell_num).first()
        if cell is None:
            raise ObjectNotFound('Cell '+ cell_num + ' not found in database')
        historic = Historic(temperature=historic_data["temperature"],humidity=historic_data["humidity"], crop = cell.crop_type, cell=cell)
        db.session.add(historic)
        db.session.commit()
    
    def put(self, historic_id):
        historic_data = request.form
        historic = Historic.query.filter_by(id=historic_id).first()
        if historic is None:
            raise ObjectNotFound('Historic '+ historic_id + ' not found in database')
        for key in historic_data:
            if key == "temperature":
                historic.temperature = historic_data[key]
            elif key == "crop":
                historic.crop = historic_data[key]
            elif key == "humidity":
                historic.humidity = historic_data[key]
        db.session.commit()
    
    def delete(self, historic_id):
        historic = Historic.query.filter_by(id=historic_id).first()
        if historic is None:
            raise ObjectNotFound('Historic '+ historic_id + ' not found in database')
        db.session.delete(historic)
        db.session.commit()


api.add_resource(CellManagement,'/cells','/cells/<string:num>')
api.add_resource(HistoricManagement,'/historics/<string:external_id>','/historics', '/historics/<int:historic_id>')