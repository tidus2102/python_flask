import json
from app.models.common import db
from app.models.user import User
from app.models.email_message import EmailMessage
from flask import request, render_template
from flask.ext.babelex import gettext
from app.utils.api import ApiResource, ApiValidation
from app.utils.api.authentication import authenticate
from app.utils import helper
from flask.ext.restful import reqparse
from app import notification
from app.cache import cache
from app.models.notification import Notification


class ApiMe(ApiResource):
    """
    Handle the the api with endpoint: /me
    """
    def __init__(self):
        # Validation rules for get method
        self.getParser = reqparse.RequestParser()
        self.getParser.add_argument(
            "fields", required=False, type=unicode, location="args")

        # Validation rules for post method
        # self.putParser = reqparse.RequestParser()
        # self.putParser.add_argument(
        #     "full_name", required=False, type=unicode, location="form",
        #     help=gettext("%(field)s VALIDATION_REQUIRED_ERROR", field="full_name"))


    @authenticate(need_auth=True)
    def get(self, user):
        """
        Get profile of current logged user
        Params:
          user: the User instance that pass authentication (logged user)

        Request params:
          No

        Response:
        {
            "id": 111,
            "full_name": "string",
            "email": "string",
            "fb_id": "string",
            "fb_token": "string",
        }
        """
        fields = helper.getFields(helper.get(self.getParser.parse_args(), "fields"))
        return user.format_profile_json(fields)


    @authenticate(need_auth=True)
    def put(self, user):
        """
        Update profile a specific user which is has permission: not define yet
        Params:
            uid: the id of checking user
            user: the User instance that pass authentication (logged user)

        Request params:
            full_name: "string"

        Response:
        {
            "id": 111,
            "full_name": "string",
            "email": "string",
            "fb_id": "string",
        }
        """
        # Parse data from request
        data = self.putParser.parse_args()

        # app.logger.info("Data: {0}".format(data))
        if data["full_name"]:
            user.full_name = data["full_name"]

        # Update avatar
        #user.updateAvatar()

        db.session.commit()
        return user.format_profile_json()