from flask import Blueprint
from app.utils.api import ApiInfo
from flask.ext.restful import Api

from users import ApiUserList, ApiUserLogin, ApiUserLoginFb, ApiUser
#from photos import ApiPhotoList, ApiPhoto
#from me import ApiMe, ApiMeFriendList, ApiMePatyList, ApiMeDeviceToken, ApiMeFeedList, ApiMeNotificationList, ApiMeLogout, ApiMeInvitation, ApiMeNewActivityList


api_v1_blueprint = Blueprint('api_v1_blueprint', __name__)

api_v1 = Api(api_v1_blueprint, prefix=ApiInfo.URI_V1)

# Endpoint for handling current logged User
# api_v1.add_resource(ApiMe, '/me')
# api_v1.add_resource(ApiMeFriendList, '/me/friends')
# api_v1.add_resource(ApiMePatyList, '/me/paties')
# api_v1.add_resource(ApiMeFeedList, '/me/feeds')
# api_v1.add_resource(ApiMeNotificationList, '/me/notifications')
# api_v1.add_resource(ApiMeDeviceToken, '/me/device_tokens')
# api_v1.add_resource(ApiMeLogout, '/me/logout')
# api_v1.add_resource(ApiMeInvitation, '/me/invitations')
# api_v1.add_resource(ApiMeNewActivityList, '/me/new_activities')


# Endpoint for handling User
api_v1.add_resource(ApiUserList, '/users')
api_v1.add_resource(ApiUserLogin, '/users/login')
api_v1.add_resource(ApiUserLoginFb, '/users/loginFb')
api_v1.add_resource(ApiUser, '/users/<string:uid>')

# Endpoint for handling Photo
#api_v1.add_resource(ApiPhotoList, '/photos')
#api_v1.add_resource(ApiPhoto, '/photos/<string:pid>')


from flask import make_response
from app.utils import custom_json


# Hack to update the custom json dump support decimal
def custom_json_output(data, code, headers=None):
    dumped = custom_json.dumps(data, use_decimal=True)
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp

api_v1.representations.update({
    'application/json': custom_json_output
})
