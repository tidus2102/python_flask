from common import db, UTCDateTime, Base
from app.models.user_token import UserToken
from flask.ext.login import UserMixin
from app.utils import helper
import pytz
import bcrypt
from datetime import datetime
#from sqlalchemy import and_, or_
#from flask import current_app as app, url_for

class User(UserMixin, Base, db.Model):
    __tablename__ = "tbl_user"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))
    updated_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))

    first_name = db.Column(db.UnicodeText())
    last_name = db.Column(db.UnicodeText())
    full_name = db.Column(db.UnicodeText())

    email = db.Column(db.UnicodeText(), unique=True)
    username = db.Column(db.UnicodeText(), unique=True)
    password = db.Column(db.UnicodeText())

    ROLE_ADMIN = u'Admin'
    ROLE_USER = u'User'
    role = db.Column(db.Enum([ROLE_ADMIN, ROLE_USER], native_enum=False), default=ROLE_USER)

    secret_token = db.Column(db.UnicodeText(), unique=True)

    STATUS_UNACTIVATED = u"unactivated"
    STATUS_ACTIVATED = u"activated"
    status = db.Column(db.Enum([STATUS_UNACTIVATED, STATUS_ACTIVATED], native_enum=False), default=STATUS_ACTIVATED)

    # Relations
    user_tokens = db.relationship('UserToken', backref='user', lazy='dynamic', foreign_keys='UserToken.user_id', order_by='UserToken.id')

    ####################
    # Instance methods #
    ####################
    # Contruction
    def __init__(self, email, username, password):
        self.email = email
        self.username = username

        # TODO: Update this when user register by email, password
        if not password:
            self.password = User.hash_password(helper.generate_string())
        else:
            self.password = User.hash_password(password)

        self.secret_token = helper.generate_string()

        # TODO: Also update this later
        self.status = self.STATUS_ACTIVATED

    @classmethod
    def hash_password(cls, password):
        return bcrypt.hashpw(password, bcrypt.gensalt(12))

    def check_password(self, input_password):
        return bcrypt.hashpw(input_password, self.password) == self.password

    def to_json(self, user_token):
        all_fields = ["id", "first_name", "last_name", "email", "username", "password", "created_at", "updated_at"]
        return self.returnJsonByFields(all_fields, fields)

    def updateDeviceToken(self, data):
        device_id = data['device_id']
        device_type = helper.get(data, 'device_type', UserToken.DEVICE_TYPE_APNS)
        # if not device_type in [UserToken.DEVICE_TYPE_APNS, UserToken.DEVICE_TYPE_GCM]:
        #     return False, 'Device type is invalid'

        user_token = UserToken.findByAttributes(
            user_id = self.id,
            device_id = device_id,
            is_active = True
        )

        if not user_token:
            return None, 'Data not found'

        user_token.device_token = data['device_token']
        user_token.device_type = device_type

        #db.session.add(user_token)
        return True, ''

    # logout device
    def logoutDevice(self, device_id):
        user_token = UserToken.findByUserAndDevice(self.id, device_id)

        if user_token:
            user_token.is_active = False
            return user_token

        return None

    @classmethod
    def getRoleList(cls):
        return [cls.ROLE_ADMIN, cls.ROLE_USER]

    @classmethod
    def create(cls, data, type='Admin'):
        username = data['username']
        if not username:
            return None, False, 'Username is empty'

        username = username.strip()
        temp_user = cls.query.filter_by(username = username).first()
        if temp_user:
            return None, False, 'Username is existed'

        email = helper.get(data, 'email')
        if not email:
            return None, False, 'Email is empty'

        email = email.strip()
        temp_user = cls.query.filter_by(email = email).first()
        if temp_user:
            return None, False, 'Email is existed'

        password = data['password']
        if not password:
            return None, False, 'Password is empty'

        user = cls(email, username, password)

        user.first_name = helper.get(data, 'first_name')
        user.last_name = helper.get(data, 'last_name')

        role = helper.get(data, 'role')
        if role and role in User.getRoleList():
            user.role = role
        else:
            return None, False, 'Role is invalid'

        db.session.add(user)

        return user, True, ''
