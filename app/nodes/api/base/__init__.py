from flask import Blueprint
from app.utils.api import ApiInfo
from flask.ext.restful import Api
from version import ApiVersion


api_blueprint = Blueprint('api_blueprint', __name__)

api_base = Api(api_blueprint, prefix=ApiInfo.URI_BASE)

# Return supported version
api_base.add_resource(ApiVersion, '/versions')


from flask import make_response
from app.utils import custom_json


# Hack to update the custom json dump support decimal
def custom_json_output(data, code, headers=None):
    if not 'success' in data:
        data['success'] = False

    dumped = custom_json.dumps(data, use_decimal=True)
    if code == 403:
        resp = make_response(dumped, 403)
    else:
        resp = make_response(dumped, 200)
    resp.headers.extend(headers or {})
    return resp

api_base.representations.update({
    'application/json': custom_json_output
})
