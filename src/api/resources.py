from flask import request, jsonify
from flask_restful import Resource, Api
from os import environ

from src import db
from src.api.models import Cell, Historic
from flask import Blueprint

from src.errors.handling import ObjectNotFound, AppErrorBaseClass

from src.api.schemas import CellSchema, HistoricSchema, CellSchemaVerbose

from evolved5g.sdk import LocationSubscriber
from evolved5g import swagger_client
from evolved5g.swagger_client import LoginApi
from datetime import datetime

bp_api = Blueprint('api', __name__, url_prefix='/api')
api = Api(bp_api)

cell_schema = CellSchema()
historic_schema = HistoricSchema()
cell_schema_verbose = CellSchemaVerbose()

netapp_id = environ.get('NETAPPID')

def get_host_of_the_nef_emulator() -> str:
    return environ.get('NEFHOST')

def request_nef_token():
    username = environ.get('NEFUSER')
    password = environ.get('NEFPASS')
    configuration = swagger_client.Configuration()
    configuration.host = get_host_of_the_nef_emulator()
    configuration.verify_ssl = False
    api_client = swagger_client.ApiClient(configuration=configuration)
    api_client.select_header_content_type(
        ["application/x-www-form-urlencoded"])
    api = LoginApi(api_client)
    token = api.login_access_token_api_v1_login_access_token_post(
        "", username, password, "", "", "")
    return token

def get_folder_path_for_certificated_and_capif_api_key():
    return environ.get('PATH_TO_CERTS')

def get_capif_host():
    return environ.get('CAPIFHOST')

def get_capif_https_port():
    return environ.get('CAPIFHTTPS')

def monitor_subscription(external_id):
    token = request_nef_token()
    host = get_host_of_the_nef_emulator()

    location_subscriber = LocationSubscriber(nef_url=host,
                                             nef_bearer_access_token=token.access_token,
                                             folder_path_for_certificates_and_capif_api_key=get_folder_path_for_certificated_and_capif_api_key(),
                                             capif_host=get_capif_host(),
                                             capif_https_port=get_capif_https_port())

    location_info = location_subscriber.get_location_information(
        netapp_id=netapp_id,
        external_id=external_id
    )
    print(location_info)

    return location_info

def error_cell_database(num):
    raise ObjectNotFound('Cell ' + num + ' not found in database')

def error_historic_database(historic_id):
    raise ObjectNotFound('Historic ' + historic_id + ' not found in database')

def error_external_id(external_id):
    raise ObjectNotFound('The UE with external_id ' + external_id + ' is not found')

class CellManagement(Resource):
    def get(self, num=None):
        verbose = request.args.get("verbose")
        if num is not None:
            cell = Cell.query.filter_by(cell_num=num).first()
            if cell is None:
                error_cell_database(num)
            if verbose is not None and verbose == "Yes":
                result = cell_schema_verbose.dump(cell)
            else:
                result = cell_schema.dump(cell)
        else:
            cells = Cell.query.all()
            if verbose is not None and verbose.lower() == "yes":
                result = cell_schema_verbose.dump(cells, many=True)
            else:
                result = cell_schema.dump(cells, many=True)
        return result

    def post(self):
        cell_data = request.form
        cell = Cell(cell_num=cell_data['cell_num'])
        db.session.add(cell)
        db.session.commit()

    def put(self, num):
        cell_data = request.get_json()
        cell = Cell.query.filter_by(cell_num=num).first()
        if cell is None:
            error_cell_database(num)
        for key in cell_data:
            if key == "cell_num":
                cell.cell_num = cell_data[key]
        db.session.commit()

    def delete(self, num):
        cell = Cell.query.filter_by(cell_num=num).first()
        if cell is None:
            error_cell_database(num)
        historics = cell.historics.all()
        for h in historics:
            db.session.delete(h)
        db.session.delete(cell)
        db.session.commit()


class HistoricManagement(Resource):
    def get(self, external_id=None):
        from_index = request.args.get("from")

        if external_id is not None:
            try:
                location_info = monitor_subscription(external_id)
            except:
                error_external_id(external_id)
            cell_num = location_info._location_info.cell_id
            cell = Cell.query.filter_by(cell_num=cell_num).first()
            if cell is None:
                error_cell_database(cell_num)
            historics = cell.historics.order_by(Historic.timestamp.asc()).all()
        else:
            if from_index is not None:
                try: 
                    index = int(from_index)
                except ValueError:
                    raise AppErrorBaseClass("Value Error")  
                historics = Historic.query.filter(Historic.id > index).order_by(Historic.timestamp.asc()).all()
            else:
                historics = Historic.query.order_by(Historic.timestamp.asc()).all()
        result = historic_schema.dump(historics, many=True)
        return result

    def post(self):
        data = str(request.data)
        historic_data = {}
        list_raw = data.split(",")
        for datapair in list_raw:
            replaced = datapair.replace('b', '')
            replaced = replaced.replace('{', '')
            replaced = replaced.replace('}', '')
            replaced = replaced.replace('"', '')
            keyvalue = replaced.split(":")
            key = keyvalue[0].replace('\'', '').strip()
            value = keyvalue[1].replace('\'', '').strip()
            historic_data[key] = value
        external_id = "10001@domain.com"
        try:
            location_info = monitor_subscription(external_id)
        except:
            error_external_id(external_id)
        cell_num = location_info._location_info.cell_id

        cell = Cell.query.filter_by(cell_num=cell_num).first()
        if cell is None:
            error_cell_database(cell_num)
        if "timestamp" in historic_data:
            datetime_data = datetime.strptime(historic_data["timestamp"], '%Y-%m-%d %H:%M:%S')
            historic = Historic(HS10_0=historic_data["HS10_0"],HS10_1=historic_data["HS10_1"], HS10_2=historic_data["HS10_2"],
                        HS30_0=historic_data["HS30_0"], HS30_1=historic_data["HS30_1"], HS30_2=historic_data["HS30_2"],
                        HS50_0=historic_data["HS50_0"], HS50_1=historic_data["HS50_1"], HS50_2=historic_data["HS50_2"],
                        FullBR=historic_data["FullBR"], AirTC=historic_data["AirTC"], RH=historic_data["RH"],
                        cell = cell, timestamp=datetime_data)
        else:
            historic = Historic(HS10_0=historic_data["HS10_0"],HS10_1=historic_data["HS10_1"], HS10_2=historic_data["HS10_2"],
                        HS30_0=historic_data["HS30_0"], HS30_1=historic_data["HS30_1"], HS30_2=historic_data["HS30_2"],
                        HS50_0=historic_data["HS50_0"], HS50_1=historic_data["HS50_1"], HS50_2=historic_data["HS50_2"],
                        FullBR=historic_data["FullBR"], AirTC=historic_data["AirTC"], RH=historic_data["RH"],
                        cell = cell) 
        db.session.add(historic)
        db.session.commit()
    
    def put(self, historic_id):
        historic_data = request.form
        historic = Historic.query.filter_by(id=historic_id).first()
        if historic is None:
            error_historic_database(historic_id)
        for key in historic_data:
            if key == "HS10_0":
                historic.HS10_0= historic_data[key]
            elif key == "HS10_1":
                historic.HS10_1 = historic_data[key]
            elif key == "HS10_2":
                historic.HS10_2 = historic_data[key]
            elif key == "HS30_0":
                historic.HS30_0 = historic_data[key]
            elif key == "HS30_1":
                historic.HS30_1 = historic_data[key]
            elif key == "HS30_2":
                historic.HS30_2 = historic_data[key]
            elif key == "HS50_0":
                historic.HS50_0 = historic_data[key]
            elif key == "HS50_1":
                historic.HS50_1 = historic_data[key]
            elif key == "HS50_2":
                historic.HS50_2 = historic_data[key]
            elif key == "FullBR":
                historic.FullBR = historic_data[key]
            elif key == "AirTC":
                historic.AirTC = historic_data[key]
            elif key == "RH":
                historic.RH = historic_data[key]
        db.session.commit()

    def delete(self, historic_id):
        historic = Historic.query.filter_by(id=historic_id).first()
        if historic is None:
            error_historic_database(historic_id)
        db.session.delete(historic)
        db.session.commit()

@bp_api.route('/database/utils/clear')
def clear_data():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()
    return jsonify({"status":"success"})

api.add_resource(CellManagement,'/cells','/cells/<string:num>')
api.add_resource(HistoricManagement,'/historics/', '/historics/<int:historic_id>', '/historics/<string:external_id>')
