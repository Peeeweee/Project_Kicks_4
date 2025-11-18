from flask import Blueprint

ml_prediction_bp = Blueprint('ml_prediction', __name__, url_prefix='/ml-prediction')

from . import routes
