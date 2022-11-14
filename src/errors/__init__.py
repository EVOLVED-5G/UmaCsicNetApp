from flask import Blueprint

bp = Blueprint('errors',__name__)

from src.errors import handling