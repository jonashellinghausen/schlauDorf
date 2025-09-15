import requests
from flask import Blueprint, Response, current_app, request

bp = Blueprint('maps', __name__, url_prefix='/api')


@bp.route('/wms-proxy')
def wms_proxy():
    base_url = current_app.config.get('WMS_BASE_URL')
    params = request.args.to_dict()
    params.setdefault('SERVICE', 'WMS')
    params.setdefault('VERSION', '1.3.0')
    params.setdefault('REQUEST', 'GetMap')
    response = requests.get(base_url, params=params)
    return Response(response.content, content_type=response.headers.get('content-type'))
