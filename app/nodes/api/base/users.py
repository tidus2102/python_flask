from flask import render_template, current_app as app
from app.utils.api import ResponseStatus, ApiResource, ApiValidation
from app.utils.api.authentication import authenticate
from flask.ext.babelex import gettext
from app.models.common import db
from app.models.user import User
from app.models.user_token import UserToken
from app.models.email_message import EmailMessage
from flask.ext.restful import reqparse, abort
from app.utils import helper
import bcrypt
import facebook


class ApiUserList(ApiResource):
    """
    Handle the the api with endpoint: /users
    """
    def __init__(self):
        # Validation rules for params
        self.postParser = reqparse.RequestParser()

        self.postParser.add_argument(
            "first_name", required=True, type=unicode, location="form",
            help=gettext("%(field)s VALIDATION_REQUIRED_ERROR", field="first_name"))

        self.postParser.add_argument(
            "last_name", required=True, type=unicode, location="form",
            help=gettext("%(field)s VALIDATION_REQUIRED_ERROR", field="last_name"))

        self.postParser.add_argument(
            "birthday", required=True, type=unicode, location="form",
            help=gettext("%(field)s VALIDATION_REQUIRED_ERROR", field="birthday"))

        self.postParser.add_argument(
            "username", required=True, type=unicode, location="form",
            help=gettext("%(field)s VALIDATION_REQUIRED_ERROR", field="username"))

        self.postParser.add_argument(
            "email", required=True, type=unicode, location="form",
            help=gettext("%(field)s VALIDATION_REQUIRED_ERROR", field="email"))

        self.postParser.add_argument(
            "email", type=ApiValidation.email, location="form")

        self.postParser.add_argument(
            "password", required=True, type=unicode, location="form",
            help=gettext("%(field)s VALIDATION_REQUIRED_ERROR", field="password"))

        self.postParser.add_argument(
            "device_id", required=True, type=unicode, location="form",
            help=gettext("%(field)s VALIDATION_REQUIRED_ERROR", field="device_id"))


    @authenticate(need_auth=False)
    def post(self):
        """
        This method to submit new user and also do authentication

        Request params:
            first_name: "string",
            last_name: "string",
            birthday: "string",
            username: "string",
            email: "string",
            password: "string",
            # fb_id: "string",
            # fb_token: "string",
            device_id: "string"

        Response:
        {
            "id": 111,
            # "fb_id": "string",
            # "fb_token": "string",
            "access_token": "string",
            "device_id": "string"
        }
        """
        data = self.postParser.parse_args()
        print data

        # Get user instance
        user, is_new = User.create(data)
        #user.updateAvatar()

        if is_new:
            db.session.flush()

        # Create associations data
        user_token = UserToken.create(
            user.id,
            helper.get(data, 'device_id', None)
        )

        # New user so send welcome email
        # if is_new:
        #     EmailMessage.create(
        #         [user.email],
        #         subject=gettext('Welcome to uPaty'),
        #         content=render_template('mail/welcome.html', user=user)
        #     )
        db.session.commit()
        return user.format_login_json(user_token)


class ApiUserLogin(ApiResource):
    """
    Handle the the api with endpoint: /users/login
    """
    def __init__(self):
        # Validation rules for params
        self.postParser = reqparse.RequestParser()

        self.postParser.add_argument(
            "username", required=True, type=unicode, location="form",
            help=gettext("%(field)s VALIDATION_REQUIRED_ERROR", field="username"))

        self.postParser.add_argument(
            "password", required=True, type=unicode, location="form",
            help=gettext("%(field)s VALIDATION_REQUIRED_ERROR", field="password"))

        self.postParser.add_argument(
            "device_id", required=True, type=unicode, location="form",
            help=gettext("%(field)s VALIDATION_REQUIRED_ERROR", field="device_id"))


    @authenticate(need_auth=False)
    def post(self):
        """
        This method to submit new user and also do authentication

        Request params:
            username: "string",
            password: "string",
            device_id: "string"

        Response:
        {
            "id": 111,
            "access_token": "string",
            "device_id": "string"
        }
        """
        data = self.postParser.parse_args()
        print data

        user = User.findByAttributes(username=data['username'])
        if not user:
            return {"message": ResponseStatus.NOT_FOUND}, 404

        password = data['password']
        if bcrypt.hashpw(password, user.password) == user.password:
            # Create associations data
            user_token = UserToken.create(
                user.id,
                helper.get(data, 'device_id', None)
            )

            db.session.commit()
            return user.format_login_json(user_token)
        else:
            return {"message": ResponseStatus.WRONG_USERNAME_OR_PASSWORD}, 404


class ApiUserLoginFb(ApiResource):
    """
    Handle the the api with endpoint: /users/loginfb
    """
    def __init__(self):
        # Validation rules for params
        self.postParser = reqparse.RequestParser()

        self.postParser.add_argument(
            "first_name", required=True, type=unicode, location="form",
            help=gettext("%(field)s VALIDATION_REQUIRED_ERROR", field="first_name"))

        self.postParser.add_argument(
            "last_name", required=True, type=unicode, location="form",
            help=gettext("%(field)s VALIDATION_REQUIRED_ERROR", field="last_name"))

        self.postParser.add_argument(
            "username", required=True, type=unicode, location="form",
            help=gettext("%(field)s VALIDATION_REQUIRED_ERROR", field="username"))

        self.postParser.add_argument(
            "email", required=True, type=unicode, location="form",
            help=gettext("%(field)s VALIDATION_REQUIRED_ERROR", field="email"))

        self.postParser.add_argument(
            "device_id", required=True, type=unicode, location="form",
             help=gettext("%(field)s VALIDATION_REQUIRED_ERROR", field="device_id"))

        self.postParser.add_argument(
            "facebook_id", required=True, type=unicode, location="form",
             help=gettext("%(field)s VALIDATION_REQUIRED_ERROR", field="facebook_id"))

        self.postParser.add_argument(
             "facebook_token", required=True, type=unicode, location="form",
             help=gettext("%(field)s VALIDATION_REQUIRED_ERROR", field="facebook_token"))


    @authenticate(need_auth=False)
    def post(self):
        """
        This method to submit new user and also do authentication

        Request params:
            first_name: "string",
            last_name: "string",
            username: "string",
            email: "string",
            device_id: "string"
            facebook_id: "string",
            facebook_token: "string",

        Response:
        {
            "id": 111,
            "access_token": "string",
            "device_id": "string"
        }
        """

        data = self.postParser.parse_args()
        print data

        # Check fb_id & fb_token
        #     graph = facebook.GraphAPI(data.get("fb_token"))
        #     profile = graph.get_object(data.get("fb_id"))
        #     canGetProfileInfo = True if helper.get(profile, "id", None) else False
        # except Exception, e:
        #     canGetProfileInfo = False

        # For dev purpose
        if app.config['env'] == 'local':
            canGetProfileInfo = True

        if canGetProfileInfo:
            # Get user instance
            user, is_new = User.create(data, 'fb')
            #user.updateAvatar()

            if is_new:
                db.session.flush()

            # Create associations data
            user_token = UserToken.create(
                user.id,
                helper.get(data, 'device_id', None)
            )

            # New user so send welcome email
            # if is_new:
            #     EmailMessage.create(
            #         [user.email],
            #         subject=gettext('Welcome to uPaty'),
            #         content=render_template('mail/welcome.html', user=user)
            #     )
            db.session.commit()
            return user.format_login_json(user_token)
        else:
            return {"message": ResponseStatus.NOT_FOUND}, 404


class ApiUser(ApiResource):
    """
    Handle the the api with endpoint: /users/<uid>
    """
    def __init__(self):
        # Validation rules for params
        pass


    @authenticate(need_auth=False)
    def get(self, uid):
        """
        Get profile a specific user
        Params:
            uid: the id of checking user

        Request params:

        Response:
        {
            "id": 111,
            "full_name": "string",
        }
        """
        checked_user = User.findById(uid)
        if not checked_user:
            abort(404, message=gettext("NOT_FOUND"))
        return checked_user.format_basic_profile_json()



