from app.utils.api import ApiResource
from app.utils.api.authentication import authenticate

class ApiVersion(ApiResource):
    """
    Checking api version handle /api/versions
    """
    def __init__(self):
        pass
        # Validation rules for get method
        # self.getParser = reqparse.RequestParser()
        # self.getParser.add_argument(
        #     "platform", required=False, type=ApiValidation.checkPlatformList, location="args")


    @authenticate(need_auth=False)
    def get(self):
        """
        Get list current version of app
        Params:
            No

        Request params:

        Response:
        {
            u"ios": "1.0.0",
            u"android": "1.0.0",
            u"windows": "1.0.0",
        }
        """
        platform_versions = {
            "ios": "1.0",
            #"android": "1.0",
            #"windows": "1.0",
        }
        return platform_versions
